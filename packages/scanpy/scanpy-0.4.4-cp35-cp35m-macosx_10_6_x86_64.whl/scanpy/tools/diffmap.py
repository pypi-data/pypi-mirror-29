from ..tools import dpt
from .. import settings
from .. import logging as logg


def diffmap(adata, n_comps=15, n_neighbors=None, knn=True, n_pcs=50, sigma=0,
            n_jobs=None, flavor='haghverdi16', copy=False):
    """Diffusion Maps [Coifman05]_ [Haghverdi15]_ [Wolf17]_.

    Diffusion maps [Coifman05]_ has been proposed for visualizing single-cell
    data by [Haghverdi15]_. The tool uses the adapted Gaussian kernel suggested
    by [Haghverdi16]_ in the implementation of [Wolf17]_.

    Parameters
    ----------
    adata : :class:`~scanpy.api.AnnData`
        Annotated data matrix.
    n_comps : `int`, optional (default: 15)
        The number of dimensions of the representation.
    n_neighbors : `int`, optional (default: 30)
        Specify the number of nearest neighbors in the knn graph. If knn ==
        False, set the Gaussian kernel width to the distance of the kth
        neighbor (method 'local').
    knn : `bool`, optional (default: `True`)
        If `True`, use a hard threshold to restrict the number of neighbors to
        `n_neighbors`, that is, consider a knn graph. Otherwise, use a Gaussian
        Kernel to assign low weights to neighbors more distant than the
        `n_neighbors` nearest neighbor.
    n_pcs : `int`, optional (default: 50)
        Use `n_pcs` PCs to compute the Euclidian distance matrix, which is the
        basis for generating the graph. Set to 0 if you don't want preprocessing
        with PCA.
    n_jobs : `int` or `None`
        Number of CPUs to use (default: `sc.settings.n_jobs`).
    copy : `bool` (default: `False`)
        Return a copy instead of writing to adata.

    Returns
    -------
    Depending on `copy`, returns or updates `adata` with the following fields.

    X_diffmap : `adata.obsm`
        Array of shape (#samples) × (#eigen vectors). Diffusion map
        representation of data, which is the right eigen basis of the transition
        matrix with eigenvectors as columns.
    diffmap_evals : `np.ndarray` (`adata.uns`)
        Array of size (number of eigen vectors). Eigenvalues of transition matrix.
    """
    logg.info('computing Diffusion Maps', r=True)
    if n_comps <= 2:
        raise ValueError('Provide any value greater than 2. '
                         'Mind that the 0th component of diffusion maps '
                         'is not used for visualization.')
    adata = adata.copy() if copy else adata
    dmap = dpt.DPT(adata, n_neighbors=n_neighbors, knn=knn, n_pcs=n_pcs,
                   n_dcs=n_comps, n_jobs=n_jobs, recompute_graph=True,
                   flavor=flavor)
    dmap.update_diffmap()
    adata.uns['data_graph_distance_local'] = dmap.Dsq
    adata.uns['data_graph_norm_weights'] = dmap.Ktilde
    adata.obsm['X_diffmap'] = dmap.rbasis[:, 1:]
    adata.obs['X_diffmap0'] = dmap.rbasis[:, 0]
    adata.uns['diffmap_evals'] = dmap.evals[1:]
    logg.info('    finished', time=True, end=' ' if settings.verbosity > 2 else '\n')
    logg.hint('added\n'
              '    \'X_diffmap\', tSNE coordinates (adata.obsm)\n'
              '    \'diffmap_evals\', eigenvalues of transition matrix (adata.uns)')
    return adata if copy else None
