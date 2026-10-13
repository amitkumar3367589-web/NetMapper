
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from netmapper.reporter import save_json, save_csv


class TestReporter(unittest.TestCase):

    def test_json_report(self):
        sample = {"hosts": [{"ip": "192.168.1.10"}]}

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("netmapper.reporter.REPORTS_DIR", Path(temp_dir)):
                save_json(sample, "test.json")

            report_path = Path(temp_dir) / "test.json"
            self.assertTrue(report_path.exists())

            with report_path.open(encoding="utf-8") as file:
                report = json.load(file)

            self.assertEqual(report["results"], sample)
            self.assertEqual(report["tool"], "NetMapper")

    def test_csv_report(self):
        hosts = [
            {
                "ip": "192.168.1.10",
                "hostname": "test-device",
                "status": "UP",
                "open_ports": [80, 443],
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("netmapper.reporter.REPORTS_DIR", Path(temp_dir)):
                save_csv(hosts, "test.csv")

            report_path = Path(temp_dir) / "test.csv"
            self.assertTrue(report_path.exists())

            with report_path.open(
                encoding="utf-8", newline=""
            ) as file:
                rows = list(csv.DictReader(file))

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["ip"], "192.168.1.10")
            self.assertEqual(rows[0]["open_ports"], "80, 443")


if __name__ == "__main__":
    unittest.main()
