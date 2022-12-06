import streamlit as st
import pandas as pd
import numpy as np
import utility as utility
import fluent as fl
import model as model
import calculations as calc
import json
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import novopy.services.file_shares as file_shares
import databaseHandler
import page as p


dil_setup = model.Dilution()
import_file = {}

# # --- Initialising SessionState ---
if "load_state" not in st.session_state:
    st.session_state.load_state = False
    
if "clear_state" not in st.session_state:
    st.session_state.clear_state = False
    
if "import_state" not in st.session_state:
    st.session_state.import_state = False
    
if "on_changeButtons" not in st.session_state:
    st.session_state.on_changeButtons = False

def change():
    st.session_state.on_changeButtons = True
    
if "import_file" not in st.session_state:
    st.session_state.import_file = ""
else:
    import_file = st.session_state.import_file


if "dil_setup" not in st.session_state:
    st.session_state.dil_setup = "dil_setup"
    dil_setup.dil_factor_max = 25
    dil_setup.cal_dil_factor = float(3)
    dil_setup.aliquot_vol = 300
    dil_setup.aliquot_num = int(12)
    dil_setup.calsQCType = 'Calibrators'
    dil_setup.stock_concentration = float(0)
    dil_setup.target_concentration = float(0)
else:
    if st.session_state.clear_state:
        dil_setup.clear()
        dil_setup.dil_factor_max = 25
        dil_setup.cal_dil_factor = float(3)
        dil_setup.aliquot_vol = 300
        dil_setup.aliquot_num = int(12)
        dil_setup.calsQCType = 'Calibrators'
        dil_setup.stock_concentration = float(0)
        dil_setup.target_concentration = float(0)
        st.session_state.clear_state = False
    else:
        dil_setup = st.session_state.dil_setup


file_database_path ='Instruments/CalibratorApp/<Your initials>'
dil_setup.pre_dil_deadvol = 150
dil_setup.vol_pip_min = 20
dil_setup.max_vial_vol = 4000
fluent_csv = None
result_df = None
results_to_fluent_df = None
loadButton = None

result_df = pd.DataFrame(columns=['Dilution_ID','Name','Concentration','Source_name','Source_ID','Dilution_factor','Volume_total','Vol_previous_dil','Vol_diluent','Adjusted','Number_of_sets_adjusted','Legacy'])
utility.add_row(result_df)

results_to_fluent_df = result_df[['Dilution_ID','Name','Concentration','Source_name','Source_ID','Vol_previous_dil','Vol_diluent','Adjusted','Number_of_sets_adjusted','Legacy']]

st.set_page_config(page_title='RBA - Calibrator app helper', layout="wide")
st.title('CalibratorApp')

# Info input
col1, col2, col3, col4, col5= st.columns(5, gap="small")   
col1.markdown('**Info**')
dil_setup.eln_num = col2.text_input(label='ELN_number (File name)',
                                    value = dil_setup.eln_num,
                                    key = "eln_num",
                                    on_change = change)
dil_setup.analogue = col4.text_input(label='Analogue name',
                                     value = dil_setup.analogue,
                                     key = "analogue",
                                     on_change = change)
dil_setup.assay_name = col3.text_input(label='Assay name',
                                       value = dil_setup.assay_name,
                                       key = 'assay_name',
                                       on_change = change)
dil_setup.initials = col5.text_input(label='Initials',
                                     value = dil_setup.initials,
                                     key = "initials",
                                     on_change = change)


# Type input
col211, col221, col231, col241, col215= st.columns(5, gap="small")
col211.markdown('**Type**')
#dil_setup.diltype = col231.selectbox('Dilution type',('Serial','Non-serial'))
dil_setup.calsQCType = col221.selectbox('CAL/QC',('Calibrators','QC'),
                                        key = 'calsQCType',
                                        on_change = change)

if dil_setup.calsQCType =='Calibrators':
    calqcValue = 8
else:
    calqcValue = 3
       
dil_setup.cals_num = col231.number_input('Number of ' + dil_setup.calsQCType,
                                         calqcValue,
                                         on_change = change)

# Pre-dilution input
col11, col12, col13, col14, col15= st.columns(5, gap="small")
col11.markdown('**Pre-Dilution**') 
dil_setup.stock_concentration = col12.number_input('Stock conc. [µM]',
                                                   value = dil_setup.stock_concentration,
                                                   key = 'stock_concentration',
                                                   on_change = change)
dil_setup.dil_factor_max = col13.number_input('Maximum dilution',
                                              value = dil_setup.dil_factor_max,
                                              key = 'dil_factor_max',
                                              on_change = change)
