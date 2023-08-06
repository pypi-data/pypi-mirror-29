#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 12:20:49 2017

@author: b5013167
"""


""" Filtering: Functions which enable filtering of UK Biobank data.

    Currently includes (Oct 17):
        
        -Filter_by_multiple
        -code2word
        -get_matched_sample (WIP)
    


"""

import pandas as pd
import numpy as np
import time
import sys
import re

def cleanup(out_df,subset=None):
    """ Drop all nan rows, columns and duplicates"""
     
    if out_df is None:
        print("Dataframe is empty")
    elif len(out_df)<1:
        out_df=None
        print("Dataframe is empty")
    else:    
        #out_df.dropna(axis=0, how='all',inplace=True, subset=subset)# drop if all columns in row are nan
        out_df.dropna(axis=1, how='all',inplace=True)# drop if all rows in  column are nan
        out_df.drop_duplicates(inplace=True)#drop duplicate rows
    
    return out_df



def convert_list(i):
    """convert strings to lists"""
    ls=[]
    if type(i)==str:
        ls.append(i)
        o=ls[:]
    else:
        o=i[:]
    
    return o
    

def code2word(ukbc, df=None):    
    """  Converts numerical values in dataframe to text based upon UK biobank coding """
    
    if df is not None: 
        
        #dataframe to be returned
        out_df=df.copy()
       
        #Converting medication coding     
        med_cols=out_df.filter(regex='Treatment/medication code').columns.tolist()#coding columns..
        
        #If medication code columns exist, then continue
        if len(med_cols)>0:
            codes_dict=ukbc.MedicationCodes.to_dict()['meaning']
            for col in med_cols:
                out_df[col].replace(codes_dict, inplace=True)
                
        
        #Converting illness coding 
        illness_cols=[]
        
        illness_cols.extend(out_df.filter(regex='Non-cancer illness code, self-reported').columns.tolist())
    
        
        #If illness code columns exist, then continue
        if len(illness_cols)>0:
            codes_dict=ukbc.IllnessCodes.to_dict()['meaning']
            codes_dict = {int(k):v for k,v in codes_dict.items()}#converting keys to int
            for col in illness_cols:
                out_df[col].replace(codes_dict, inplace=True)
               
        cancer_cols=[]
        cancer_cols.extend(out_df.filter(regex='Cancer code, self-reported').columns.tolist())
        
        #If cancer code columns exist, then continue
        if len(cancer_cols)>0:
            codes_dict=ukbc.CancerCodes.to_dict()['meaning']
            codes_dict = {int(k):v for k,v in codes_dict.items()}#converting keys to int
            for col in cancer_cols:
                out_df[col].replace(codes_dict, inplace=True)
                
                
        #TODO: continue to implement other types of coding (see UK biobank showcase)...    
        
        #e.g.1 ethnic background.
        #e.g. 2	Job SOC coding (data coding 2) (req download of coding file and assignment to ukbc object...)
    return out_df



def select_by_illness(ukbc, in_df=None, illness=None, visit=None, instance=None):    
    """  Returns a dataframe containing subjects with given string of list of illnesses
         NOTE: If a list [A,B,C] is supplied, then an instance is treated as if A OR B OR C is present """

    
    #If string given then convert to list
    illness=convert_list(illness)

    
    ill_codes=[]
    cancer_codes=[]
    for i in illness:        
        #Gather illness code(s) codes must be list of int
        x=ukbc.IllnessCodes[ukbc.IllnessCodes==i]#illness codes
        x.dropna(inplace=True)   
        
        y=ukbc.CancerCodes[ukbc.CancerCodes==i]#cancer codes
        y.dropna(inplace=True)
        
        if len(x)<0 and len(y)<0:        
            raise Exception('Error: cannot find the illness: {0}. Please ensure that you are using medications exactly as specified in ''IllnessCodes or CancerCodes'''.format(i))
        
        #TODO: Currently this function will treat illnessess & cancer which share the same code as the same
        #How to overcome, include 'Cancer' flag' in function
        elif len(x)>0:
            ill_codes.append(int(x.index.tolist()[0]))
        else:
            cancer_codes.append(int(y.index.tolist()[0]))            
        
       
    illness_df=ukbc.extract_many_vars(keywords=['Cancer code, self-reported','Non-cancer illness code, self-reported'],visit=visit,instance=instance)
    
    #selecting only illness columns
    cancer_cols_of_interest=illness_df.filter(regex='Cancer code, self-reported').columns.tolist()
    illness_cols_of_interest=illness_df.filter(regex='Non-cancer illness code, self-reported').columns.tolist()
    
    
    #If the code is contained within df then append to out_df...
    include_rows=[]
    
    for c in ill_codes:        
            #Is code in dataframe?
            bool_df=illness_df[illness_cols_of_interest]==c        
            #If any element in a row is true, then include this row          
            inc=bool_df[bool_df.any(axis=1)].index.tolist()  
            include_rows.extend(inc)
            
    for c in cancer_codes:        
            #Is code in dataframe?
            bool_df=illness_df[cancer_cols_of_interest]==c        
            #If any element in a row is true, then include this row          
            inc=bool_df[bool_df.any(axis=1)].index.tolist()  
            include_rows.extend(inc)
            
    
    #Append included rows
    out_df=illness_df.loc[include_rows,:]   
    
    cols_of_interest2=[]
    cols_of_interest2.extend(out_df.filter(regex='Cancer code, self-reported').columns.tolist())
    cols_of_interest2.extend(out_df.filter(regex='Non-cancer illness code, self-reported').columns.tolist())
    
    #merge incoming dataframe
    if in_df is not None:
        cols_to_use=in_df.columns.difference(out_df.columns).tolist()
        cols_to_use.append('eid')
        out_df = out_df.merge(in_df[cols_to_use],on='eid',how='inner')
    
    out_df=cleanup(out_df,subset=cols_of_interest2)    
    
    
    return out_df


def select_by_illness_free(ukbc, in_df=None, illness=None, visit=None, instance=None):    
    """  Returns a dataframe containing subjects with no record of a given list of medications
    NOTE: If a list [A,B,C] is supplied, then an instance is treated as if A OR B OR C is present """
    
    #If string given then convert to list
    illness=convert_list(illness)
    
    
    ill_codes=[]
    cancer_codes=[]
    for i in illness:        
        #Gather illness code(s) codes must be list of int
        x=ukbc.IllnessCodes[ukbc.IllnessCodes==i]#illness codes
        x.dropna(inplace=True)   
        
        y=ukbc.CancerCodes[ukbc.CancerCodes==i]#cancer codes
        y.dropna(inplace=True)
        
        if len(x)<0 and len(y)<0:        
            raise Exception('Error: cannot find the illness: {0}. Please ensure that you are using medications exactly as specified in ''IllnessCodes or CancerCodes'''.format(i))
            
        elif len(x)>0:
            ill_codes.append(int(x.index.tolist()[0]))
        else:
            cancer_codes.append(int(y.index.tolist()[0]))     
    
    
    illness_df=ukbc.extract_many_vars(keywords=['Cancer code, self-reported','Non-cancer illness code, self-reported'],visit=visit,instance=instance)
    
    #selecting only illness columns
    cols_of_interest=[]
    cols_of_interest.extend(illness_df.filter(regex='Cancer code, self-reported').columns.tolist())
    cols_of_interest.extend(illness_df.filter(regex='Non-cancer illness code, self-reported').columns.tolist())
    
    cancer_cols_of_interest=illness_df.filter(regex='Cancer code, self-reported').columns.tolist()
    illness_cols_of_interest=illness_df.filter(regex='Non-cancer illness code, self-reported').columns.tolist()
    
    
    #If the code is contained within df then append to out_df...
    dont_include_rows=[]
    
    for c in ill_codes:        
            #Is code in dataframe?
            bool_df=illness_df[illness_cols_of_interest]==c        
            #If any element in a row is true, then include this row          
            dont_inc=bool_df[bool_df.any(axis=1)].index.tolist()  
            dont_include_rows.extend(dont_inc)
            
    for c in cancer_codes:        
            #Is code in dataframe?
            bool_df=illness_df[cancer_cols_of_interest]==c        
            #If any element in a row is true, then include this row          
            dont_inc=bool_df[bool_df.any(axis=1)].index.tolist()  
            dont_include_rows.extend(dont_inc)
            
                
    #Append included rows
    out_df=illness_df.drop(dont_include_rows)
    
    
    cols_of_interest2=[]
    cols_of_interest2.extend(out_df.filter(regex='Cancer code, self-reported').columns.tolist())
    cols_of_interest2.extend(out_df.filter(regex='Non-cancer illness code, self-reported').columns.tolist())
        
    #merge incoming dataframe
    if in_df is not None:
        
        #finding column which are present in in_df but not out_df, merging with out_df
        cols_to_use=in_df.columns.difference(out_df.columns).tolist()
        cols_to_use.append('eid')
        out_df = out_df.merge(in_df[cols_to_use],on='eid',how='inner')
        
    
    out_df=cleanup(out_df,subset=cols_of_interest2)
    
    return out_df


def select_by_medication(ukbc, in_df=None, medication=None, visit=None, instance=None):    
    """  Returns a dataframe containing subjects with given string of list of medications """
    
    #If string given then convert to list
    medication=convert_list(medication)
    
    #Gather medication code(s) codes must be list of int
    codes=[]
    for i in medication:        
        x=ukbc.MedicationCodes[ukbc.MedicationCodes==i]
        x.dropna(inplace=True)
        if len(x)<1:
            raise Exception('Error: cannot find the medication {0}. Please ensure that you are using medications exactly as specified in ''MedicationCodes'''.format(i))
        else:
            codes.append(int(x.index.tolist()[0]))
    
    
    medication_df=ukbc.extract_many_vars(keywords=['Treatment/medication code'],visit=visit,instance=instance)
    
    #selecting only illness columns -ugly workaround (basically we want to avoid including the demographics columns here (which are returned by the 
    #above function by default. If an add_demographics() function is implemented then demographics=False can be implemeted above to circumvent this))
    cols_of_interest=[]
    cols_of_interest.extend(medication_df.filter(regex='Treatment/medication code').columns.tolist())
    
    #If the code is contained within df then append to out_df...
    include_rows=[]
    
    for c in codes:        
        #Is code in dataframe?
        bool_df=medication_df[cols_of_interest]==c        
        #If any element in a row is true, then include this row          
        inc=bool_df[bool_df.any(axis=1)].index.tolist()  
        include_rows.extend(inc)
    
    #Append included rows
    out_df=medication_df.loc[include_rows,:]
            
    cols_of_interest2=out_df.filter(regex='Treatment/medication code').columns.tolist()     
    
    #merge incoming dataframe
    if in_df is not None:
        cols_to_use=in_df.columns.difference(out_df.columns).tolist()
        cols_to_use.append('eid')
        out_df = out_df.merge(in_df[cols_to_use],on='eid',how='inner')
    
    
    out_df=cleanup(out_df,subset=cols_of_interest2)

    return out_df



def select_by_medication_free(ukbc, in_df=None, medication=None, visit=None, instance=None):    
    """  Returns a dataframe containing subjects with no record of a given list of medications 
         NOTE: If a list [A,B,C] is supplied, then an instance is treated as if A OR B OR C is present """
    
    #If string given then convert to list
    medication=convert_list(medication)

    
    
    codes=[]
    for i in medication:        
        #Gather medication code(s) codes must be list of int
        x=ukbc.MedicationCodes[ukbc.MedicationCodes==i]
        x.dropna(inplace=True)
        if len(x)<1:
            raise Exception('Error: cannot find that medication: {0}. Please ensure that you are using medications exactly as specified in ''MedicationCodes'''.format(i))
        else:
            codes.append(int(x.index.tolist()[0]))
    
    
    medication_df=ukbc.extract_many_vars(keywords=['Treatment/medication code'],visit=visit,instance=instance)
    
    #selecting only illness columns -ugly workaround (basically we want to avoid including the demographics columns here (which are returned by the 
    #above function by default. If an add_demographics() function is implemented then demographics=False can be implemeted above to circumvent this))
    cols_of_interest=[]
    cols_of_interest.extend(medication_df.filter(regex='Treatment/medication code').columns.tolist())
    
    
    dont_include_rows=[]
    for c in codes:        
        #Is code in dataframe?
        bool_df=medication_df[cols_of_interest]==c
        
        #If any element in a row is true, then DONT include this row
        dont_inc=bool_df[bool_df.any(axis=1)].index.tolist()  
        
        dont_include_rows.extend(dont_inc)
    
    #Append included rows
    out_df=medication_df.drop(dont_include_rows)
    
    
    cols_of_interest2=out_df.filter(regex='Treatment/medication code').columns.tolist()  
        
    #merge incoming dataframe
    if in_df is not None:
        
        #finding column which are present in in_df but not out_df, merging with out_df
        cols_to_use=in_df.columns.difference(out_df.columns).tolist()
        cols_to_use.append('eid')
        out_df = out_df.merge(in_df[cols_to_use],on='eid',how='inner')
        
    
    out_df=cleanup(out_df,subset=cols_of_interest2)
    
    return out_df








def select_by_medications(ukbc, in_df=None, on_medication=None, off_medication=None, visit=None, instance=None):    
    """  Returns a dataframe containing subjects with given string of list of medications 
        NOTE: If a list [A,B,C] is supplied, then an instance is treated as if A OR B OR C is present """
    
    if on_medication is not None and off_medication is not None:        
        on_df=select_by_medication(ukbc=ukbc,in_df=in_df, medication=on_medication, visit=visit, instance=instance)
        off_df=select_by_medication_free(ukbc=ukbc,in_df=in_df, medication=off_medication, visit=visit, instance=instance)
        
        #Find common 'eids' between on and off dfs and merge
        #finding column which are present in in_df but not out_df, merging with out_df
        cols_to_use=on_df.columns.difference(off_df.columns).tolist()
        cols_to_use.append('eid')
        out_df = off_df.merge(on_df[cols_to_use],on='eid',how='inner')
    
    elif on_medication is not None and off_medication is None:
        out_df=select_by_medication(ukbc=ukbc,in_df=in_df, medication=on_medication, visit=visit, instance=instance)

    elif on_medication is None and off_medication is not None:
        out_df=select_by_medication_free(ukbc=ukbc,in_df=in_df, medication=off_medication, visit=visit, instance=instance)
    
    else:        
        ValueError('Error: you must specify either on_medication OR off_medication')
        out_df=None


    return out_df

def select_by_illnesses(ukbc, in_df=None, on_illness=None, off_illness=None, visit=None, instance=None):    
    """  Returns a dataframe containing subjects with given string of list of illnesses
    NOTE: If a list [A,B,C] is supplied, then an instance is treated as if A OR B OR C is present """
    
    if on_illness is not None and off_illness is not None:        
        on_df=select_by_illness(ukbc=ukbc,in_df=in_df, illness=on_illness, visit=visit, instance=instance)
        off_df=select_by_illness_free(ukbc=ukbc,in_df=in_df, illness=off_illness, visit=visit, instance=instance)
        
        #Find common 'eids' between on and off dfs and merge. Finding column which are present in in_df but not out_df, merging with out_df
        cols_to_use=on_df.columns.difference(off_df.columns).tolist()
        cols_to_use.append('eid')
        out_df = off_df.merge(on_df[cols_to_use],on='eid',how='inner')
    
    elif on_illness is not None and off_illness is None:
        out_df=select_by_illness(ukbc=ukbc,in_df=in_df, illness=on_illness, visit=visit, instance=instance)

    elif on_illness is None and off_illness is not None:
        out_df=select_by_illness_free(ukbc=ukbc,in_df=in_df, illness=off_illness, visit=visit, instance=instance)
    
    else:        
        ValueError('Error: you must specify either on_illness OR off_illness')
        out_df=None


    return out_df



#TODO insert 'in_df' functionality into here
def select_by_multiple(ukbc, on_med=None,off_med=None, on_illness=None, off_illness=None, visit=None, instance=None):    
    """  Returns a dataframe containing subjects with given illnesses and medications.
         NOTE: If a list [A,B,C] is supplied, then an instance is treated as if A OR B OR C is present """
    
    
    to_merge=[]#collecting df's to merge

    
    if on_med is not None and len(on_med)>0:
        on_med_df=select_by_medication(ukbc=ukbc, medication=on_med, visit=visit, instance=instance)
        to_merge.append(on_med_df)
        
    if off_med is not None and len(off_med)>0:
        off_med_df=select_by_medication_free(ukbc=ukbc,medication=off_med, visit=visit, instance=instance)
        to_merge.append(off_med_df)
        
    if on_illness is not None and len(on_illness)>0:
        on_ill_df=select_by_illness(ukbc=ukbc, illness=on_illness, visit=visit, instance=instance)
        to_merge.append(on_ill_df)
        
    if off_illness is not None and len(off_illness)>0:
        off_ill_df=select_by_illness_free(ukbc=ukbc,illness=off_illness, visit=visit, instance=instance)
        to_merge.append(off_ill_df)
    
    
    #if any dataframes in 'to_merge' list are empty then drop them
    temp=to_merge[:]
    to_merge=[]
    for i in temp:
        if i is not None:
            if len(i)>0:
                to_merge.append(i)
    

    #Merging dataframes in to_merge list. Must be a simpler, cleaner way. Currenlty deciding which columns to use is v.messy . . .
    
    #if only one input option
    if len(to_merge)==1:
        out_df=to_merge[0].copy()
    
    #if two options selected
    elif len(to_merge)==2:
        cols1=to_merge[1].columns.difference(to_merge[0].columns).tolist()
        cols1.append('eid')
        out_df=to_merge[0].merge(to_merge[1][cols1],on='eid',how='inner')
    
    elif len(to_merge)==3:
        cols1=to_merge[1].columns.difference(to_merge[0].columns).tolist()
        cols1.append('eid')
        cols2=to_merge[2].columns.difference(to_merge[1].columns).tolist()
        cols2.append('eid')
        
        out_df=to_merge[0].merge(to_merge[1][cols1],on='eid',how='inner').merge(to_merge[2][cols2],on='eid',how='inner')
    
    elif len(to_merge)==4:
        cols1=to_merge[1].columns.difference(to_merge[0].columns).tolist()
        cols1.append('eid')
        cols2=to_merge[2].columns.difference(to_merge[1].columns).tolist()
        cols2.append('eid')
        cols3=to_merge[3].columns.difference(to_merge[2].columns).tolist()
        cols3.append('eid')
        
        out_df=to_merge[0].merge(to_merge[1][cols1],on='eid',how='inner').merge(to_merge[2][cols2],on='eid',how='inner').merge(to_merge[3][cols3],on='eid',how='inner')
        
    else:
        out_df=None
        #no illness/medication options chosen or results found 

    out_df=cleanup(out_df)
    
    return out_df

 
def add_vars(ukbc, in_df=None, add_vars=None, visit=None, instance=None):
    """ Adds selected variables to the current dataframe """
    
    if in_df is None or add_vars is None:
        ValueError('Error: you have failed to provide in_df and/or add_vars')
        out_df=None
        
    #extract variables #deleted: (but we dont want demographics columns)
    variables_df=ukbc.extract_many_vars(keywords=add_vars, visit=visit, instance=instance, demographics=False)
    
    #extract rows based on eids from in_df and all columns (except eid)
    in_eids=in_df['eid'] # gather encoded subject IDs
    rows=variables_df['eid'].isin(in_eids)
    variables_df=variables_df.loc[rows,:]
    
    #select only columns unique to variables_df
    cols_to_use=variables_df.columns.difference(in_df.columns).tolist()
    cols_to_use.append('eid')
    
    #join dataframes (variables_df and in_df)
    out_df=in_df.merge(variables_df[cols_to_use],on='eid',how='inner')
         
    out_df=cleanup(out_df)
        
    return out_df




def get_illness_code(ukbc, text_in):
    """Returns illness code
     given text input"""
     
    codes_dict=ukbc.IllnessCodes
    code=codes_dict[codes_dict['meaning']==text_in].index.tolist()[0]

    return code

#TODO: add functions which add variables to a new 'addvariables' document
#Work in progress . . .
def initial_diagnosis(ukbc, in_df=None, illness=None, visit=None, instance=None):
    """ Adds a column labelling Year and Age of first diagnosis for selected illnesses.
        Illness is expected as text, e.g. 'depression', (not corresponding code)"""
    
    
    out_df=in_df.copy()
    
    #getting initial diagnosis year and age of participans
    for v in ['Year','Age of participant']:
    
        #If string given then convert to list
        illness=convert_list(illness)
    
        """find code (or string) in in_df"""
        
        #get non cancer illness columns
        cols=out_df.filter(regex='Non-cancer illness code, self-reported')
        cols=cols.columns.tolist()
        
        
        #1. check that interpolated diagnosis year column exists, if not then request it
        if len(out_df.filter(regex='Interpolated '+v+' when non-cancer illness first diagnosed').columns)<1:
            out_df=add_vars(ukbc, in_df=out_df, add_vars='Interpolated '+v+' when non-cancer illness first diagnosed')
        
    
    
        #for each illness identify column
        for i in illness:
            
                    
            #get code for illness
            illness_code=get_illness_code(ukbc,i)
                   
            #creating dict to store year of diagnosis variable
            var_name=i+'_'+v+'_first_diagnosed'
            res_dict={'eid':[],var_name:[]}
            
            #iterrate over each row in df
            for row in out_df.iterrows():
                            
                #get columns with matching code
                matching_columns=row[1][row[1]==illness_code].index.tolist()
                
                
                #TODO: #NOTE only one value for 'INterpolated year..' wil be generated. TODO: If two different values exist then the mean will be taken
                if len(matching_columns)>0:
                    
                    c=matching_columns[0]
                       
                    found=re.findall('(.*)_(\d+).(\d+)',c)
                    visit=found[0][1]
                    instance=found[0][2]
                    
                    #extract intial diagnosis year based upon year and instance
                    initial_diagnosis_year=row[1]['Interpolated '+v+' when non-cancer illness first diagnosed_'+str(visit)+'.'+str(instance)]
                    eid=row[1]['eid']
                    
                    #create variable
                    res_dict['eid'].append(eid)
                    res_dict[var_name].append(initial_diagnosis_year) 
                     
                        
            new_df=pd.DataFrame.from_dict(res_dict)
            
            #for each illness merge latest new_df with in_df on 'eid' 
            out_df=out_df.merge(new_df,on='eid',how='outer')
        
    out_df=cleanup(out_df)
        
    return out_df





#Work in progress . . .
def get_matched_sample(ukbc, to_match=None, off_illness=None, off_med=None, visit=None, num_samples=1):    
    """ This function aims to return a dataframe returning a matched sample according with
        same M/F and same age distribution and allows the user to specificy illnesses NOT
        to be contained within the sample
        
        The returned sample will differ each time as the sampling df is shuffled"""
    
    if visit is None:
        sys.exit('You must provide a visit so that the sample can be age matched for the target visit')
        

    
    
    #getting dataframe free from illness (to gather matched sample from)
    if off_illness is not None and off_med is not None:
        off_ill_df=select_by_illness_free(ukbc,illness=off_illness,visit=visit)
        off_med_df=select_by_medication_free(ukbc, medication=off_med, visit=visit)
        df=off_ill_df.merge(off_med_df, how='inner')
    elif off_illness is not None:
        df=select_by_illness_free(ukbc,illness=off_illness,visit=visit)
    elif off_med is not None:
        df=select_by_medication_free(ukbc, medication=off_med,visit=visit)
    else:
        df=ukbc.gather_related_vars()
        
    #for each sample  
    matched_samples=[]
    for sample in range(num_samples):
        
        #shuffling healthy df
        df=df.sample(frac=1)
        
        #df to store out matched sample
        out_df=pd.DataFrame()
        
        #Gathering M/F age information for current distribution
        currentSexAge=[]
        for row in to_match.iterrows():
            currentSexAge.append((row[1]["Age when attended assessment centre_"+str(visit)+".0"],row[1]["Sex_0.0"]))
            
        #could remove timeout
        timeout = time.time() + 60 #times out after 1 minute
    
    
        #gathering matched sample from 'df'
        covered_rows=[]
        
        #cycling through each requirement, e.g.30yrs Female...
        for targetSexAge in currentSexAge:
            
            moveOn=False
            
            
            if time.time()>timeout:
                sys.exit('Error: Couldn''t find a sample matching your AGE criteria')
        
    
            #checking each row in the ill/med free df
            for i,row in enumerate(df.iterrows()):
            
                
                #while a match has not been found
                if moveOn is False:
                
                    #if current row has not already been selected
                    if i not in covered_rows:
                        
                        #if current row matches requirements                    
                        if (row[1]["Age when attended assessment centre_"+str(visit)+".0"] == targetSexAge[0]) & (row[1]["Sex_0.0"] == targetSexAge[1]):
                            
                            #append row to out df
                            out_df=out_df.append(row[1])
                            
                            #make sure this row isn't re-used
                            covered_rows.append(i)
                
                            #Pass onto next target sexAge
                            moveOn=True

        matched_samples.append(out_df)
    
    
    return matched_samples