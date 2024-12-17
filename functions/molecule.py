import requests
import urllib.parse
import json
import pandas as pd
import numpy as np

def iupac_to_smiles(iupac_name: str) -> str:
    # URL encode the IUPAC name to handle special characters
    encoded_name = urllib.parse.quote(iupac_name)
    
    # PubChem PUG REST API URL
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded_name}/json'
    
    # Send the GET request to the API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Check if the response contains the expected compound data
        if 'PC_Compounds' in data and len(data['PC_Compounds']) > 0:
            compound = data['PC_Compounds'][0]

            # Extract the SMILES string from the compound data
            if 'props' in compound:
                for prop in compound['props']:
                    if prop.get('urn', {}).get('label') == 'SMILES':
                        return prop['value']['sval']
            
            return f"SMILES not found for molecule '{iupac_name}'."
        else:
            return None
    else:
        return f"Error fetching data from PubChem (status code: {response.status_code})."



def post_hmdb_id(smiles: str):
    url = "http://35.184.189.38/api/hmdb/metabolites/search/"

    headers = {
        "accept": "application/json",
        "Authorization": "Api-Key XnkVcFeM.IFjz7rShQJoW46DVeCKxwZz1c05BV7ir",
        "Content-Type": "application/json",
        "X-CSRFTOKEN": "optional_token_here"
    }

    data = {
        "smiles": f"{smiles}"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response = response.json()

        with open("test.json", "w") as f:
            json.dump(response, f, indent=4)

        return response[0]["hmdb_id"]
    
    else:
        print(response.status_code)
        return "No Data"
    
def change_spectrum_into_df(spectrum: list, offset: float):
    df = pd.DataFrame(spectrum)

    # Finds doublets, triplets etc and separates the grouped peaks
    ppm_counts = df['ppm'].value_counts()
    
    for ppm, count in ppm_counts.items():
        if count > 1:  # If duplicates exist
            # Indices of rows with this ppm value
            indices = df[df['ppm'] == ppm].index
            
            # Generate new ppm values, centered on the original value
            center = ppm
            adjustments = [
                center + offset * (i - (count - 1) / 2)  # Offset from center
                for i in range(count)
            ]
            
            # Update the DataFrame
            df.loc[indices, 'ppm'] = adjustments

    return df
    

def get_predicted_peaks(hmdb_id: str, nmr_type: str, offset: float):
    url = f"http://35.184.189.38//api/hmdb/metabolites/{hmdb_id}/spectra/"

    headers = {
        "accept": "application/json",
        "Authorization": "Api-Key XnkVcFeM.IFjz7rShQJoW46DVeCKxwZz1c05BV7ir",
        "Content-Type": "application/json",
        "X-CSRFTOKEN": "optional_token_here"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response = response.json()


        nmr_data = response["nmr"]


        # nmr_samples = []
        for nmr_sample in nmr_data:
            if nmr_sample["nucleus"] == nmr_type:
                return change_spectrum_into_df(nmr_sample["peaks"], offset=offset)
            else:
                return None
    else:
        return None
            

def full_predicted_spectrum(df, start, end, step=0.001):
    """
    Adds missing ppm values between `start` and `end` (with a step of `step`) 
    to the DataFrame, setting their intensity to 0.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame with 'ppm' and 'intensity' columns.
        start (float): Start of the ppm range.
        end (float): End of the ppm range.
        step (float): Step size for generating ppm values.
    
    Returns:
        pd.DataFrame: Modified DataFrame with missing ppm values added.
    """
    # Generate all possible ppm values in the range
    full_ppm_range = np.arange(start, end, step)
    
    # Extract existing ppm values
    existing_ppms = set(df['ppm'])
    
    # Identify missing ppm values
    missing_ppms = [ppm for ppm in full_ppm_range if ppm not in existing_ppms]
    
    # Create a DataFrame for the missing ppm values
    missing_data = pd.DataFrame({'ppm': missing_ppms, 'intensity': 0})
    
    # Append the missing data to the original DataFrame
    combined_df = pd.concat([df, missing_data], ignore_index=True)
    
    # Sort by ppm
    combined_df = combined_df.sort_values(by='ppm').reset_index(drop=True)
    
    return combined_df