dil_setup.diluent_type = col14.selectbox("Diluent",("Buffer","Plasma"),
                                         key = 'diluent_type',
                                         on_change = change)

if dil_setup.diluent_type == "Plasma":
    dil_setup.diluent_species = col15.text_input("Plasma species",
                                                 value = dil_setup.diluent_species,
                                                 key='diluent_species',
                                                 on_change = change)

# Dilution input
col21, col22, col23, col24, col25= st.columns(5, gap="small")    
col21.markdown('**Dilution**')
dil_setup.target_concentration = col22.number_input('Start conc. [pM]',
                                                    value = dil_setup.target_concentration,
                                                    key='target_concentration', 
                                                    on_change = change)
dil_setup.cal_dil_factor = col23.number_input('Serial dilution factor',
                                              value = dil_setup.cal_dil_factor,
                                              key='cal_dil_factor',
                                              on_change = change)
dil_setup.aliquot_vol = col24.number_input('Volume/aliquot [µL]',
                                           value = dil_setup.aliquot_vol,
                                           key='aliquot_vol',
                                           on_change = change)
dil_setup.aliquot_num = col25.number_input('Number of aliquots',
                                           value = dil_setup.aliquot_num,
                                           key='aliquot_num',
                                           on_change = change)

# Comment area
col31, col32 = st.columns([1,4],gap='small')
col31.write('**Comments**')
dil_setup.comment = col32.text_area(' ')

# Buttons
col41, col42, col43, col44, col45 = st.columns((5), gap="small")                           
calculateButton = col41.button('Update/Calculate')
importButton = col42.button('Open file import', key = "import_button")
closeimportButton = col43.button('Close file import')
saveButton = col44.button('Save to file')
clearButton = col45.button('Clear')

# Clear
if clearButton:
    st.session_state.load_state = False
    st.session_state.clear_state = True
    dil_setup.clear()
    #st.session_state.import_state = ""
    #st.experimental_rerun()
    st.session_state.import_state = False
    st.experimental_rerun()

# Import file
col51, col52 = st.columns([1,4],gap='small')   
if importButton or st.session_state.import_state:
    if not closeimportButton:
        st.session_state.import_state = True

        loadButton = col51.button('Load file')
        import_file = col52.file_uploader('Choose a .json file from Z:\\' + file_database_path.replace('/','\\')
                                          + ' and the click on Load', accept_multiple_files=False, type =['.json'])
    else:
        st.session_state.import_state = False
        
if import_file and st.session_state.import_state:
    dil_setup.clear()
    utility.import_file(dil_setup, import_file)
    st.session_state.dil_setup = dil_setup

# Debug 
#st.write(str(st.session_state.on_changeButtons) + ' '+ str(calculateButton) +' ' +str(saveButton) +' ' +str(clearButton) +' '+ str(st.session_state.load_state)+ ' '+ str(st.session_state.import_state))
if  import_file and not calculateButton and st.session_state.on_changeButtons and st.session_state.import_state:
    col52.warning('If you want to edit, first remove file from donwload dialog by clicking the cross. Then click on Update/Calculation.',icon="⚠️")
    
# Calculate and create data
if (calculateButton or loadButton or saveButton or clearButton or st.session_state.load_state) and (dil_setup.stock_concentration != 0 and dil_setup.target_concentration != 0):
    p.update_calculate_page(st, result_df, dil_setup, results_to_fluent_df, fluent_csv)
    st.session_state.load_state = True

# Create files and save


if saveButton and dil_setup.initials and dil_setup.eln_num:
    
    if utility.save(result_df, dil_setup):
        col52.success('Files created and saved.', icon="✅")
    else:
        col52.warning('Cannot save file! Is sc19/Z-drive online?',icon="⚠️")
        
    database ={}
    databaseHandler.connect(database)
    merged_json = {}
    merged_json_new  = {}
    merged_json["Dilution_Setup"] = dil_setup.__dict__
    merged_json["Dilution_Scheme"] = result_df.to_dict(orient="index")
    #merged_json["CalQC_Record"] = merged_json

    #print("Json.................")
    #print(merged_json)
    #print("Dump.................")
    #print(json.dumps(merged_json))
    #databaseHandler.write_to_database(database,merged_json)
    
if saveButton and (not dil_setup.initials or not dil_setup.eln_num):
    col52.warning('Cannot save file! Missing info: ELN number and/or Initials',icon="⚠️")


#Set state
st.session_state.dil_setup = dil_setup 
st.session_state.import_file = import_file
st.session_state.on_changeButtons = False
