def create_csv(_dil_setup, _results_df):
    text = _dil_setup.assay_name + '\r'
    text += _dil_setup.analogue + '\r'
    text += _dil_setup.eln_num + '\r'
    text += _dil_setup.diluent_species + '\r'
    text += ';' + '\r'
    
    text += 'Comments:'
    for s in _dil_setup.comment:
        text += str(s) + ' '
    text += '\r'
    text += 'pmol/L' + '\r'
    text += 'Stock Concentration;Stock units;Number of sets;Set volume;Number of pre-dil buffer;Number of pre-dil Matrix;Number of Calibrators;Calibrators in buffer;Pre-wet;Rinse' + '\r'    
    text += str(_dil_setup.stock_concentration) + ';' + 'µmol/L' + ';' + str(_dil_setup.aliquot_num)+';'+str(_dil_setup.aliquot_vol) + ';' + str(_dil_setup.predilPlasma_num) + ';' + str(_dil_setup.predilBuffer_num)+ ';'+ str(_dil_setup.cals_num) +';'+ str(_dil_setup.calsInBuffer) + ';'+ 'False'  + ';' + 'True' + '\r'
    text += _results_df.to_csv(header=True,sep=';', encoding='utf-8', index=False)
    #print(text)
    return text
    
    
    