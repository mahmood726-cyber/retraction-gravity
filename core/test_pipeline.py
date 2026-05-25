import json
import os
import tempfile
import unittest

from core.math import propagate_retraction_gravity
from core.pipeline import RESULTS_PATH, run_pipeline


class TestRetractionGravityPipeline(unittest.TestCase):
    def test_pipeline_writes_repo_relative_output_from_any_cwd(self):
        original_cwd = os.getcwd()
        temp_cwd = tempfile.mkdtemp()
        temp_output = os.path.join(temp_cwd, "gravity_results.json")
        try:
            os.chdir(temp_cwd)
            output = run_pipeline(output_path=temp_output)
        finally:
            os.chdir(original_cwd)

        self.assertTrue(os.path.isabs(RESULTS_PATH))
        self.assertTrue(os.path.exists(temp_output))
        with open(temp_output, encoding="utf-8") as handle:
            saved = json.load(handle)

        self.assertEqual(saved["graph"], output["graph"])
        self.assertEqual([scenario["id"] for scenario in saved["scenarios"]], ["baseline", "shock_trial", "shock_method"])

    def test_unknown_retraction_node_raises_clear_error(self):
        nodes = [{"id": "A"}, {"id": "B"}]
        edges = [{"source": "A", "target": "B"}]

        with self.assertRaisesRegex(ValueError, "Unknown retraction event node id"):
            propagate_retraction_gravity(nodes, edges, "MISSING")

    def test_invalid_edge_reference_raises_clear_error(self):
        nodes = [{"id": "A"}, {"id": "B"}]
        edges = [{"source": "A", "target": "C"}]

        with self.assertRaisesRegex(ValueError, "Edge references unknown node"):
            propagate_retraction_gravity(nodes, edges, "A")


if __name__ == "__main__":
    unittest.main()
