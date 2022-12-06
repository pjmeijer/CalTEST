import novopy
import novopy.services.file_shares as file_shares
import json
import os
import pandas as pd
import fluent as fl

def check_min_vol(vol, min_vol):
    if vol<min_vol:
        return min_vol
    else:
        return vol
    
def initiate_dfs(result_df, results_to_fluent_df):

    # Initiate dfs
    result_df = pd.DataFrame(columns=['Dilution_ID','Name','Concentration','Source_name','Source_ID','Dilution_factor','Volume_total','Vol_previous_dil','Vol_diluent','Adjusted','Number_of_sets_adjusted','Legacy'])
    add_row(result_df)

    results_to_fluent_df = result_df[['Dilution_ID','Name','Concentration','Source_name','Source_ID','Vol_previous_dil','Vol_diluent','Adjusted','Number_of_sets_adjusted','Legacy']]

    
    
def add_row(_df):
    _df.loc[_df.shape[0]] = [None, None, None,None, None, None,None, None, None,None, None, None]
    
def save(result_df, dil_setup):
    fluent_csv = fl.create_csv(dil_setup, result_df)
    print('Saving')
    #print(fluent_csv)
    #print(result_df)
    #print(dil_setup.initials + '_' + dil_setup.eln_num + '.csv')
   
    try:
        local_dir = './'
        file_name = dil_setup.initials + '_' + dil_setup.eln_num + '.csv'
        remote_dir = 'Instruments/CalibratorApp/DataForTECANFluent/'
        #print(local_dir)
        #print(file_name)
        #print(remote_dir)
        #fluent
        with open(file_name, "w") as outfile:
            outfile.write(fluent_csv)
            print(fluent_csv)
        client = file_shares.SC19Client(share='dept0244')
        print('client.isdir(remote_dir)' + client.isdir(remote_dir))
        client.upload(local_dir + file_name, remote_dir +'/' + file_name)

        #lean up local dir
        os.remove(local_dir + file_name)

        #database
        merged_json = {}
        merged_json["Dilution_setup"] = dil_setup.__dict__
        merged_json["Dilution_scheme"] = result_df.to_dict(orient="index")
        #print(merged_json)
        local_dir='./'
        file_name = dil_setup.initials + '_' + dil_setup.eln_num + '.json'
        remote_dir='Instruments/CalibratorApp/DataForTECANFluent/'+ dil_setup.initials
        with open(file_name+'', "w") as outfile:
            #outfile.write(json.dumps(dil_setup.__dict__,indent=4, ensure_ascii=True))
            outfile.write(json.dumps(merged_json,indent=4, ensure_ascii=True))
        client = file_shares.SC19Client(share='dept0244')
        client.upload(local_dir + file_name, remote_dir +'/' + file_name)
        print(local_dir)
        print(file_name)
        print(remote_dir)
        #lean up local dir
        os.remove(local_dir + file_name)
        return True
    except:
        print('Error when trying to save. Filename: ' + file_name + ' Local: ' + local_dir + ' Remote: ' + remote_dir )
        return False
        

def import_file(dil_setup,file):
    
    json_import = json.loads(file.read())

    #for k in json_import.keys():
     #   setattr(dil_setup, k, json_import[k])
     #   print(str(k) + '... ' + str(json_import[k]))
    #print('.................')
    #print('.................')
    #print('.................')
    iterate(json_import,dil_setup)    
    #print('..................dil_setup.__dict__')
    #print(dil_setup.__dict__)
    #database
    #merged_json = {}
    #merged_json["Dilution setup"] = dil_setup.__dict__
    #merged_json["Dilution scheme"] = result_df.to_dict(orient="index")
    #local_dir='./'
    #file_name='demofile.json'
    #remote_dir='Instruments/CalibratorApp/DataForTECANFluent/PJHM/'
    

    
def clear_form(st):
    for key in range(1,2,1):
        st.session_state[key] = 0
        st.write(st.session_state[key])

def iterate(json, dil_setup): 
    for key, value in json.items():
        #print('key {!r} -> value {!r}'.format(key, value))
        setattr(dil_setup, key, value)
        if isinstance(value, dict):
            #print('.................')
            setattr(dil_setup, key, value)
            iterate(value, dil_setup) 
            continue
    