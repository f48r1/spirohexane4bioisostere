# Directory description

- **raw/** – Contains unprocessed initial data of organic cores represented as SMILES paired with name and label.
- **MM/** – Contains files and results from the molecular mechanics (MM) initialization step, such as conformer generation and energy minimization.
- **computed/** – Contains processed or finalized computational results derived from molecular characterization, PCA and clustering.
- **DFT/** – Stores ORCA inputs/outputs and electronic structure data files generated during density functional theory calculations. Each subfolder is for a single molecular structure named by a numerical code (see [encoded_list.csv](encoded_list.csv) file) rather than by the original SMILES notation of the molecule. This encoding scheme was introduced to facilitate automated execution and systematic organization of DFT computations across the entire dataset.
- **encoded_list.csv** – Lookup table mapping each molecular SMILES string to its corresponding numerical code used as folder names.
    > For completeness, the encoding procedure assigns a unique integer to each SMILES string by converting the SMILES into UTF-8 bytes and interpreting those bytes as a big-endian integer. The resulting integer, represented as a string, serves as the folder name corresponding to that molecular structure. Relative function is stored in [src/paths.py](../../src/paths.py#L25) file.
- **opt_mol/** – Stores optimized molecular geometries obtained after quantum-mechanical geometry optimization procedures.
