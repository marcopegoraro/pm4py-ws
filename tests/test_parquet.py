import os
import unittest

from pm4pyws.handlers.parquet.parquet import ParquetHandler


def basic_test(path):
    handler = ParquetHandler()
    handler.build_from_path(path)
    handler.get_schema(variant="dfg_freq")
    handler.get_schema(variant="dfg_perf")
    handler.get_schema(variant="inductive_freq")
    handler.get_schema(variant="inductive_perf")
    handler.get_schema(variant="indbpmn_freq")
    handler.get_schema(variant="indbpmn_perf")
    handler.get_schema(variant="heuristics_freq")
    handler.get_schema(variant="heuristics_perf")
    handler.get_schema(variant="tree_freq")
    handler.get_schema(variant="tree_perf")
    handler.get_case_duration_svg()
    handler.get_events_per_time_svg()
    handler.get_sna(variant="handover")
    handler.get_sna(variant="working_together")
    handler.get_sna(variant="subcontracting")
    handler.get_sna(variant="jointactivities")
    handler.get_transient(86400)


def process_quantities_test(path):
    handler = ParquetHandler()
    handler.build_from_path(path)
    handler.get_start_activities()
    handler.get_end_activities()
    handler.get_variant_statistics()
    cases = handler.get_case_statistics()
    case_id_0 = cases[0]['caseId']
    handler.get_variant_statistics()
    handler.get_paths("concept:name")
    handler.get_attribute_values("concept:name")
    handler.get_events(case_id_0)


class ParquetTests(unittest.TestCase):
    def test_parquets_basic(self):
        basic_test("logs//running-example.parquet")
        basic_test("logs//receipt.parquet")

    def test_parquets_process_quantities(self):
        process_quantities_test("logs//running-example.parquet")
        process_quantities_test("logs//receipt.parquet")


if __name__ == "__main__":
    unittest.main()
