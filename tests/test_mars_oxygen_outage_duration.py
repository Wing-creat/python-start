"""Tests for the Mars habitat outage-duration comparison plot."""

import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "06_Astronomy"))

from mars_oxygen_outage_duration import save_outage_duration_plot


class MarsOxygenOutageDurationTests(unittest.TestCase):
    def test_plot_creates_a_nonempty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "mars" / "duration.png"
            save_outage_duration_plot([1, 2, 3], [8.7, 4.6, 0.5], str(output))
            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
