import os
_current_path = os.path.dirname(os.path.abspath(__file__))

if __name__=="__main__":
    from script_utils import append_parent, change2parent
    change2parent(_current_path)
else:
    from .script_utils import append_parent

append_parent(_current_path)

from sklearn.cluster import DBSCAN, KMeans
from sklearn_extra.cluster import KMedoids
clusterizers={
    'kmeans':KMeans,
    'dbscan':DBSCAN,
    'kmedoids':KMedoids,
}

def main(args):
    import pandas as pd
    import numpy as np

    from src.cluster import global_metrics, silhouette_samples

    dir_computed_data = os.path.join(args.dir_data, args.dir_cores, args.dir_comp)

    scores_path = os.path.join(dir_computed_data, 'PCAscore_def.csv')
    scores = pd.read_csv(scores_path, index_col="smiles") # XXX care here : outliers structures are not included
    PCs = scores[[f"PC{_+1}" for _ in range(3)]].values

    dir_cluster_data = os.path.join(dir_computed_data, f'clusterizer={args.clusterizer}',f'seed={args.seed}')
    os.makedirs(dir_cluster_data, exist_ok=True)

    clusterizer_fnc = clusterizers[args.clusterizer]

    globalMetrics = pd.DataFrame(index=range(2,args.max_cluster+1), columns=global_metrics.keys())
    globalMetrics.index.name ="size"
    for cluster in range(2,args.max_cluster+1):
        # kmeans = KMeans(n_clusters = cluster, init='k-means++', n_init=len(PCs), random_state=args.seed)
        clusterizer = clusterizer_fnc(n_clusters = cluster, random_state=args.seed)
        labels = clusterizer.fit_predict(PCs)
        for metric,fnc in global_metrics.items():
            if not fnc:
                globalMetrics.at[cluster,metric]=clusterizer.inertia_
            else:
                globalMetrics.at[cluster,metric]=fnc(PCs, labels)

        silhouette = silhouette_samples(PCs, labels)
        localMetric = pd.DataFrame(np.stack([labels, silhouette]).T, index = scores.index, columns=["cluster", "silhouette"])

        localMetric.to_csv(os.path.join(dir_cluster_data, f"local_k{cluster}.csv"))

    globalMetrics.to_csv(os.path.join(dir_cluster_data, "global.csv"))

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='Clustering mols in 3D PC space. Specify directories, if required')

    from src.paths import DIR_DATA, DIR_CORES, DIR_COMP

    parser.add_argument('--dir_data', type=str, default=DIR_DATA, help='Directory of full data files')
    parser.add_argument('--dir_cores', type=str, default=DIR_CORES, help='Directory where full core data file are stored')
    parser.add_argument('--dir_comp', type=str, default=DIR_COMP, help='Directory of computed features for the structures.')

    parser.add_argument('--seed', type=int, default=0, help='Random seed adopted for the clusterization.')
    parser.add_argument('--max_cluster', type=int, default=20, help='Max number of cluster to find and store.')
    parser.add_argument('--clusterizer', type=str, default='kmeans', choices=list(clusterizers.keys()), help='Clustering algorithm.')
    
    args,unk = parser.parse_known_args()
    if unk:
        print("unknown arguments passed ! i.e.,", *unk)

    exit = main(args)
