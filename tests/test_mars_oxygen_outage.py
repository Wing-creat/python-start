"""Tests for the one-day Mars habitat oxygen-production outage study."""

import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "06_Astronomy"))

from mars_oxygen_outage import save_outage_plot


class MarsOxygenOutageTests(unittest.TestCase):
    def test_plot_creates_a_nonempty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "mars" / "outage.png"
            save_outage_plot([10, 10.4, 10.8], [10, 5.9, 6.3], 1, str(output))
            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
