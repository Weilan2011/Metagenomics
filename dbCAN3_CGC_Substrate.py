import pandas as pd
import os

# Define the directory where the files are stored
directory = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_shotgun_dbCAN3_contigs/Contigs_PUL_Substrates/CGC_substrate_majority_voting'

# List all files in the directory that end with '.out'
file_names = [f for f in os.listdir(directory) if f.endswith('.out')]

# Display the files
print(file_names)

# Create an empty DataFrame again for the adjusted data
adjusted_data = pd.DataFrame()

# Re-process each file with the correct sample ID extraction
for file_name in file_names:
    file_path = os.path.join(directory, file_name)
    # Read the file
    data = pd.read_csv(file_path, sep="\t", usecols=["Substrate", "Abundance(sum of CGC)"])
    # Correctly extract the sample ID from the filename
    sample_id = file_name.split("_CGC_substrate_majority_voting.out")[0]  # Gets the part before '_CGC_substrate_majority_voting.out'
    data.rename(columns={"Abundance(sum of CGC)": sample_id}, inplace=True)
    # Merge the data into the adjusted DataFrame
    if adjusted_data.empty:
        adjusted_data = data.set_index("Substrate")
    else:
        adjusted_data = adjusted_data.join(data.set_index("Substrate"), how="outer")

# Fill NaN values with 0 (assuming no abundance as 0)
adjusted_data.fillna(0, inplace=True)

# Reset index to turn 'Family' back into a column
adjusted_data.reset_index(inplace=True)

# Define the new path for saving the output file
output_directory = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_shotgun_dbCAN3_contigs/Contigs_PUL_Substrates'
adjusted_output_path = os.path.join(output_directory, "Combined_CGC_substrate_abund.csv")

# Save the adjusted combined data to the new CSV file path
adjusted_data.to_csv(adjusted_output_path, index=False)

# Show the adjusted DataFrame structure
adjusted_data.head()
