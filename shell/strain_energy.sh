#!/bin/bash

# Path for CSV file
CSV_FILE="data/cores/raw/cores.csv"
SMILES_COLUMN_NAME="smiles"

# Column index of from name (SMILES)
HEADER=$(head -n 1 "$CSV_FILE")
IFS=',' read -ra COLUMNS <<< "$HEADER"

SMILES_INDEX=-1
for i in "${!COLUMNS[@]}"; do
    if [[ "${COLUMNS[$i]}" == "$SMILES_COLUMN_NAME" ]]; then
        SMILES_INDEX=$i
        break
    fi
done

if [[ $SMILES_INDEX -eq -1 ]]; then
    echo "Column '$SMILES_COLUMN_NAME' didnt find within CSV file."
    exit 1
fi

# Read and store SMILES in indexed array
mapfile -t SMILES_LIST < <(tail -n +2 "$CSV_FILE" | awk -F',' -v idx=$((SMILES_INDEX + 1)) '{print $idx}')

# For loop
for SMILES in "${SMILES_LIST[@]}"; do
    echo "--------------------------------------"
    echo "Starting for: $SMILES"
    python scripts/strain_energy.py --smiles "$SMILES"
    echo "$SMILES process completed"
    echo "--------------------------------------"

done
