from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.algo.discovery.inductive.versions.dfg import imdfb as inductive_miner
from pm4py.algo.filtering.pandas.auto_filter import auto_filter
from pm4py.objects.log.util import xes
from pm4py.objects.petri.exporter.pnml import export_petri_as_string
from pm4py.visualization.common.utils import get_base64_from_gviz, get_base64_from_file
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.visualization.petrinet.util.vis_trans_shortest_paths import get_decorations_from_dfg_spaths_acticount
from pm4py.visualization.petrinet.util.vis_trans_shortest_paths import get_shortest_paths
from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.algo.filtering.pandas.start_activities import start_activities_filter
from pm4py.algo.filtering.pandas.end_activities import end_activities_filter
from pm4py.util import constants as pm4_constants
from pm4py.algo.filtering.common.filtering_constants import CASE_CONCEPT_NAME
from pm4pyws.util import get_graph
import base64

from pm4pyws.util import constants

from pm4pybpmn.objects.conversion.petri_to_bpmn import factory as petri_to_bpmn
from pm4pybpmn.visualization.bpmn import factory as bpmn_vis_factory


def apply(dataframe, parameters=None):
    """
    Gets the Petri net through Inductive Miner, decorated by frequency metric

    Parameters
    ------------
    dataframe
        Dataframe
    parameters
        Parameters of the algorithm

    Returns
    ------------
    base64
        Base64 of an SVG representing the model
    model
        Text representation of the model
    format
        Format of the model
    """
    if parameters is None:
        parameters = {}

    activity_key = parameters[pm4_constants.PARAMETER_CONSTANT_ACTIVITY_KEY] if pm4_constants.PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY
    timestamp_key = parameters[pm4_constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] if pm4_constants.PARAMETER_CONSTANT_TIMESTAMP_KEY in parameters else xes.DEFAULT_TIMESTAMP_KEY
    case_id_glue = parameters[pm4_constants.PARAMETER_CONSTANT_CASEID_KEY] if pm4_constants.PARAMETER_CONSTANT_CASEID_KEY in parameters else CASE_CONCEPT_NAME

    parameters[pm4_constants.RETURN_EA_COUNT_DICT_AUTOFILTER] = True
    dataframe = attributes_filter.filter_df_keeping_spno_activities(dataframe, activity_key=activity_key,
                                                                    max_no_activities=constants.MAX_NO_ACTIVITIES)
    dataframe, end_activities = auto_filter.apply_auto_filter(dataframe, parameters=parameters)
    end_activities = list(end_activities.keys())
    dfg = df_statistics.get_dfg_graph(dataframe, activity_key=activity_key, timestamp_key=timestamp_key, case_id_glue=case_id_glue, sort_caseid_required=False, sort_timestamp_along_case_id=False)
    activities_count = attributes_filter.get_attribute_values(dataframe, activity_key, parameters=parameters)
    activities = list(activities_count.keys())
    start_activities = list(start_activities_filter.get_start_activities(dataframe, parameters=parameters).keys())

    net, im, fm = inductive_miner.apply_dfg(dfg, parameters, activities=activities, start_activities=start_activities, end_activities=end_activities)
    spaths = get_shortest_paths(net)
    aggregated_statistics = get_decorations_from_dfg_spaths_acticount(net, dfg, spaths,
                                                                      activities_count,
                                                                      variant="frequency")


    bpmn_graph, el_corr, inv_el_corr, el_corr_keys_map = petri_to_bpmn.apply(net, im, fm)

    gviz = bpmn_vis_factory.apply_petri(net, im, fm, aggregated_statistics=aggregated_statistics, parameters={"format": "svg"})

    gviz_base64 = base64.b64encode("".encode('utf-8'))

    ret_graph = get_graph.get_graph_from_petri(net, im, fm)

    return get_base64_from_file(gviz.name), export_petri_as_string(net, im, fm), ".pnml", "parquet", activities, start_activities, end_activities, gviz_base64, ret_graph, "indbpmn", "freq", None, ""

