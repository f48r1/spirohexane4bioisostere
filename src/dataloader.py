import pandas as pd
import os

from .paths import DIR_RAW, DIR_OPT, DIR_COMP, DIR_CORES, DIR_DATA

from rdkit import Chem

class Dataloader:
    def __init__(self, dir_data=DIR_DATA, dir_cores=DIR_CORES, dir_raw=DIR_RAW, dir_opt = DIR_OPT, dir_comp = DIR_COMP):
        self.dir_data=dir_data
        self.dir_cores=dir_cores
        self.dir_raw=dir_raw
        self.dir_opt = dir_opt
        self.dir_comp = dir_comp

        self.cores = None
        self.dft_mols = None

        self.descriptions = None
        self.descriptions_selected = None

        self.scores = None
        self.scores_selected = None

    def load_cores(self):
        self.cores = pd.read_csv(os.path.join(self.dir_data, self.dir_cores, self.dir_raw,'cores.csv'))
    
    def load_dft_mols(self):

        mols_from_dft = self.cores.smiles.apply(lambda x : Chem.MolFromMolFile(
            os.path.join(self.dir_data, self.dir_cores, self.dir_opt,str(x)+".mol"), removeHs=False)
        )
        mols_from_dft.name = 'mol'

        self.dft_mols = mols_from_dft

    def load_descriptions(self):
        self.descriptions = pd.read_csv(os.path.join(self.dir_data, self.dir_cores, self.dir_comp,'descripted.csv'))

    def load_descriptions_selected(self):
        self.descriptions_selected= pd.read_csv(os.path.join(self.dir_data, self.dir_cores, self.dir_comp,'descripted_def.csv'))

    @property
    def smiles(self):
        return self.cores.smiles

    def load_scores(self):
        self.scores = pd.read_csv(os.path.join(self.dir_data, self.dir_cores, self.dir_comp,"PCAscore.csv"))

    def load_scores_selected(self):
        self.scores_selected = pd.read_csv(os.path.join(self.dir_data, self.dir_cores, self.dir_comp,"PCAscore_def.csv"))

    def get_global_cluster(self, clusterizer, seed,):
        return pd.read_csv(os.path.join(self.dir_data, self.dir_cores, self.dir_comp,f"clusterizer={clusterizer}/seed={seed}/global.csv"), index_col="size")
    
    def get_local_cluster(self, clusterizer, seed, size):
        return pd.read_csv(os.path.join(self.dir_data, self.dir_cores, self.dir_comp,f"clusterizer={clusterizer}/seed={seed}/local_k{size}.csv"), index_col='smiles')

special_cores=[
    'C1CCNCC1',
    'C1CC12COC2',
    'C1CC2(C1)CC2',
    'C1CC12CNC2',
]
