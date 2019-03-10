from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.algo.filtering.pandas.auto_filter import auto_filter
from pm4py.objects.log.util import xes
from pm4py.visualization.common.utils import get_base64_from_gviz
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.visualization.petrinet.util.vis_trans_shortest_paths import get_decorations_from_dfg_spaths_acticount
from pm4py.visualization.petrinet.util.vis_trans_shortest_paths import get_shortest_paths


def apply(dataframe, parameters=None):
    if parameters is None:
        parameters = {}
    dataframe = auto_filter.apply_auto_filter(dataframe, parameters=parameters)
    dfg = df_statistics.get_dfg_graph(dataframe)
    activities_count = attributes_filter.get_attribute_values(dataframe, xes.DEFAULT_NAME_KEY)
    net, im, fm = inductive_miner.apply_dfg(dfg, parameters=parameters)
    spaths = get_shortest_paths(net)
    aggregated_statistics = get_decorations_from_dfg_spaths_acticount(net, dfg, spaths,
                                                                      activities_count,
                                                                      variant="frequency")
    gviz = pn_vis_factory.apply(net, im, fm, parameters={"format": "svg"}, variant="frequency",
                                aggregated_statistics=aggregated_statistics)
    return get_base64_from_gviz(gviz)