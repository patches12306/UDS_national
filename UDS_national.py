import pandas as pd
import itertools
import numpy as np


def clean_UDS(UDS_awardee_path,UDS_awardee_lookalike_path):
	lookalike_awardees =pd.ExcelFile(UDS_awardee_lookalike_path)
	awardees =pd.ExcelFile(UDS_awardee_lookalike_path)

	awardees_arr = []
	lookalike_awardees_arr = []
	for sheet in awardees.sheet_names:
	   
	    df= pd.read_excel(UDS_awardee_path, sheet_name= sheet)
	    awardees_arr.append(df)
	    
	for kheet in lookalike_awardees.sheet_names:
	  
	    df= pd.read_excel(UDS_awardee_lookalike_path, sheet_name= kheet)
	    lookalike_awardees_arr.append(df)

	combined_arr = []
	for i in range(5):
	    combined_arr.append((awardees_arr[i],lookalike_awardees_arr[i]))

	full_arr = []
	for i in combined_arr:
	    full_arr.append(pd.concat(i))


	real_uds_2021 = []
	for df in full_arr:
	    df= df.drop(columns=['Health Center Name', 'City'])
	    UDS_2021_arr = []
	    for i in df['State'].unique():
	        place_holder_df = df.copy()
	        state_df = df.copy().loc[df.copy()['State']==i]
	        place_holder_df['State'] = i
	        #print(place_holder_df)
	        #print(place_holder_df["State"])
	        for col in state_df.columns[1:]:
	    #         if (state_df[col].str.contains('-') == True:
	            state_df[col] =state_df[col].replace('-',0)
	        
	            try:        
	                if pd.to_numeric(state_df[col],errors='coerce').mean() >1.0:
	                    #rint(place_holder_df["Total Patients"])
	                    place_holder_df[col] = pd.to_numeric(state_df[col],errors='coerce').sum()
	                    #print(place_holder_df["Total Patients"])
	                    
	                elif pd.to_numeric(state_df[col],errors='coerce').mean() <1.0:
	                    place_holder_df[col] = pd.to_numeric(state_df[col],errors='coerce').mean()
	                    #print(place_holder_df[col])
	            except:
	                pass

	        UDS_2021_arr.append(place_holder_df.iloc[:1])
	    sheet_df = pd.concat(UDS_2021_arr)
	    real_uds_2021.append(sheet_df)

	UDS_2021_df = real_uds_2021[0]
	for i in real_uds_2021[1:]:
	    UDS_2021_df = UDS_2021_df.merge(i, how='outer', on='State')

	return UDS_2021_df

