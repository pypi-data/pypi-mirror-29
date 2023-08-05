# -*- coding: utf-8 -*-

"""This module contains functions that help overlay tabular data to nodes in a graph"""

import logging

from pybel.constants import NAME
from pybel.struct.filters import filter_nodes
from .. import pipeline
from ..filters.node_filters import function_namespace_inclusion_builder

__all__ = [
    'overlay_data',
    'overlay_type_data',
]

log = logging.getLogger(__name__)


@pipeline.in_place_mutator
def overlay_data(graph, data, label, overwrite=False):
    """Overlays tabular data on the network

    :param pybel.BELGraph graph: A BEL Graph
    :param dict data: A dictionary of {tuple node: data for that node}
    :param str label: The annotation label to put in the node dictionary
    :param bool overwrite: Should old annotations be overwritten?
    """
    for node, value in data.items():
        if node not in graph:
            log.debug('%s not in graph', node)
            continue
        elif label in graph.node[node] and not overwrite:
            log.debug('%s already on %s', label, node)
            continue
        graph.node[node][label] = value


# TODO switch label to be kwarg with default value DATA_WEIGHT
@pipeline.in_place_mutator
def overlay_type_data(graph, data, label, func, namespace, overwrite=False, impute=None):
    """Overlays tabular data on the network for data that comes from an data set with identifiers that lack
    namespaces.

    For example, if you want to overlay differential gene expression data from a table, that table
    probably has HGNC identifiers, but no specific annotations that they are in the HGNC namespace or
    that the entities to which they refer are RNA.

    :param pybel.BELGraph graph: A BEL Graph
    :param dict[str,float] dict data: A dictionary of {name: data}
    :param str label: The annotation label to put in the node dictionary
    :param str func: The function of the keys in the data dictionary
    :param str namespace: The namespace of the keys in the data dictionary
    :param bool overwrite: Should old annotations be overwritten?
    :param Optional[float] impute: The value to use for missing data
    """
    new_data = {
        node: data.get(graph.node[node][NAME], impute)
        for node in filter_nodes(graph, function_namespace_inclusion_builder(func, namespace))
    }

    overlay_data(graph, new_data, label, overwrite=overwrite)


def load_differential_gene_expression(data_path, gene_symbol_column='Gene.symbol', logfc_column='logFC'):
    """Quick and dirty loader for differential gene expression data

    :param str data_path:
    :param str gene_symbol_column:
    :param str logfc_colun:
    :return: A dictionary of {gene symbol: log fold change}
    :rtype: dict
    """
    import pandas as pd
    df = pd.read_csv(data_path)
    df = df.loc[df[gene_symbol_column].notnull(), [gene_symbol_column, logfc_column]]

    return {
        k: v
        for _, k, v in df.itertuples()
    }
