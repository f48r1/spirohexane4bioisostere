import os
_current_path = os.path.dirname(os.path.abspath(__file__))

if __name__=="__main__":
    from script_utils import append_parent, change2parent
    change2parent(_current_path)
else:
    from .script_utils import append_parent

append_parent(_current_path)

# NOTE Change mechanisms or features here to generate 3D conformer.
def smTo3D(sm):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    m = Chem.MolFromSmiles(sm)
    hm = Chem.AddHs(m)
    AllChem.EmbedMolecule(hm,useExpTorsionAnglePrefs=True ,useBasicKnowledge=True)
    AllChem.UFFOptimizeMolecule(hm)
    return hm

def main(args):
    import pandas as pd

    from rdkit import Chem

    smiles_path = os.path.join(args.dir_data, args.dir_structures, args.dir_raw, args.file_name)
    
    smiles_df = pd.read_csv(smiles_path)

    dir_out = os.path.join(args.dir_data, args.dir_structures, args.dir_mm)

    os.makedirs(dir_out, exist_ok=True)

    for smiles in smiles_df.smiles:
        if os.path.exists(os.path.join(dir_out,f"{smiles}.mol")):
            continue
        
        tmpMol = smTo3D (smiles)
        
        Chem.MolToMolFile(tmpMol, os.path.join(dir_out,f"{smiles}.mol"))

if __name__ == '__main__':

    from src.paths import DIR_DATA, DIR_RAW, DIR_MM, DIR_CORES

    import argparse
    parser = argparse.ArgumentParser(description='Generate conformer by MM optimization. Specify directories, if required')

    parser.add_argument('--dir_data', type=str, default=DIR_DATA, help='Directory of full data files')
    parser.add_argument('--dir_structures', type=str, default=DIR_CORES, help='Directory where full data file are stored. It is referred to cores or structures involved for reactions')
    parser.add_argument('--dir_raw', type=str, default=DIR_RAW, help='Directory where raw data file are stored')
    parser.add_argument('--dir_mm', type=str, default=DIR_MM, help='Storing directory of .mol molecules after optimization')
    parser.add_argument('--file_name', type=str, default='cores.csv', help='File where smiles (column header brings same name) are listed')
    
    args,unk = parser.parse_known_args()
    if unk:
        print("unknown arguments passed ! i.e.,", *unk)

    exit = main(args)


