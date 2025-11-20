_MAXCORE = 3000
_MAXITER = 500
_NPROC = 6

_PATH_ORCA_CMD = '/opt/orca/run-orca' # TODO set this path to run-orca cmd carefully :P

import os
_current_path = os.path.dirname(os.path.abspath(__file__))

if __name__=="__main__":
    from script_utils import append_parent, change2parent
    change2parent(_current_path)
else:
    from .script_utils import append_parent

append_parent(_current_path)

def getOrcaInpOpt(mol, charge=0, molt=1,
                  basis = "def2-SVP",
                  method='m062x',
                  freq=False,
                  solvent : str|None = None,
                  tightscf=False,
                  hess=False,
):
    from rdkit import Chem
    basis_str = basis.upper()

    if method != '6-311++G(d,p)':
        method_str = method.upper()
    else:
        method_str = method

    rows = []

    freq_str = 'Freq' if freq else ''
    tightscf_str = 'TightSCF' if tightscf else ''
    solvent_str = f'CPCM({solvent.upper()})' if solvent is not None else ''

    first_row = f"!{method_str} {basis_str} Opt {freq_str} {tightscf_str} {solvent_str}"
    rows.append(first_row)

    core_row = f"%maxcore {_MAXCORE}"
    rows.append(core_row)

    proc_block = f'pal\n\tnprocs {_NPROC}\nend'
    rows.append(proc_block)

    if hess:
        hess_block = f'%geom\n\tcalc_hess true\n\tMaxIter {_MAXITER}\nend'
        rows.append(hess_block)

    mol_block = f"* xyz {charge} {molt}\n"
    _mol_rows = Chem.MolToXYZBlock(mol).split("\n")
    mol_block+="\n".join(_mol_rows[2:])
    mol_block+='*'
    rows.append(mol_block)

    orca_input = '\n'.join(rows)

    return orca_input

def main(args):

    from rdkit import Chem
    import subprocess
    import re

    from src.paths import smi2safepath
    from src.utils import xyzToMol

    path_mm = os.path.join(args.dir_data, args.dir_task, args.dir_mm)

    if not os.path.exists(os.path.join(path_mm,f"{args.smiles}.mol")):
        print(f"*** File .mol for {args.smiles} not recognized ***")
        return 0
    
    path_dft = os.path.join(args.dir_data, args.dir_task, args.dir_dft)
    path_opt = os.path.join(args.dir_data, args.dir_task, args.dir_opt)
    
    if args.sub_dir:
        folder_setup = f'method={args.method}|basis={args.basis}|freq={args.freq}|solvent={args.solvent}|tightscf={args.tightscf}'
        path_dft = os.path.join(path_dft, folder_setup)
        path_opt = os.path.join(path_opt, folder_setup)

    if os.path.exists(os.path.join(path_opt, f"{args.smiles}.mol")):
        print(f"*** Optimization for {args.smiles} arleady processed ***")
        return 1
    
    path_mm = os.path.join(args.dir_data, args.dir_task, args.dir_mm)

    mm_mol = Chem.MolFromMolFile(os.path.join(path_mm, f"{args.smiles}.mol"),removeHs=False)
    charge = sum( [a.GetFormalCharge() for a in mm_mol.GetAtoms()] )

    print('charge recognized =', charge)

    path_dft_calc = os.path.join(path_dft, smi2safepath(args.smiles))

    if not os.path.exists(os.path.join(path_dft_calc, f'file.out')):
        inp = getOrcaInpOpt(mm_mol, basis = args.basis, method=args.method, charge = charge, solvent=args.solvent, freq=args.freq, tightscf=args.tightscf, hess=args.hess)
        print(inp)

        os.makedirs(path_dft_calc, exist_ok=True)
        with open(os.path.join(path_dft_calc, 'file.inp'), 'w') as f:
            print(inp, file=f)

        subprocess.run([_PATH_ORCA_CMD, 'file.inp'], 
                        stdout = subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        cwd=path_dft_calc+'/')

    with open(os.path.join(path_dft_calc, 'file.out'), "r") as f:
        ok = re.search("ORCA TERMINATED NORMALLY",f.read())

    if not ok:
        print(f"*** Computation on {args.smiles} failed or accidentally interrupted ***")
        return 0

    if not os.path.exists(os.path.join(path_dft_calc, f'file.xyz')):
        print(f'*** Optimized structure of {args.smiles} not found ***')
        return 0
    
    print(f'*** Optimized structure of {args.smiles} is going to be stored in {path_opt}')
    
    tmpMol = Chem.MolFromXYZFile(os.path.join(path_dft_calc, f'file.xyz'))
    tmpMol = xyzToMol(tmpMol, charge = charge)

    os.makedirs(path_opt, exist_ok=True)
    Chem.MolToMolFile(tmpMol, os.path.join(path_opt, f'{args.smiles}.mol'))

    return 1

if __name__=="__main__":

    from src.paths import DIR_DATA, DIR_CORES, DIR_MM, DIR_DFT, DIR_OPT
    
    import argparse
    parser = argparse.ArgumentParser(description='Optimization for mols. Specify necessarly SMILES and directories, if required')

    parser.add_argument('--smiles', type=str, help='SMILES of molecular structure to be optimized', required=True)

    parser.add_argument('--dir_data', type=str, default=DIR_DATA, help='Directory of full data files')
    parser.add_argument('--dir_task', type=str, default=DIR_CORES, help='Name of structures task. Should be "cores" or "reactions"')
    parser.add_argument('--dir_mm', type=str, default=DIR_MM, help='Directory of .mol molecules before DFT optimization')
    parser.add_argument('--dir_dft', type=str, help='Storing directory of DFT calculations', default = DIR_DFT, required = False)
    parser.add_argument('--dir_opt', type=str, default=DIR_OPT, help='Storing directory of .mol molecules after DFT optimization')

    parser.add_argument('--basis', type=str, help='Basis adopted for optimization', default = "def2-svp", required = False)
    parser.add_argument('--method', type=str, help='dft adopted for optimization', default = "m062x", required = False)
    parser.add_argument('--solvent', type=str, help='Implicit solvent', default = None, required = False, choices=('thf',))

    parser.add_argument('--tightscf', action='store_true', help='If emply TightSCF convergency cycles', default = False, required = False)
    parser.add_argument('--freq', action='store_true', help='Frequency calculation for minimum state energy', default = False, required = False)
    parser.add_argument('--hess', action='store_true', help='Wheter compute hessian matrix', default = False, required = False)

    parser.add_argument('--sub_dir', action='store_true', help='Wheter store results in sub dir named with method parameters', default = False, required = False)
    
    args,unk = parser.parse_known_args()
    if unk:
        print("unknown arguments passed ! i.e.,", *unk)
    
    exit = main(args)