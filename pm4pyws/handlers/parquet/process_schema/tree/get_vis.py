from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.algo.filtering.pandas.auto_filter import auto_filter
from pm4py.visualization.common.utils import get_base64_from_gviz
from pm4py.visualization.process_tree import factory as pt_vis_factory


def apply(dataframe, parameters=None):
    if parameters is None:
        parameters = {}
    dataframe = auto_filter.apply_auto_filter(dataframe, parameters=parameters)
    dfg = df_statistics.get_dfg_graph(dataframe)
    tree = inductive_miner.apply_tree_dfg(dfg, parameters=parameters)
    gviz = pt_vis_factory.apply(tree, parameters={"format": "svg"})
    return get_base64_from_gviz(gviz)