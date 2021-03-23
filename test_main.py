import unittest
from app.main import create_app


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the unit tests for Casting Agency end points"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.questionText = "asdfooiuqwerlkjsfamoipiuqwlekrjasdfpoiqjweasdjkhfauihebagsjk"
        self.app = create_app()
        self.client = self.app.test_client

    def test_healthCheck_success(self):
        result = self.client().get('/')
        self.assertEqual(200, result.status_code)
        self.assertTrue(result.json['success'])
        self.assertEqual("Healthy", result.json['action'])


if __name__ == "__main__":
    unittest.main()
