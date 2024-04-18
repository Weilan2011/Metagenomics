import os
import pandas as pd

# Directory containing all the files - updated to the correct path
directory_path = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_dbCAN3_Substrate/substrate'

# Initialize an empty DataFrame to collect all data
columns = ['dbCAN-PUL substrate', 'PULID', 'Sample ID', '#cgcid', 'dbCAN-sub substrate', 'bitscore']
collected_data = pd.DataFrame(columns=columns)

# Process each file in the directory that ends with '_substrate.out'
for filename in os.listdir(directory_path):
    if filename.endswith("_substrate.out"):  # Correct filename check
        # Extract sample ID from filename
        sample_id = filename.split('_dbCAN_substrate_substrate.out')[0]
        
        # Read the current file
        file_path = os.path.join(directory_path, filename)
        try:
            data = pd.read_csv(file_path, sep='\t', usecols=['#cgcid', 'PULID', 'dbCAN-PUL substrate', 'dbCAN-sub substrate', 'bitscore'])
            # Add sample ID to the data
            data['Sample ID'] = sample_id
            
            # Append to the collected data
            collected_data = pd.concat([collected_data, data], ignore_index=True)
            print(f"Processed file: {filename} with {len(data)} rows.")
        except Exception as e:
            print(f"Failed to process file: {filename}. Error: {e}")

if collected_data.empty:
    print("No data has been collected. Check the file patterns and paths.")
else:
    # Group by 'dbCAN-PUL substrate' and 'PULID' and format the output
    formatted_data = []
    for (substrate, pulid), group in collected_data.groupby(['dbCAN-PUL substrate', 'PULID']):
        # Append first row with dbCAN-PUL substrate and PULID
        formatted_data.append({'dbCAN-PUL substrate': substrate, 'PULID': pulid})
        # Append details for each sample in the group
        for _, row in group.iterrows():
            formatted_data.append({
                'Sample ID': row['Sample ID'],
                '#cgcid': row['#cgcid'],
                'dbCAN-sub substrate': row['dbCAN-sub substrate'],
                'bitscore': row['bitscore']
            })

    # Convert the list of dictionaries to a DataFrame
    formatted_df = pd.DataFrame(formatted_data)

    # Save to Excel file
    output_file = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_dbCAN3_Substrate/substrate/Formatted_Substrate_Data.xlsx'
    formatted_df.to_excel(output_file, index=False, header=True)
    print("Data has been formatted and saved to Excel.")
