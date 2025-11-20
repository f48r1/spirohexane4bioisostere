import os
_current_path = os.path.dirname(os.path.abspath(__file__))

if __name__=="__main__":
    from script_utils import append_parent, change2parent
    change2parent(_current_path)
else:
    from .script_utils import append_parent

append_parent(_current_path)

def main(args):
    from src.dataloader import Dataloader
    from src.descriptors import dipoleMoment, desc_2d, compute_3Dscore

    import pandas as pd
    from rdkit.Chem import Descriptors3D

    dataloader = Dataloader(args.dir_data, args.dir_cores, args.dir_raw, args.dir_opt, args.dir_comp)
    dataloader.load_cores()
    dataloader.load_dft_mols()

    df = dataloader.cores
    mols = dataloader.dft_mols

    df.drop(columns=['name','label'], inplace=True)

    for nameDesc, fncDesc in desc_2d.items():
        df[nameDesc] = mols.apply(fncDesc)

    dir_dft = os.path.join(args.dir_data, args.dir_cores, args.dir_dft)
    df["dipole"]=df["smiles"].apply(dipoleMoment, dft_dir = dir_dft)
    df["3Dscore"]=mols.apply(compute_3Dscore)
    df_3d = pd.DataFrame(mols.apply(Descriptors3D.CalcMolDescriptors3D).tolist())

    df = pd.concat(
        [df, df_3d],
        axis=1
    )

    dir_file = os.path.join(args.dir_data, args.dir_cores, args.dir_comp)
    os.makedirs(dir_file, exist_ok=True)
    
    path_file = os.path.join(dir_file, 'descripted.csv')
    df.to_csv(path_file, index=False)

if __name__=="__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Molecular characterization. Specify directories, if required')

    from src.paths import DIR_DATA, DIR_RAW, DIR_COMP, DIR_OPT, DIR_CORES, DIR_DFT

    parser.add_argument('--dir_data', type=str, default=DIR_DATA, help='Directory of full data files')
    parser.add_argument('--dir_raw', type=str, default=DIR_RAW, help='Directory of raw data files')
    parser.add_argument('--dir_cores', type=str, default=DIR_CORES, help='Directory where full core data file are stored')
    parser.add_argument('--dir_comp', type=str, default=DIR_COMP, help='Soring directory for computed features')
    parser.add_argument('--dir_dft', type=str, default =DIR_DFT, help='Storing directory of DFT calculations')
    parser.add_argument('--dir_opt', type=str, default=DIR_OPT, help='Storing directory of .mol molecules after optimization')
    
    args,unk = parser.parse_known_args()
    if unk:
        print("unknown arguments passed ! i.e.,", *unk)
    
    exit = main(args)