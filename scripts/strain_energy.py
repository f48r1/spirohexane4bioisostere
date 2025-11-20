_PATH_ORCA_CMD = '/opt/orca/orca_2aim' # TODO set this path to orca_2aim cmd carefully :P
_PATH_MULTIWFN_CMD = 'Multiwfn' # TODO set this path to Multiwfn cmd carefully :P

import os
_current_path = os.path.dirname(os.path.abspath(__file__))

if __name__=="__main__":
    from script_utils import append_parent, change2parent
    change2parent(_current_path)
else:
    from .script_utils import append_parent

append_parent(_current_path)


CPS_COMMANDS="""
2
2
3
4
5
-4
4
q
q
"""

LAPLACIAN_COMMANDS="""
1
{x},{y},{z}
1
q
q
"""

def main(args):

    import pandas as pd
    import re
    import subprocess

    from src.paths import smi2safepath

    path_dft = os.path.join(args.dir_dft,smi2safepath(args.smiles))
    path_gbw = os.path.join(path_dft, 'file')
    subprocess.run([_PATH_ORCA_CMD, path_gbw],
        stdout = subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        # cwd=path_dft+'/'
    )

    subprocess.run([_PATH_MULTIWFN_CMD, 'file.wfn'],
        text=True,
        input=CPS_COMMANDS, # NOTE nuclear positions are reported as bohr units
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        cwd=path_dft + '/',
    )
    
    CPs_df = pd.read_csv(
        os.path.join(path_dft, 'CPs.txt'),
        skiprows=1,
        sep='\s+',
        index_col=0,
        header=None,
        names=['x','y','z','type'],
    )

    CPs_df = CPs_df.query('type == 3')
    if CPs_df.empty:
        print('Critial points (+3,1) not recognized for SMILES:',args.smiles)
        return 0
    
    compiler = re.compile(r'Lagrangian kinetic energy G\(r\):\s+([0-9]+\.[0-9]+E?[+-]?[0-9]+)')
    all_Gr = []

    for idx,row in CPs_df.iterrows():
        x,y,z = str(row.x), str(row.y), str(row.z)

        output = subprocess.run([_PATH_MULTIWFN_CMD, 'file.wfn'],
            text=True,
            input=LAPLACIAN_COMMANDS.format(x=x,y=y,z=z),
            capture_output = True,
            cwd=path_dft + '/',
        )
        
        match = compiler.findall(output.stdout)
        all_Gr.extend(match)

    CPs_df['G_r'] = all_Gr
    CPs_df.to_csv(
        os.path.join(path_dft, 'G_r.txt')
    )

    return 1

if __name__=="__main__":
    
    import argparse
    parser = argparse.ArgumentParser(description='Optimization for mols. Specify directories, if required')

    from src.paths import DIR_DATA, DIR_CORES, DIR_DFT
    default_core_dft_path = os.path.join(DIR_DATA, DIR_CORES, DIR_DFT)

    parser.add_argument('--smiles', required=True, type=str, help='SMILES of optimized structure to be calculated critical points')
    parser.add_argument('--dir_dft', type=str, help='Exact storing directory of DFT results', default = default_core_dft_path)
    
    args,unk = parser.parse_known_args()
    if unk:
        print("unknown arguments passed ! i.e.,", *unk)

    exit = main(args)