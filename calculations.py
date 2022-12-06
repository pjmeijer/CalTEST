import streamlit as st
import pandas as pd
import numpy as np
import utility
import fluent as fl
import model

#@st.cache(allow_output_mutation=True)
def create_dilutions(result_df, dil_setup):
    
    # Calculate pre-dilution
    stock = dil_setup.target_concentration
    if dil_setup.vol_pip_min and dil_setup.get_total_vol() and dil_setup.dil_factor_max and dil_setup.stock_concentration and dil_setup.target_concentration:
        if dil_setup.get_total_vol()/dil_setup.vol_pip_min <= dil_setup.dil_factor_max:
            dil_setup.dil_factor_max = total_pre_dil_vol/dil_setup.vol_pip_min
            st.write('The effective maximum dilution factor due to volume is: '+str(dil_setup.dil_factor_max))
    vol_ratio = dil_setup.get_total_vol()/dil_setup.vol_pip_min
    stock = dil_setup.stock_concentration*1000000
    dil_ratio = stock/dil_setup.target_concentration

    n=1
    while dil_ratio**(1/n) > dil_setup.dil_factor_max:
        n+=1
    
    if dil_setup.diluent_type == 'Plasma':
        dil_setup.predilPlasma_num = n
        dil_setup.predilBuffer_num = 0
        dil_setup.calsInBuffer = True
       
    if dil_setup.diluent_type == 'Buffer':
        dil_setup.predilBuffer_num = n
        dil_setup.predilPlasma_num = 0
        dil_setup.calsInBuffer = False
     
    result_df['Name'][0]='Stock'
    result_df['Dilution_ID'][0] = 1
    result_df['Dilution_factor'][0] = 1
    result_df['Concentration'][0] = stock

    index = 0

    # Calculate pre-dil concentrations
    for x in range(n):
        index = index +  1
        utility.add_row(result_df)
        dilution_factor = dil_ratio**(1/n)
        stock = stock/dilution_factor
        result_df['Dilution_factor'][index] = dilution_factor
        result_df['Concentration'][index] = stock
        result_df['Dilution_ID'][index] = index + 1
        result_df['Source_name'][index] = result_df['Name'][index-1]
        result_df['Source_ID'][index] = result_df['Dilution_ID'][index-1]
        if index != n:
            result_df['Name'][index] = 'Predil ' + str(x+1)
        else:
            result_df['Name'][index] = dil_setup.get_calsQCType_in_singular() + ' 1'

    # Calculate minimum needed vol for pre-dil used for first calibrator
    result_df['Vol_previous_dil'][index] = dil_setup.get_total_vol() / result_df['Dilution_factor'][index]
    result_df['Vol_diluent'][index] = dil_setup.get_total_vol() - result_df['Vol_previous_dil'][index]
    result_df['Volume_total'][index] = dil_setup.get_total_vol()

    for z in range(n-1, 0, -1):
        result_df['Vol_previous_dil'][z] = utility.check_min_vol(result_df['Vol_previous_dil'][z+1]/result_df['Dilution_factor'][z], dil_setup.vol_pip_min)
        if result_df['Vol_previous_dil'][z] * result_df['Dilution_factor'][z] > dil_setup.pre_dil_deadvol:
            result_df['Vol_diluent'][z] = result_df['Vol_previous_dil'][z] * (result_df['Dilution_factor'][z]-1)
            result_df['Volume_total'][z] = result_df['Vol_previous_dil'][z] * result_df['Dilution_factor'][z]
        else:
            factor_needed_vol = dil_setup.pre_dil_deadvol / result_df['Vol_previous_dil'][z] * result_df['Dilution_factor'][z]
            result_df['Vol_previous_dil'][z] = result_df['Vol_previous_dil'][z] * factor_needed_vol
            result_df['Vol_diluent'][z] = dil_setup.pre_dil_deadvol * factor_needed_vol-result_df['Vol_previous_dil'][z]       
            result_df['Volume_total'][z] = result_df['Vol_previous_dil'][z] + result_df['Vol_diluent'][z]


    # set volume needed from original stock
    result_df['Volume_total'][0] = result_df['Vol_previous_dil'][1] + dil_setup.pre_dil_deadvol

    # last dilution in pre-dilution is the first calibrator/qc. 6 dilutions are performed and a blank is added after that.
    wstock = dil_setup.target_concentration
    for y in range(dil_setup.cals_num-1):
        index += 1
        utility.add_row(result_df)
        wstock = wstock/dil_setup.cal_dil_factor
        result_df['Dilution_factor'][index] = dil_setup.cal_dil_factor
        result_df['Concentration'][index] = wstock
        result_df['Dilution_ID'][index] = index
        result_df['Vol_previous_dil'][index] = dil_setup.get_total_vol()/dil_setup.cal_dil_factor
        result_df['Vol_diluent'][index] = dil_setup.get_total_vol()-dil_setup.get_total_vol()/dil_setup.cal_dil_factor
        result_df['Name'][index] = dil_setup.get_calsQCType_in_singular() + ' ' + str(y+1)
        result_df['Volume_total'][index] = dil_setup.get_total_vol()
        result_df['Source_ID'][index] = result_df['Dilution_ID'][index-1]
        result_df['Source_name'][index] = result_df['Name'][index-1]

    if dil_setup.calsQCType == "Calibrators":
        #add blank
        index += 1
        utility.add_row(result_df)
        result_df['Dilution_factor'][index] = None
        result_df['Concentration'][index] = 0
        result_df['Dilution_ID'][index] = index
        result_df['Vol_previous_dil'][index] = 0
        result_df['Vol_diluent'][index] = dil_setup.get_total_vol()
        result_df['Name'][index] = 'Blank'
        result_df['Volume_total'][index] = dil_setup.get_total_vol()
        result_df['Source_ID'][index] = -1
        result_df['Source_name'][index] = None

    if dil_setup.get_total_vol()>dil_setup.max_vial_vol:
        st.warning('Max volume for 4.5ml vials is '+ str(dil_setup.max_vial_vol)+'µl. Suggested max number of aliquots with current volume: ' + str(np.round(dil_setup.max_vial_vol/dil_setup.aliquot_vol)),icon="⚠️")

    return result_df

    



    
