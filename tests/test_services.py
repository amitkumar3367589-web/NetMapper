
import unittest

from netmapper.services import identify_service


class TestServiceIdentification(unittest.TestCase):

    def test_dns_port(self):
        self.assertEqual(identify_service(53), "DNS")

    def test_ssh_port(self):
        self.assertEqual(identify_service(22), "SSH")

    def test_http_port(self):
        self.assertEqual(identify_service(80), "HTTP")

    def test_unknown_port(self):
        self.assertEqual(identify_service(12345), "Unknown")


if __name__ == "__main__":
    unittest.main()
