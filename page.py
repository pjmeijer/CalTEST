import streamlit as st
import pandas as pd
import numpy as np
import utility as utility
import fluent as fl
import model as model
import calculations as calc
import json

def update_calculate_page(st, result_df, dil_setup, results_to_fluent_df, fluent_csv) :
    st.session_state.load_state = True
  
    calc.create_dilutions(result_df, dil_setup)
    
    
    # CSS to inject contained in a string
    hide_dataframe_row_index = """
                <style>
                .row_heading.level0 {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
    
    # Display results
    st.table(result_df[['Name', 'Concentration','Dilution_factor','Volume_total', 'Vol_previous_dil', 'Vol_diluent']])
    
    # legacy variables added - not used
    result_df['Adjusted'] = False
    result_df['Legacy'] = False
    result_df['Number of sets adjusted'] = 0
   
    