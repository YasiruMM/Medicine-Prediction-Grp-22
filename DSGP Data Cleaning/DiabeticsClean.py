import pandas as pd
import os
import re


root_folder = r"D:\IIT\2 Year\Diabetics"
categories = ['ALPHA GLUCO','SULFON','THIAZOL']

combined_data = pd.DataFrame()

def extract_dosage(Item_Name):

    match = re.search(r'(\d+(\.\d+)?MG)', str(Item_Name))
    if match:
        return match.group(0)
    return None


# Process each medicine category (subfolder)
for category in categories:
    # Construct the path to the subfolder
    category_folder = os.path.join(root_folder, category)

