import os
import re
import pandas as pd

from rdkit import Chem
from rdkit.Chem import Descriptors, Descriptors3D

from .paths import DIR_DFT, DIR_CORES, DIR_DATA, smi2safepath

# dipole value extracted from orca file output
def dipoleMoment(smi, dft_dir = os.path.join(DIR_DATA, DIR_CORES, DIR_DFT)):
    patt = r"magnitude\s*\(debye\)\s*:\s*(?P<dm>[-\.0-9]+)$"
    compiler = re.compile(patt, flags=re.MULTILINE | re.IGNORECASE)
    
    safe_name = smi2safepath(smi)
    path_file = os.path.join(dft_dir, safe_name, 'file.out')
    with open(path_file) as f:
        match = compiler.search(f.read())
        
    if match is None: # FIXME we should not have a nan dipole moment !
        return None
    return float(match["dm"])

def strain_energy(smi, dft_dir = os.path.join(DIR_DATA, DIR_CORES, DIR_DFT)):
        
	safe_name = smi2safepath(smi)
	path_file = os.path.join(dft_dir, safe_name, 'G_r.txt')

	df = pd.read_csv(path_file, index_col=0)
	mean_Gr = df['G_r'].mean()
	energy = 337.72*mean_Gr-8.115
	return energy

desc_2d={
    'QeD':Descriptors.qed,
    'logP':Descriptors.MolLogP,
    'TPSA':Descriptors.TPSA,
    'SMR_VSA3':Descriptors.SMR_VSA3,
    'SlogP_VSA3':Descriptors.SlogP_VSA3,
    'MR':Descriptors.MolMR,
    'NumNatoms':lambda x: len(x.GetSubstructMatches(Chem.MolFromSmarts('N'))),
    'NumOatoms':lambda x: len(x.GetSubstructMatches(Chem.MolFromSmarts('O'))),
}

compute_3Dscore = lambda x : Descriptors3D.NPR1(x)+Descriptors3D.NPR2(x)