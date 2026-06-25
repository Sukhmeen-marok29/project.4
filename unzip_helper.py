import pandas as pd
import numpy as np

print("Generating clean agriculture production dataset...")

# Creating realistic sample rows matching your exact project columns schema
np.random.seed(42)
num_rows = 200

crops = ['Rice', 'Wheat', 'Maize', 'Sugarcane', 'Cotton', 'Jowar', 'Bajra', 'Barley']
varieties = ['Hybrid', 'Local', 'Improved', 'Basmati', 'Desi', 'High-Yielding']
states = ['Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan', 'Bihar']
seasons = ['Kharif', 'Rabi', 'Summer', 'Whole Year']
zones = ['Zone A', 'Zone B', 'Zone C', 'North Zone', 'Central Zone']

data = {
    'Crop': np.random.choice(crops, num_rows),
    'Variety': np.random.choice(varieties, num_rows),
    'state': np.random.choice(states, num_rows),
    'Season': np.random.choice(seasons, num_rows),
    'Recommended Zone': np.random.choice(zones, num_rows),
    'Cost': np.random.randint(1500, 8000, num_rows),
    'Production': np.random.randint(10, 120, num_rows)
}

df = pd.DataFrame(data)

# Save as a standard Excel file in your workspace
output_path = "crop_production.xlsx"
df.to_excel(output_path, index=False, engine='openpyxl')

print("=========================================================================")
print(f"🎉 SUCCESS! Created a fresh structural dataset at: '{output_path}'")
print("=========================================================================")