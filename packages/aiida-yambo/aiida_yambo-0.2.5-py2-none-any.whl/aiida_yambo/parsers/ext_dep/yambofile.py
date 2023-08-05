# Copyright (C) 2016 Henrique Pereira Coutada Miranda
# All rights reserved.
#
# This file is part of yamboparser
#
#
import os
import re
import numpy as np

#we try to use netcdf
try:
    from netCDF4 import Dataset
except ImportError:
    _has_netcdf = False
else:
    _has_netcdf = True

class YamboFile():
    """
    This is the Yambo file class.
    It takes as input a filename produced by yambo.
    Can be a netcdf or a text file
    
    List of supported NETCDF files:
        -> ndb.QP

    List of supported text files:
        -> r-*_em?1_*_gw0
        -> o-*.qp
    """
    _output_prefixes = ['o-']
    _report_prefixes = ['r-','r.']
    _log_prefixes    = ['l-','l.']
    _p2y_log_prefixes = ['l_']
    _netcdf_prefixes = ['ns','ndb']
    _netcdf_sufixes  = {'QP':'gw','HF_and_locXC':'hf'}

    def __init__(self,filename,folder='.'):
        self.filename = filename
        self.folder   = folder
        self.type     = None   
        self.errors   = [] #list of errors
        self.warnings   = [] #list of warnings
        self.memstats   = [] #list of memory allocation statistics
        self.max_memory = None # max memory allocated or freed (Gb)
        self.last_memory = None # last memory allocated or freed (Gb)
        self.last_memory_time = None # last memory allocated or freed (Gb)
        self.timestats   = [] #list of reported times 
        self.last_time = None # last reported time 
        self.yambo_wrote = None #  yambo performed a write to disk
        self.data     = {} #dictionary containing all the important data from the file
        self.kpoints = {}
        self.timing = []
        self.timing_section = []
        self.timing_overview = {} 
        self.wall_time = None
        self.game_over = False  # check yambo run completed successfully
        self.p2y_complete = False  # check yambo initialization completed successfully
        self.para_error = False 
        self.unphysical_input = False 
        if any(filename.startswith(prefix) for prefix in self._output_prefixes):
            #read lines from file
            f = open("%s/%s"%(folder,filename),'r')
            self.lines = f.readlines()
            f.close()

            #get the line with the title
            try:
                title = self.lines[14]
            except:
                self.errors.append('error reading title')
                return
            if 'GW' in title:
                 self.type = 'output_gw'

        elif any(filename.startswith(prefix) for prefix in self._report_prefixes):
            self.type = 'report'
        elif any(filename.startswith(prefix) for prefix in self._log_prefixes):
            self.type = 'log'
        elif any(filename.startswith(prefix) for prefix in self._p2y_log_prefixes):
            self.type = 'p2y_log'
        elif any(filename.startswith(prefix) for prefix in self._netcdf_prefixes) and _has_netcdf:
            for sufix in self._netcdf_sufixes:
                if filename.endswith(sufix): 
                    self.type = 'netcdf_%s'%self._netcdf_sufixes[sufix]
                    break

        if self.type is None: self.type = 'unknown'
        
        #parse the file
        self.parse()

    def parse(self):
        """ Parse the file
            Add here things to read log and report files...
        """
        if   self.type == 'netcdf_gw': self.parse_netcdf_gw()
        elif self.type == 'netcdf_hf': self.parse_netcdf_hf()
        elif self.type == 'output_gw': self.parse_output()
        elif self.type == 'log': self.parse_log()
        elif self.type == 'p2y_log': self.parse_p2y_log()
        elif self.type == 'report'  : self.parse_report()

    def parse_output(self):
        """ Parse an output file from yambo,
        """
        #get the tags of the columns
        if self.type == "output_absorption":
            tags = [tag.strip() for tag in re.findall('([ `0-9a-zA-Z\-\/]+)\[[0-9]\]',''.join(self.lines))]
        if self.type == "output_gw":
            tags = [line.replace('(meV)','').replace('Sc(Eo)','Sc|Eo') for line in self.lines if all(tag in line for tag in ['K-point','Band','Eo'])][0]
            tags = tags[2:].strip().split()
        table = np.genfromtxt(self.lines)
        _kdata ={}
        if table.ndim> 1:
            k_index =[ str(int(i)) for i in table[:,0]] # first column  has kpoints
        else:
            k_index =[ str(int(table[0])) ] # first column  has kpoints
        for ind in range(len(k_index)):
            for itag in range(len(tags)):
                 if k_index[ind] not in _kdata.keys():
                     _kdata[k_index[ind]] = {}
                 try:
                     _kdata[k_index[ind]][tags[itag]].append(table[ind,itag])
                 except KeyError:
                    try:
                         _kdata[k_index[ind]][tags[itag]]  = [ table[ind,itag] ]
                    except IndexError:
                         _kdata[k_index[ind]][tags[itag]]  = [ table[itag] ]

        self.data = _kdata 
        #self.data = dict(zip(tags,table.T))

    def parse_netcdf_gw(self):
        """ Parse the netcdf gw file
        """
        if _has_netcdf:
            data = {}
            f = Dataset('%s/%s'%(self.folder,self.filename))
            #quasiparticles table
            qp_table  = f.variables['QP_table'][:].T
            data['Kpoint_index'] = qp_table[:,2]
            data['Band'] = qp_table[:,0]
            if qp_table.shape[1] == 4: # spin polarized
                data['Spin_pol'] = qp_table[:,3]
            data['qp_table'] = qp_table[:,1:]  # ib, ik, ,(isp if spin polarized)
            #qpoints
            data['Kpoint']   = f.variables['QP_kpts'][:].T

            #quasi-particles
            #old format
            if 'QP_E_Eo_Z' in f.variables:
                qp = f.variables['QP_E_Eo_Z'][:]
                qp = qp[0]+qp[1]*1j
                data['E'],  data['Eo'], data['Z'] = qp.T
                data['E-Eo'] = data['E']  -  data['Eo'] 
                self.data=data
                f.close()
            #new format
            else:
                E  = f.variables['QP_E'][:]
                data['E'] = E[:,0] + E[:,1]*1j
                Eo = f.variables['QP_Eo'][:]
                data['Eo']= Eo
                Z  = f.variables['QP_Z'][:]
                data['Z'] = Z[:,0] + Z[:,1]*1j
                data['E-Eo'] = data['E']  -  data['Eo'] 
                self.data=data
                f.close()
       
    def parse_netcdf_hf(self):
        """ Parse the netcdf hf file (ndb.HF_and_locXC)
        """
        if _has_netcdf:
            data = {}
            f = Dataset('%s/%s'%(self.folder,self.filename))
            hf =  f.variables['Sx_Vxc'][:]
            if hf.shape[0]%8 ==0 :
                qp =  hf.reshape(-1,8)
                ib, ibp, ik, isp, rsx, isx, revx, imvx = qp.T
            else:
                qp =  hf.reshape(-1,7)
                ib, ibp, ik, rsx, isx, revx, imvx = qp.T
            data['Sx'] = rsx + isx*1j 
            data['Vxc'] = revx + imvx*1j

            self.data=data
            f.close()
 
    def parse_report(self):
        """ Parse the report files.
            produces output of this nature:
            { k-index1  : { 'dft_enrgy':[...], 'qp_energy':[...] },
              k-index2  :{...}
            }
            k-index is the kpoint at which the yambo calculation was
            done.
        """
        if not hasattr(self, 'lines'):
            with open('%s/%s'%(self.folder,self.filename)) as fl:
                self.lines = fl.readlines()
        # start with check for  failure due to error:
        err = re.compile('^\s+?\[ERROR\]\s+?(.*)$')
        kpoints = re.compile('^  [A-X*]+\sK\s\[([0-9]+)\]\s[:](?:\s+)?([0-9.E-]+\s+[0-9.E-]+\s+[0-9.E-]+)\s[A-Za-z()\s*.]+[0-9]+[A-Za-z()\s*.]+([0-9.]+)')
        timing = re.compile('\s+?[A-Za-z]+iming\s+?[A-Za-z/\[\]]+[:]\s+?([a-z0-9-]+)[/]([a-z0-9-]+)[/]([a-z0-9-]+)')
        timing_section = re.compile('^\s+?\[\d+[.]?\d+?\]\s+?(.*)$')
        game_over = re.compile('^\s+?\[\d+\]\s+?G\w+\s+?O\w+\s+?\&\s+?G\w+\s+?\w+') # Game over & Game summary
        p2y_complete = re.compile('^(\s+)?[-<>\d\w]+\s+?P\d+[:]\s+?==\s+?P2Y\s+?\w+\s+?==(\s+)?') # P2Y Complete
        p2y_complete_v2 = re.compile('(\s+)?[-<>\w\d]+(\s+)?==(\s+)?P2Y(\s+)?\w+(\s+)?==') # P2Y Complete
        yambo_wrote =  re.compile('(?:\s+)?[[]WR[./\w]+[]](?:[-])+')
        timing_overview = re.compile('\s+?([a-zA-Z_()0-9\s]+)\s+?:\s+?([0-9a-z.]+)\s*?CPU\s*?([(]?\s*?(\d+)?\s*?[a-z]+[,]\s*?([\d.]+\s+?s)\s+?avg[)])?$')
        current_timing_section= None
        for line in self.lines:
            if err.match(line):
                if 'STOP' in err.match(line).groups()[0]:
                    # stop parsing, this is a failed calc.
                    self.errors.append(err.match(line).groups()[0])
                    return 
            if timing_section.match(line):
                current_timing_section = timing_section.match(line).groups()[0]
            if timing.match(line):
                self.timing.append( self.get_seconds( timing.match(line).groups()[0]) )    
                self.timing_section.append(current_timing_section)                         
            if kpoints.match(line):                                                        
                kindx, kpt, wgt = kpoints.match(line).groups()                             
                self.kpoints[str(int(kindx))] =  [ float(i.strip()) for i in kpt.split(    )]
            if game_over.match(line):                                                      
                self.game_over = True                                                      
            if p2y_complete.match(line) or p2y_complete_v2.match(line):                    
                self.p2y_complete = True                                                   
                self.game_over = True                                                      
            if yambo_wrote.match(line):                                                    
                self.yambo_wrote = True                                                    
            if timing_overview.match(line):
                name, total, _ , calls, avg = timing_overview.match(line).groups()
                self.timing_overview[name.replace(' ','')] =  self.get_seconds( total) 
                self.timing_overview[name.replace(' ','')+'_calls'] = int(calls) if calls else calls
                if avg:
                    self.timing_overview[name.replace(' ','')+'_avg'] = self.get_seconds(avg.replace(' ',''))
    
        full_lines = ''.join(self.lines)
        qp_regx = re.compile('(^\s+?QP\s\[eV\]\s@\sK\s\[\d+\][a-z0-9E:()\s.-]+)(.*?)(?=^$)',re.M|re.DOTALL)
        kp_regex = re.compile('^\s+?QP\s\[eV\]\s@\sK\s\[(\d+)\][a-z0-9E:()\s.-]+$')
        spliter = re.compile('^(B[=]\d+\sEo[=]\s+?[E0-9.-]+\sE[=]\s+?[E0-9.-]+\sE[-]Eo[=]\s+?[E0-9.-]+\sRe[(]Z[)][=]\s+?[*E0-9.-]+\sIm[(]Z[)][=]\s?[*E0-9.-]+\snlXC[=]\s+?[E0-9.-]+\slXC[=]\s+?[E0-9.-]+\sSo[=]\s+?[E0-9.-]+)')
        extract = re.compile('B[=](\d+)\sEo[=](?:\s+)?([E0-9.-]+)\sE[=](?:\s+)?([E0-9.-]+)\sE[-]Eo[=](?:\s+)?([E0-9.-]+)\sRe[(]Z[)][=](?:\s+)?([*E0-9.-]+)\sIm[(]Z[)][=](?:\s+)?[*E0-9.-]+\snlXC[=](?:\s+)?([E0-9.-]+)\slXC[=](?:\s+)?([E0-9.-]+)\sSo[=](?:\s+)?([E0-9.-]+)')
        qp_lines = qp_regx.findall(full_lines)
        qp_results ={}
        for each in qp_lines: # first group of qp data, shares k-point index
            kp_index = None
            kp_results={'bindex':[],'dft_energy':[],'qp_energy':[],'qp_correction':[],
                        'z_factor':[],'non_local_xc':[],'local_xc':[],'selfenergy_c':[]}
            for line in each: # different band indexes =B
                if kp_regex.match(line):
                    kp_index = str(int(kp_regex.match(line).groups()[0]))
                else: #  data line B=x Eo = y ..
                    data_lines = [ i for i in spliter.split(line) if i.strip()]
                    for qp_data in data_lines:
                        bindex, dft_energy, qp_energy, qp_correction, z_factor, \
                        non_local_xc, local_xc, selfenergy_c = [ i for i in extract.match(qp_data).groups() ]
                        listed = [bindex, dft_energy, qp_energy, qp_correction, z_factor, non_local_xc, local_xc, selfenergy_c]
                        for i in range(len(listed)):
                            try:
                                listed[i] = float(listed[i])
                            except ValueError:
                                listed[i] =  np.nan
                        bindex, dft_energy, qp_energy, qp_correction, z_factor,\
                        non_local_xc, local_xc, selfenergy_c = listed
                        kp_results['bindex'].append(bindex) 
                        kp_results['dft_energy'].append(dft_energy) 
                        kp_results['qp_energy'].append(qp_energy) 
                        kp_results['qp_correction'].append(qp_correction) 
                        kp_results['z_factor'].append(z_factor) 
                        kp_results['non_local_xc'].append(non_local_xc) 
                        kp_results['local_xc'].append(local_xc) 
                        kp_results['selfenergy_c'].append(selfenergy_c) 
            qp_results[kp_index] = kp_results
        self.data = qp_results 

    def get_type(self):
        """ Get the type of file        
        """
        return self.type

    def has_errors(self):
        #check if the list is empty
        return not not self.errors

    def get_errors(self):
        """ Check if this is a report file and if it contains errors
        """
        if self.type == 'report':
            return self.errors
        return False

    def get_data(self):
        """ Get the data from this file as a dictionary 
        """
        pass

    def get_seconds( self, time_string):
        time = []
        if '-' in time_string:
            time = time_string.split('-')
        else:
            r = re.compile('([\d.]+h)?\s*([\d.]+m)?\s*([\d.]+s)?')
            hr, mn, sc = r.match(time_string).groups()
            time.append(hr if hr else '0h') 
            time.append(mn if mn else '0m') 
            time.append(sc if sc else '0s') 
          
        if time[0]=='' and time[1]=='' and time[2]=='':
            time= ['0h','0m','0s']
        if time[0].endswith('h'):
            return int(float(time[0].replace("h",""))) * 3600 + int(float(time[1].replace("m",""))) * 60 + int(float(time[2].replace("s","")))
        elif time[0].endswith('m'):
            return int(float(time[0].replace("m",""))) * 60 + int(float(time[1].replace("s","")))
        elif time[0].endswith('s'):
            return int(float(time[0].replace("s","")))
        else:
            raise Exception


    def parse_log(self):
        """ Get ERRORS and WARNINGS from  l-*  file, useful for debugging
        """
        if not hasattr(self, 'lines'):
            with open('%s/%s'%(self.folder,self.filename)) as fl:
                self.lines = fl.readlines()
        warning = re.compile('^\s+?<([0-9a-z-]+)> ([A-Z0-9]+)[:] \[(WARNING)\]? ([a-zA-Z0-9\s.()\[\]]+)?')
        error = re.compile('^\s+?<([0-9a-z-]+)> ([A-Z0-9]+)[:] \[(ERROR)\]? ([a-zA-Z0-9\s.()\[\]]+)?')
        self.warnings.extend([ line for line in self.lines if warning.match(line)])
        self.errors.extend([ line for line in self.lines if error.match(line)])
        memory = re.compile('^\s+?<([0-9a-z-]+)> ([A-Z0-9]+)[:] \[M  ([0-9.]+) Gb\]? ([a-zA-Z0-9\s.()\[\]]+)?')
        self.memstats.extend([ line for line in self.lines if memory.match(line)])
        if len(self.memstats)>0:
            self.max_memory = max([float(memory.match(line).groups()[2]) for line in self.memstats])
            self.last_memory = [float(memory.match(line).groups()[2]) for line in self.memstats][-1]
        # Function to convert time in seconds

        times = re.compile('^\s+?<([0-9a-z-]+)>')   
        self.timestats.extend([ self.get_seconds(times.match(line).groups()[0]) for line in self.lines if times.match(line)]) 
        self.last_time = self.timestats[-1]
        if len(self.memstats)>0:
            self.last_memory_time = [ self.get_seconds(memory.match(line).groups()[0]) for line in self.memstats][-1]

        generic_error = re.compile('^(?=\s+)?([A-Z0-9]+)[:] \[(ERROR)\](?=\s+)?([a-zA-Z0-9\s.()\[\]]+)?')
        paralle = re.compile('^(?=\s+)?([A-Z0-9]+)[:] \[ERROR\](?=\s+)?Impossible(?=\s+)?(?=[a-zA-Z0-9\s.()\[\]]+)?')
        unphysical = re.compile('^(?=\s+)?([A-Z0-9]+)[:] \[ERROR\](?=\s+)?\[NetCDF\]\s*NetCDF[:]\s*NC_UNLIMITED\s*in\s*the\s*wrong\s*index')
        self.errors.extend ([ line for line in self.lines if ( generic_error.match(line) and (paralle.match(line) or unphysical.match(line)) )  ])
        for line in self.lines:
            if generic_error.match(line):
                if paralle.match(line):
                    self.para_error = True
                if unphysical.match(line):
                    self.unphysical_input = True

    def parse_p2y_log(self):
        """ Get ERRORS and WARNINGS from p2y l_*  file, useful for debugging
            Get *Writing* lines, useful to tell if 'aiida' directory was created.
        """
        if not hasattr(self, 'lines'):
            with open('%s/%s'%(self.folder,self.filename)) as fl:
                self.lines = fl.readlines()
        p2y_complete = re.compile('^(\s+)?[-<>\d\w]+\s+?P\d+[:]\s+?==\s+?P2Y\s+?\w+\s+?==(\s+)?') # P2Y Complete
        p2y_complete_v2 = re.compile('(\s+)?[-<>\w\d]+(\s+)?==(\s+)?P2Y(\s+)?\w+(\s+)?==') # P2Y Complete
        error = re.compile('\[(ERROR)\](?=\s+)?([a-zA-Z0-9\s.\(\)\[\]\-]*)')
        generic_error = re.compile('^(?=\s+)?([A-Z0-9]+)[:] \[(ERROR)\](?=\s+)?([a-zA-Z0-9\s.()\[\]]+)?')
        yambo_wrote = re.compile('(?:\s+)?(?:[<>\w\d]+)(:?\s+)?(?:P\d+[:])(?:\s+)?(?:[[]\w+[]])?(?:\s+)?Writing(?:\s+)?\w+(?:\s+)?')
        for line in self.lines:
            if p2y_complete.match(line) or p2y_complete_v2.match(line):
                self.p2y_complete = True
                self.game_over = True 
            if yambo_wrote.match(line):
                self.yambo_wrote = True 
        self.errors.extend ([ line for line in self.lines if ( generic_error.match(line) or error.match(line) )  ])

    def __bool__(self):
        if self.type == 'unknown':
            return False
        else:
            return True
    __nonzero__=__bool__

    def __str__(self):
        return "type: %9s   file: %s/%s"%(self.type, self.folder, self.filename)

