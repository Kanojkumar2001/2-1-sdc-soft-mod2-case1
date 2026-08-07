import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).parent.parent))

from app.web_interface import app


class TestWebInterface(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_page_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Personal Finance Advisor', response.data)


if __name__ == '__main__':
    unittest.main()