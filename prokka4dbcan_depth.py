import csv
import os

def extract_locus_tag_details(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()

        unique_entries = set()
        current_feature = None
        last_positions = None

        for line in lines:
            if line.startswith('>Feature'):
                current_feature = line.split(' ')[1].strip().replace('Feature:', '')
            elif '\t' in line and not line.startswith('\t\t\t'):
                last_positions = line.strip().split('\t')[:2]
            elif '\tlocus_tag' in line:
                locus_tag = line.split('\t')[-1].strip()
                if last_positions and len(last_positions) == 2:
                    entry = (locus_tag, current_feature, last_positions[0], last_positions[1])
                    unique_entries.add(entry)

        sorted_details = sorted(unique_entries, key=lambda x: x[0])

        numbered_details = []
        feature_counter = {}
        for locus_tag, feature, start, end in sorted_details:
            if feature not in feature_counter:
                feature_counter[feature] = 0
            else:
                feature_counter[feature] += 1
            modified_feature = f"{feature}_{feature_counter[feature]}"
            numbered_details.append((locus_tag, modified_feature, start, end))

        with open(output_file_path, 'w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['Locus Tag', 'Feature', 'Start Position', 'End Position'])
            tsv_writer.writerows(numbered_details)

        return numbered_details  # Return the processed list of details

    except Exception as e:
        print(f"Error processing file {input_file_path}: {e}")
        return []

def update_depth_file(depth_file_path, mapping, output_file_path):
    replaced_count = 0
    try:
        with open(depth_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            for line in infile:
                parts = line.strip().split()
                if parts[0] in mapping:
                    parts[0] = mapping[parts[0]]
                    replaced_count += 1
                outfile.write('\t'.join(parts) + '\n')
    except Exception as e:
        print(f"Error updating depth file {depth_file_path}: {e}")
    return replaced_count

def process_batch(tbl_directory, depth_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file in os.listdir(tbl_directory):
        if file.endswith(".tbl"):
            sample_id = file.replace("_contigs.fasta.tbl", "")
            tbl_file_path = os.path.join(tbl_directory, file)
            tsv_file_path = os.path.join(output_directory, f"{sample_id}_locustag.tsv")
            depth_file_path = os.path.join(depth_directory, f"{sample_id}.depth.txt")
            updated_depth_file_path = os.path.join(output_directory, f"{sample_id}.updated_depth.txt")

            # Process TBL to TSV and get the details
            numbered_details = extract_locus_tag_details(tbl_file_path, tsv_file_path)
            unique_count = len(numbered_details)
            print(f"Processed {sample_id} with {unique_count} unique locus tags.")

            # Update depth file
            if numbered_details and os.path.exists(depth_file_path):
                mapping = {entry[0]: entry[1] for entry in numbered_details}
                replaced_count = update_depth_file(depth_file_path, mapping, updated_depth_file_path)
                print(f"Updated depth file for {sample_id} with {replaced_count} replacements")


# Example usage
tbl_directory = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_shotgun_Prokka/Raf_shotgun_Prokka_Contigs/all_tbl_files'
depth_directory = '/media/weilan/easystore/Raf-Shotgun/2_trimed_reads_alignment/Prokka_ffn_BAMs'
output_directory = '/media/weilan/easystore/Raf-Shotgun/2_trimed_reads_alignment/Prokka_ffn_BAMs'
process_batch(tbl_directory, depth_directory, output_directory)
