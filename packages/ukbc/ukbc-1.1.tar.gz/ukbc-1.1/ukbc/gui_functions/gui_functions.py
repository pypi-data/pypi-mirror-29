# -*- coding: utf-8 -*-
"""
GUI functions for ukbc
"""
#colour scheme info
ukb_bg="#deeaec"
ukb_fg="#005f6f"
title_size=16
font="Arial"



def setup_loading_screen(app=None):
    app.addFileEntry("html_file")
    app.updateEntryDefault("html_file", "enter html file")
    app.addFileEntry("csv_file")
    app.updateEntryDefault("csv_file", "enter csv file")
    app.addStatusbar(fields=1)
    app.setStatusbar("No files entered", 0)
    


def setup_add_vars(app=None, ukbc=None):
    
    #show subwindow if already created, else build it
    try:
        app.showSubWindow("Adding Variables")
    except:
        #setting up subwindow
        app.startSubWindow("Adding Variables", modal=True)
        app.setStretch("both")
        app.setSticky("nesw")
        
        app.setBg(ukb_bg)
        app.setFont(title_size,font)
        app.addLabel("addVarTitle", "Adding Variables")
        app.setLabelBg("addVarTitle",ukb_bg)
        app.setLabelFg("addVarTitle", ukb_fg)
        
        #TODO: this information could be showed as a tabbed frame subdivided in to UKB showcase categories for ease of selection (see bottom of page 'TAB' for example code)
        # May need to parse the data showcase link into UKBC object...
        
        all_vars=ukbc.Vars[:]
        all_vars.sort()

        app.addListBox("var_options",all_vars)

        app.setListBoxMulti("var_options")
        app.setListBoxGroup("var_options")

         
        app.showSubWindow("Adding Variables")
    
    
#setting up select_multiple filtering option boxes 
def setup_select_multiple(app=None, ukbc=None, press=None):
    
    
    
    for opt in ["on_illness","off_illness"]:
        app.addLabel("Select "+opt,opt)
        i=ukbc.IllnessCodes['meaning'].tolist()
        i.sort()
        app.addListBox(opt,i)
        app.setListBoxMulti(opt)
        app.setListBoxGroup(opt)

        
    for opt in ["on_med","off_med"]:
        app.addLabel("Select "+opt,opt)
        m=ukbc.MedicationCodes['meaning'].tolist()
        m.sort()
        app.addListBox(opt, m)
        app.setListBoxMulti(opt)
        app.setListBoxGroup(opt)

                 
    #Add options to allocate excel output filename . . 
    app.addButtons(names=["Submit","Add Variables", "View Selection", "Cancel"], funcs=press)
        
        
def get_illness_med_selections(app=None):
        on_illness = app.getListBox("on_illness")
        off_illness = app.getListBox("off_illness")
        on_med = app.getListBox("on_med")
        off_med = app.getListBox("off_med")
        
        return on_illness, off_illness, on_med, off_med
    
    
def updateMeter(app=None, percentComplete=None):
    app.setMeter("progress", percentComplete)
    

