from .anndata import scatter, violin, ranking, clustermap

from .preprocessing import filter_genes_dispersion

from .tools import pca, pca_loadings, pca_scatter, pca_variance_ratio
from .tools import diffmap
from .tools import draw_graph
from .tools import tsne
from .tools import umap
from .tools import aga, aga_attachedness, aga_graph, aga_path, aga_scatter
from .tools import dpt, dpt_scatter, dpt_groups_pseudotime, dpt_timeseries
from .tools import louvain
from .tools import rank_genes_groups, rank_genes_groups_violin
from .tools import sim
from .top_genes_visual import correlation_matrix, exploratory_rank_analysis, top_ranked_group_analysis, \
    ROC_AUC_analysis, comparison_table, comparison_v2

from .rcmod import reset_rcParams, set_rcParams_Scanpy, set_rcParams_Defaults
from . import palettes

from .utils import matrix
from .utils import timeseries, timeseries_subplot, timeseries_as_heatmap

# set Scanpy defaults
set_rcParams_Scanpy()
