# -*- coding: utf-8 -*-
"""
GUI setup for UKBCrunch

Requires 'appJar'
"""
import os
import UKBcrunch as UKBC 

from appJar import gui
from ukbc_functions import Filtering #Import filtering module:  Filtering requires the user to pass the ukbc object, followed by any desired options"""
from gui_functions.gui_functions import setup_loading_screen, setup_add_vars, setup_select_multiple
from gui_functions.gui_functions import get_illness_med_selections, updateMeter





#colour scheme info
ukb_bg="#deeaec"
ukb_fg="#005f6f"
title_size=16
font="Arial"
ukb_logo=os.path.dirname(__file__)+'/images/ukb_logo.gif'

def press(button):  

    if button == "Cancel":
        app.stop()
        
    elif button=="get_files":
        
        if len(app.getEntry("html_file"))>0:
            html_file=app.getEntry("html_file")
            csv_file=app.getEntry("csv_file")
            app.setStatusbar("Loading biobank data, please wait...", 0)
             
            app.infoBox("loading_ukbc",message="Loading UKBC object, will take ~3minutes")
            
            global ukbc #defining ukbc as global object
            ukbc=UKBC.UKBcrunch(html_file=html_file,csv_file=csv_file)
                
            app.infoBox("loaded_ukbc",message="Succesfully loaded UKBC object!")
            
            app.clearStatusbar(field=0)
            
            #This should remove file entry but doesn't - Q submitted to appJAr github
            app.removeFileEntry("html_file")
            app.removeFileEntry("csv_file")

            app.removeButton("get_files")
     
            #currently only provides functionality for 'select_multiple; filter
            setup_select_multiple(app=app,ukbc=ukbc,press=press)

             
    #Implemeting add vars option
    elif button=="Add Variables":        
        setup_add_vars(app=app, ukbc=ukbc)
    
      
    #display selections    
    elif button=="View Selection":
        
        #getting illness/med selections ..
        on_illness, off_illness, on_med, off_med = get_illness_med_selections(app)
        med_illness_msg=("Here are your current selections: \n\n ON ILLNESS: {0} \n OFF ILLNESS: {1} \n ON MED: {2} \n OFF MED {3} \n").format(on_illness,off_illness,on_med,off_med)
        
        #getting var selections..
        try:
            var_selections=app.getListBox("var_options")
        except:
            message=med_illness_msg+"No additional variables selected. Go back and choose 'Add Variables'"
        else:
            message=med_illness_msg+("Variables: {0}").format(var_selections)
            
        
        app.infoBox("selections",message)
        
    #generating df
    elif button=="Submit":
        
        #define output location
        fname=app.saveBox(title="Save file as ...", fileExt=None) 
        
        if len(fname)<1:
            fname='no_filename_given'
        
        #getting illness/med selections ..
        on_illness, off_illness, on_med, off_med = get_illness_med_selections(app)

        #getting var selections..
        try:
            var_selections=app.getListBox("var_options")
        except:
            var_selections=None
       
        
        #Creating excel file
        app.infoBox("loading_df","Your excel file is being created. You will be notified when it's ready (~3mins)")
        df=Filtering.select_by_multiple(ukbc, on_med=on_med, off_med=off_med, on_illness=on_illness, off_illness=off_illness)#creating df

        #if no illness or meds chosen then generate a full dataframe
        if all(len(v)<1 for v in [on_illness, off_illness, on_med, off_med]):
            df=ukbc.extract_many_vars()


        if var_selections is not None and df is not None:
            df=Filtering.add_vars(ukbc, in_df=df, add_vars=var_selections)#adding vars
        
        if df is not None:            
        #saving list of bulk fields requested.
            if len(ukbc.bulk_request)>0:
                outtxt = open(fname+'_bulk_fields.txt', 'w')
                for subj in df['eid']:
                    for item in ukbc.bulk_request:
                        outtxt.write("%s %s\n" % (subj, item))
                outtxt.close()
            
            df_decoded=Filtering.code2word(ukbc, df=df)
            df.to_excel(fname+'.xls')
            df_decoded.to_excel(fname+'_decoded.xls')
            app.infoBox("df","Your output was saved to: "+fname+".xls")
            
        else:
            app.infoBox("no_df","Your query returned no results")
            



"""      Setting up gui interface         """
# create a GUI variable called app
app = gui("UKBcrunch")
app.setLogLevel("CRITICAL")#prevents warning outputs
#app.setIcon(ukb_logo) # doesnt work atm
app.addImage("LOGO",ukb_logo)
app.setBg(ukb_bg)
app.setFont(title_size,font)



"""If UKBC object doesnt exist then must be loaded """
try:
    ukbc   
except:
    setup_loading_screen(app=app)
    app.addButton("get_files", press)


else:    
    app.addLabel("ukbc_found", "ukbc object detected, no need to reload!",colspan=2)
    #currently only provides functionality for 'select_multiple; filter
    setup_select_multiple(app=app, ukbc=ukbc, press=press)

     


# start the GUI
def start():       
    app.go()


