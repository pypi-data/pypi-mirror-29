# -*- coding: utf-8 -*-
"""


UKBcrunch , a simple tool for crunching the UKBioBank data.

Created Sept 2017 
@author: Joe Necus (NCL, UK)
@contact: j.necus2@ncl.ac.uk



"""

import pandas as pd
import bs4 #beautifulsoup4 package
import re  
import urllib3
import urllib2
import numpy as np
import os
from datetime import datetime


class UKBcrunch():
    """ A class to crunch UK Biobank data.
    
    To initialise:
        
        UKB_data=UKBcrunch(html_filepath, csv_filepath) 
  

    class variables
        html_file = path to html
        soup = parsed tables from html
        Vars = all variables extracted in data frame
        Eids = all Eids (encoded ID) extracted in data frame
    
        
    """
    
    special_char = "~`!@#$%^&*()_-+={}[]:>;',</?*-+" # needed to handle special chars in variable names
    sub_link  = 'http://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id='

    
    def __init__(self, html_file=None, csv_file=None):
                
        # Get filepath        
        if html_file is not None and csv_file is not None:
            #Construct the path to the html file
            self.html_file = html_file
            self.csv_file = csv_file
        else:
            ValueError("Must give location to folder containing html & csv")
        
        
        self.coding3_file=os.path.dirname(__file__)+'/coding_files/coding3.tsv'
        self.coding4_file=os.path.dirname(__file__)+'/coding_files/coding4.tsv'
        self.coding6_file=os.path.dirname(__file__)+'/coding_files/coding6.tsv'
        
        # Number of cases in csv
        self.N = len(pd.read_csv(self.csv_file,low_memory=False))
        
        #stores bulk variable code requests
        self.bulk_request=[]

        # Parse html
        # This enables easy searching of the html file for information on variables
        self.soup = self.makeSoup()
        
        #Time/date variables (initialised to arbitrary dates)
        self.date_format = "%Y-%m-%d"
        self.end_follow_up = "2016-02-15"
        self.start_follow_up = "2006-05-10"
        self.Time_end = datetime.strptime(self.end_follow_up, self.date_format)
        
        #Gathering all Variables from html file 
        self.Vars = self.gather_all_vars()['names']
        self.Data_types = self.gather_all_vars()['types']

        #Illness codes
        self.IllnessCodes=self.get_illness_codes()
        self.CancerCodes=self.get_cancer_codes()
        
        #Medication codes
        self.MedicationCodes=self.get_medication_codes() 


        #Gathering all eids from html file 
        self.Eids = self.gather_all_eids()
        self.OK = False
        if self.Eids is not None:
            self.OK = True
        if not self.OK:
            print 'error - failed to get Eids'
            self.OK = False
            return
        
        #Gathering all assesment centre visit dates ([53.0] 1st visit [53-1] 2nd visit [53-2] Imaging visit)
        
	if 'Date of attending assessment centre' in self.Vars:
            self.assess_dates = self.get_assessment_dates()

        
        
        
    """ Methods defined here onwards """
        

    def makeSoup(self):
        """Parse the html into a nested data structure"""
        f = open(self.html_file, 'r').read()
        soup = bs4.BeautifulSoup(f, 'html.parser')
        return soup
        

    def gather_all_vars(self):
        """Read all variable names in the table and return"""
        
        allrows = self.soup.findAll('tr')
        res = []
        data_type = []
        for t in allrows:
            re_string = 'nowrap;\">(.*?)</span></td><td rowspan=\"(\d+)\">(.*?)</td></tr>'
            res1=re.search(re_string,str(t))
            if not res1 is None:
                res1 = res1.group(0)
                ## get variable data type
                x1,y1,z1=res1.partition('nowrap;\">')
                xx1,yy1,zz1=z1.partition('</span>')
                data_type.append(xx1)
                ## get variable name
                x,y,z = zz1.partition('">')
                xx,yy,zz = z.partition('</td></tr>')
                if xx.find('<br>') > -1:
                    t = xx.find('<br>')
                    xx = xx[0:t]
                res.append(xx)
        res2 = []
        for x in res:
            if x.find('<br/>') >-1:
                 t = x.find('<br/>')
                 xx = x[0:t]
                 res2.append(xx)
            else:
                 res2.append(x)
        res = res2
        return {'names':res, 'types':data_type}

    def gather_all_eids(self):
        """Return all the EIDs"""
        # data frame of EIDs
        filename = self.csv_file 
        if filename == None:
            return None
        EIDs = pd.read_csv(filename, usecols=['eid'], nrows=self.N)
        return EIDs
    
    def get_assessment_dates(self):
        # data frame of EIDs
        var = 'Date of attending assessment centre'
        Ds = self.extract_variable(var)
        return Ds   


    #TODO: Extract variable currently accesses UKB showcase. May wish to edit this to access the html file (or some other more stable resource..)
    def extract_variable(self, variable=None):
        """Extract a single set of variable IDs given a single variable name as a list or string"""
        
        ### extract fields from supplied .html file
        allrows = self.soup.findAll('tr') # all rows in html file
        
        
        ## search variable string for problematic characters
        symbols = UKBcrunch.special_char

        varlist = list(variable)
        lvarlist = len(varlist)
        newvar = []
        for v in range(0, lvarlist):
            if varlist[v] in symbols:
                newvar.extend(['\\', varlist[v]])
            else:
                newvar.extend([varlist[v]])
        variable = ''.join(newvar)
                
        userrows = [t for t in allrows if re.search('>'+variable+'<',str(t))]
        
        if not userrows:
            userrows = [t for t in allrows if re.search('>'+variable+'.<',str(t))]
            
        #TODO:This fails if an unrecognised variable is found. This function should throw an error if so to enable easy detection of error
        
        userrows_str = str(userrows[0])

        IDs = [] # extract raw ids (e.g. 31 (Sex)) IDs related to variables
        
        # extract all variable names 
        match1 = re.search('id=(\d+)',userrows_str)
        if match1:
            IDs.append(match1.group(1))
            
        var_names = variable

        ## Retrieve all associated columns with variables names 
        Sub_list = {}
        
        
        for idx in IDs:

            key = []
                       
            #accessing row in html source file according to reference showcase link
            for link in self.soup.find_all('a', href=UKBcrunch.sub_link+idx):               
                tmp = str(link.contents[0].encode('utf-8'))#return associated code (e.g. sex (31-0))
                key.append(tmp)
            
            
                         
                ### Below I am trialling accessing the data showcase to determine whether the current field is 'Bulk' data or not        
                #Delete if necessary #                
                #opening data showcase link and parsing
                try:
                    page = urllib2.urlopen(UKBcrunch.sub_link+idx).read()
                except:
                    pass #page not acccesible
                else:
                    soup = bs4.BeautifulSoup(page, 'html.parser')            
                
                    for link in soup.find_all('td', class_="txt_blu"):#locating part of html where bulk field is located
                        bulk_type=str(link.contents[0].encode('utf-8'))
                    
                        #If current variable is deemed to be 'bulk', then save this into list of bulk vars
                        if bulk_type=='Bulk':
                            
                            bulk_code=tmp.replace('-','_').replace('.','_')#generating bulk code (contains underscores instead of . or -)
                            self.bulk_request.append(bulk_code)
                ### Trialling above ###
            
            
            
            Sub_list[var_names]=key
            
            
        my_range = Sub_list[var_names]
        my_range.append('eid') # Encoded anonymised participant ID
        filename = self.csv_file
        everything = pd.read_csv(filename,usecols=my_range,nrows=self.N)
        
            
        return everything
        
    
    def extract_many_vars(self, keywords=None, spaces=False, visit=None,instance=None, demographics=True):
        """Extracts variables for several pre-specified var. names 
        returns one single df with eids and each variables as columns"""
        
        if type(keywords)==str: # if string given (single var) then convert to list
            ls=[]
            ls.append(keywords)
            keywords=ls[:]
        
        #Returning standard demographic information
        if demographics==True:
            if keywords==None:
                keywords=[]
                
            if 'Sex' in self.Vars and 'Age when attended assessment centre' in self.Vars:
                        keywords.extend(['Sex','Age when attended assessment centre'])
            
            
            # including other demographics can cause trouble later down the line. E.g. if visit1 is selected then it will make it difficult to obtain age at visit 2, it will be hard to.
            #'Body mass index (BMI)','Age when attended assessment centre','Ethnic background','Sex'])
        
        #Extract vars
        main_Df = pd.DataFrame(columns = ['eid'])
        main_Df['eid'] = self.Eids['eid']
        for var in keywords:
            DBP = self.extract_variable(variable=var)
            if spaces:
                b,k,a = var.partition(' ')
                var = b
            DBP = self.rename_columns(DBP, var)           
            
            main_Df = pd.merge(main_Df,DBP,on='eid',how='outer')
        
        if visit is not None:
                main_Df=self.select_visit(df=main_Df,visit=visit, demographics=demographics)
                
        if instance is not None:
                main_Df=self.select_instance(df=main_Df,instance=instance)
        
        
        return main_Df
     
    
    def select_visit(self, df=None,visit=None,demographics=False):
        """returns dataframe containing only selected visit"""
        ls=['eid']#include eid column
        
        #extract columns with '_(visit)'
        for var in df.columns:
            res = re.search('(.*?)_'+str(visit)+'.(\d+)',var)
            if not res is None:
                ls.append(res.group(0))
        
        if visit > 0 and demographics is True:            
            ls.append('Sex_0.0')#appending sex, which is only included as visit 0       
        
        return df.loc[:,ls]#return df with list of selected columns
    
    
    def select_instance(self, df=None,instance=None):
        # returns dataframe containing only selected instnace e.g. '0.(instance)'
        ls=['eid']#include eid column
        
        #extract columns with '_(visit)'
        for var in df.columns:
            res = re.search('(.*?)_(\d+).'+str(instance)+'(.*)',var)
            if not res is None:
                ls.append(res.group(0))
               
        return df.loc[:,ls]#return df with list of selected columns
       
    


    def show_related_vars(self, keyword=None):
        
        if type(keyword)!=list: #if not list then make list
            ls=[]
            ls.append(keyword)            
            keyword=ls[:]
        
        keywords='|'.join('({0})'.format(i) for i in keyword)

        matches = [t for t in self.Vars if re.search(keywords,t,re.IGNORECASE)]
        
        if len(matches)<1:
            print('No matches found')
        
        return matches


    def get_demographics(self, visit=None):
        """ Returns simple dataframe containing demographics information """
        return self.extract_many_vars()
    
    def gather_related_vars(self, keyword=None,visit=None,instance=None,demographics=True):
    # Extracts all variables 'related' to a keyword variable or list of keyword variables. Note: this function will ignore case.
    # Returns single df 

           
        if type(keyword)!=list: #if not list then make list
            ls=[]
            ls.append(keyword)            
            keyword=ls[:]
            
        keywords='|'.join('({0})'.format(i) for i in keyword)
        
        matches = [t for t in self.Vars if re.search(keywords,t,re.IGNORECASE)]#searching all vars for those containing keyword
        

        if len(matches)<1:
            print('No matches found')
            data=None
            
        #may need to include if len ==1, self.extract_singl_var ..
        else:
            data=self.extract_many_vars(keywords=matches,visit=visit,instance=instance,demographics=demographics)
        
        return data
        
    
    def vars_by_visits(self, col_names=None,visit=0):
        # returns variables names associated with initial assessment (0), 1st (1) and 2nd (2) re-visit
        # 1st (1) and 2nd (2) re-visit
        V1 =[]
        for var in col_names:
            res = re.search('(.*?)-'+str(visit)+'.(\d+)',var)
            if not res is None:
                V1.append(res.group(0))
        return V1 
    
    
    def get_cancer_codes(self):
        """Returns data coding convention from coding3 files (cancer encoding)"""
        
        Cancer_codes=pd.read_table(self.coding3_file,index_col='coding',usecols=['coding','meaning'])
        Cancer_codes.drop(-1,inplace=True)#drop '-1' codings
        return Cancer_codes
        
    
    def get_illness_codes(self):
        """Returns data coding convention from coding6 files (illness encoding)"""
        
        noCancer_codes=pd.read_table(self.coding6_file,index_col='coding',usecols=['coding','meaning'])
        noCancer_codes.drop(-1,inplace=True)#drop '-1' codings
        return noCancer_codes
    
    def get_medication_codes(self):
        """Returns data coding convention from coding4 file"""
        med_codes=pd.read_table(self.coding4_file,index_col='coding')
        return med_codes
    
    
    def get_illness_summary(self, in_df=None, Cancer=False):    
        """Returns information regarding the frequency of various illnesses in the current data
        sample (if in_df is not provided then the whole  'ukbc' object dataset will be summarised"""
        
        if Cancer==True:
            k='Cancer code, self-reported'#setting column keywords
            illness_codes=self.CancerCodes
        else:
            k='Non-cancer illness code, self-reported'
            illness_codes=self.IllnessCodes
        
        #1. Get dataframe with all medication information
        if in_df is not None:
            df=in_df.copy()
        else:
            df=self.gather_related_vars(keyword=k)            
        
        illness_columns=df.filter(regex=k).columns
        
        out_df=pd.DataFrame()
        
        #2. For each illness in illness codes count the frequencies (separately for each sex)
        for sex,sex_df in df.groupby('Sex_0.0'):
            for code in illness_codes.index:
                    bool_df=sex_df.loc[:,illness_columns]==int(code)
                    freq=(bool_df.sum(axis=1)>0).sum()
                    out_df.loc[illness_codes.loc[code,'meaning'],'IllnessFrequencySex'+str(sex)]=freq       
        
   
        return out_df 
    
    
    def get_medication_summary(self, in_df=None):    
        """Returns information regarding the frequency of various medications in the current data
        sample (if in_df is not provided then the whole  'ukbc' object dataset will be summarised"""
        
        k='Treatment/medication code'#setting column keyword
        medication_codes=self.MedicationCodes 
        
        #1. Get dataframe with all medication information
        if in_df is not None:
            df=in_df.copy()
        else:
            df=self.gather_related_vars(keyword=k)            
        
        
        medication_columns=df.filter(regex=k).columns
       
        out_df=pd.DataFrame()
        
        #2. For each illness in illness codes count the frequencies (separately for each sex)
        for sex,sex_df in df.groupby('Sex_0.0'):
            for code in medication_codes.index:
                    bool_df=sex_df[medication_columns]==int(code)
                    freq=(bool_df.sum(axis=1)>0).sum()
                    out_df.loc[medication_codes.loc[code,'meaning'],'MedicationFrequencySex'+str(sex)]=freq
        return out_df 
    

    
    def rename_columns(self, df=None,key=None,option_str=True):
        # rename the columns of a data frame with something sensible
        col_names = df.columns.tolist()
        col_new = ['eid']
        for k in range(3):
            V0 = self.vars_by_visits(col_names,k)
            for v in V0:
                b,k,a = v.partition('-')
                if option_str:
                    col_new.append(key+'_'+a)
                else:
                    col_new.append(key)
        df_new = pd.DataFrame(columns=col_new)
        for c in range(len(col_new)):
            df_new[col_new[c]] = df[col_names[c]]
        return df_new 
    
    
    
    
    
