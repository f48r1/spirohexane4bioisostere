#!/bin/bash

# Tasks and directories
tasks=("cores" "reactions")
dirs=("raw" "DFT" "opt_mol" "MM")

base_dir="data"

CURRENT_DIR=$(pwd)

for task in "${tasks[@]}"; do

    task_path="${base_dir}/${task}"

    if [ ! -d "$task_path" ]; then
        echo "Skipping missing task directory: $task_path"
        continue
    fi

    # --- ZIP ONLY FILES INSIDE THE TASK ROOT DIRECTORY ---
    zip_name="${task}_info.zip"
    echo "  Creating $zip_name (files only)"

    # Go into the task directory
    cd "$task_path" || exit 1

    # Zip only regular files
    find . -maxdepth 1 -type f -print0 | xargs -0 zip -j "${CURRENT_DIR}/${zip_name}"

    cd "${CURRENT_DIR}" || exit 1

done

# --- ZIP EACH SUBDIRECTORY ---
for task in "${tasks[@]}"; do
    for dir in "${dirs[@]}"; do

        dir_path="${base_dir}/${task}/${dir}"
        if [[ "$task" == "reactions" && "$dir" == "DFT" ]]; then
            special_dir="method=m062x|basis=def2-svp|freq=True|solvent=thf|tightscf=True"
            dir_path="${dir_path}/${special_dir}"
        fi

        if [ ! -d "$dir_path" ]; then
            echo "Skipping missing directory: ${dir_path}"
            continue
        else
            zip_name="${task}_${dir}.zip"
            echo "  Creating $zip_name"

            cd "$dir_path" || exit 1
            zip -r "${CURRENT_DIR}/${zip_name}" .
        fi

        cd "${CURRENT_DIR}" || exit 1

    done
done

echo "All zipping operations completed."
