#!/bin/bash

# Set input and output directories
Prokka_DIR="$HOME/Desktop/Raf_shotgun_desktop/Raf_dbCAN3"
OUTPUT_DIR="$HOME/Desktop/Raf_shotgun_desktop/Raf_dbCAN3_out"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through all .faa files in the input directory
for file in "$Prokka_DIR"/*.faa; do
    # Extract file name without extension
    filename=$(basename -- "$file")
    filename_no_ext="${filename%.*}"
    
    # Run dbCAN annotation
    echo "Running dbCAN annotation for $filename_no_ext..."
    run_dbcan "$file" protein --dbcan_thread 8 --tf_cpu 8 --stp_cpu 8 -c "$Prokka_DIR/$filename_no_ext.gff" --cgc_substrate --hmm_cpu 8 --out_dir "$OUTPUT_DIR/$filename_no_ext" --dia_cpu 8
done

echo "All dbCAN3 annotation are completed."