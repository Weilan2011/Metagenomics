import os
import pandas as pd

# Define the list of enzymes to search for
enzymes = ["AA4_e0", "CBM34_e9", "CBM77_e0", "CBM9_e20", "CE12_e14", "CE19_e1", "CE2_e6",
           "CE20_e20", "CE4_e150", "CE4_e225", "CE4_e320", "CE4_e338", "CE7_e2", "CE8_e50",
           "CE8_e51", "GH1_e0", "GH1_e13", "GH10_e78", "GH105_e7", "GH109_e6", "GH140_e0",
           "GH143_e0", "GH154_e5", "GH16_e336", "GH2_e13", "GH23_e992", "GH25_e123", "GH25_e157",
           "GH26_e35", "GH3_e130", "GH32_e91", "GH39_e74", "GH43_e105", "GH43_e171", "GH43_e264",
           "GH5_e304", "GH53_e14", "GH53_e16", "GH73_e116", "GH77_e18", "GT1_e246", "GT113_e5",
           "GT14_e13", "GT28_e115", "GT4_e1113", "GT4_e2108", "GT4_e2729", "GT4_e45", "GT51_e21",
           "PL9_e8"]

# Directory containing the files
input_directory = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_shotgun_dbCAN3_contigs/Contigs_PUL_Substrates/CGC_abund'  
output_directory = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_shotgun_dbCAN3_contigs/Contigs_PUL_Substrates/CGC_abund' 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Create subdirectories for filtered outputs and summaries
filtered_output_directory = os.path.join(output_directory, 'filtered_outputs')
summary_output_directory = os.path.join(output_directory, 'summaries')

if not os.path.exists(filtered_output_directory):
    os.makedirs(filtered_output_directory)

if not os.path.exists(summary_output_directory):
    os.makedirs(summary_output_directory)

# Function to process each file
def process_file(file_path, filename):
    # Read the data from the file
    data = pd.read_csv(file_path, delimiter='\t')
    
    # Check if 'Fams' column exists
    if 'Fams' not in data.columns:
        print(f"Column 'Fams' not found in file: {file_path}")
        return None
    
    # Filter the rows where the 'Fams' column contains any of the enzymes
    filtered_data = data[data['Fams'].apply(lambda fam: any(enzyme in fam for enzyme in enzymes))]
    
    # Add the query enzymes as the first column
    filtered_data.insert(0, 'Query_Enzymes', [", ".join([enzyme for enzyme in enzymes if enzyme in fam]) for fam in filtered_data['Fams']])
    
    # Save the filtered data to a new CSV file
    filtered_output_path = os.path.join(filtered_output_directory, f'filtered_{filename}')
    filtered_data.to_csv(filtered_output_path, index=False)
    
    # Calculate the sum of Abundance(mean) for each Query_Enzymes
    summary = filtered_data.groupby('Query_Enzymes').agg({'Abundance(mean)': 'sum'}).reset_index()
    summary.columns = ['Query_Enzymes', filename.split('_CGC_abund.out')[0]]
    
    # Save the summary data to a new CSV file
    summary_output_path = os.path.join(summary_output_directory, f'summary_{filename}')
    summary.to_csv(summary_output_path, index=False)
    
    return summary

# Process each file in the directory
all_summaries = []

for filename in os.listdir(input_directory):
    if filename.endswith('_CGC_abund.out'):
        file_path = os.path.join(input_directory, filename)
        
        # Process the file
        summary = process_file(file_path, filename)
        
        if summary is not None:
            all_summaries.append(summary)

# Combine all summaries into one DataFrame by merging on Query_Enzymes
combined_summary = all_summaries[0]
for summary in all_summaries[1:]:
    combined_summary = pd.merge(combined_summary, summary, on='Query_Enzymes', how='outer')

# Fill any NaN values with 0
combined_summary = combined_summary.fillna(0)

# Save the final combined summary to a new CSV file
combined_output_file_path = os.path.join(output_directory, 'combined_summary.csv')
combined_summary.to_csv(combined_output_file_path, index=False)

print("Processing complete.")


