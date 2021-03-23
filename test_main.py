import unittest
from app.main import app
from app.database.models import addTestData, deleteTestData, Actor
import json


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the unit tests for Casting Agency end points"""

    @classmethod
    def setUpClass(cls):
        addTestData()

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client()
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVZclR5NG04ZmIwbVZGWmtRVl9EUSJ9.eyJpc3MiOiJodHRwczovL3NjaGV2b2xhLWNvZmZlZS1zaG9wLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDU5MjIwYTNhZDU3YTAwNjkxZmIzMWIiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNjE2NDYzODIzLCJleHAiOjE2MTY1NTAyMjMsImF6cCI6Ikl6NXpPR1hXWm03Sk1VbDVRYm1XUWZuQUFJMGU2MEpGIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Eb9k0eBPzvYJQ77kOO7BNNvfSWUQ7VapNl7mHXzvqtAg-XgmfMr_uIw9eVIcgjgpmleBUE__pGzsT3Xsg8FQz2KspHwxaWnbGZESGIxD4BurNsBqTHyKljvDAStFMfPk6sKikvkyas9wu0z3WHxP9GnNIqQE3NbuK_oR4JEBc2VoOf5l8KAVLnGbPS_PqbQJuNZ34hPhwWJL49XOxSRBLakNQnNFHGf6fDF6VfZ66JZqXnx1EJo-dKr0rv14ct_l8xJKb9vVQyiVxwADcY7lATg2OHkq-BAc92C0tCfgfA0sWeRBTtC_-ODQrujJxN5UpAy9eEWf8XVfC78L_CassQ"
        self.authHeader = {"Authorization": "Bearer {}".format(self.token)}

    @classmethod
    def tearDownClass(self):
        deleteTestData()

    def test_healthCheck_success(self):
            result = self.client.get('/')
            self.assertEqual(200, result.status_code)
            self.assertTrue(result.json['success'])
            self.assertEqual("Healthy", result.json['action'])

    def test_getActors_success(self):
        result = self.client.get('/actors', headers=self.authHeader)
        self.assertEqual(200, result.status_code)
        actors = result.json['actors']
        self.assertTrue(len(actors) >= 3)
        dataset = self.getDataSetForActor(actors, "billyasdf")
        self.assertEqual(32,dataset['age'])
        self.assertEqual('M',dataset['gender'])
        self.assertIsNotNone(dataset['id'])
        dataset = self.getDataSetForActor(actors, "jimmyasdf")
        self.assertEqual(64,dataset['age'])
        self.assertEqual('M',dataset['gender'])
        self.assertIsNotNone(dataset['id'])
        dataset = self.getDataSetForActor(actors, "samasdf")
        self.assertEqual(21,dataset['age'])
        self.assertEqual('F',dataset['gender'])
        self.assertIsNotNone(dataset['id'])
        self.assertTrue(result.json['success'])

    def test_addActor_success(self):
        result = self.client.post('/actors', headers=self.authHeader,
                                  data=json.dumps(dict(
                                    name="freddyasdf",
                                    age=123,
                                    gender='F')),
                                  content_type='application/json')
        self.assertEqual(200, result.status_code)
        actor = result.json['actor']
        self.assertEqual('freddyasdf',actor['name'])
        self.assertEqual(123,actor['age'])
        self.assertEqual('F',actor['gender'])
        self.assertIsNotNone(actor['id'])
        self.assertTrue(result.json['success'])
        actorDel = Actor.query.get(actor['id'])
        actorDel.delete()

    def test_ActorAlreadyExists_fail(self):
        result1 = self.client.post('/actors', headers=self.authHeader,
                                  data=json.dumps(dict(
                                      name="freddyasdf",
                                      age=123,
                                      gender='F')),
                                  content_type='application/json')
        result = self.client.post('/actors', headers=self.authHeader,
                                  data=json.dumps(dict(
                                      name="freddyasdf",
                                      age=123,
                                      gender='F')),
                                  content_type='application/json')
        actor = result1.json['actor']
        actorDel = Actor.query.get(actor['id'])
        actorDel.delete()
        self.assertEqual(409, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("DataBase insert error", result.json['errorCode'])

    def test_ActorNameNotProvided_fail(self):
        result = self.client.post('/actors', headers=self.authHeader,
                                  data=json.dumps(dict(
                                      age=123,
                                      gender='F')),
                                  content_type='application/json')
        self.assertEqual(400, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Invalid Request", result.json['errorCode'])

    def test_ActorAgeNotProvided_fail(self):
        result = self.client.post('/actors', headers=self.authHeader,
                                  data=json.dumps(dict(
                                      name='asdf',
                                      gender='F')),
                                  content_type='application/json')
        self.assertEqual(400, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Invalid Request", result.json['errorCode'])

    def test_ActorGenderNotProvided_fail(self):
        result = self.client.post('/actors', headers=self.authHeader,
                                  data=json.dumps(dict(
                                      name='asdf',
                                      age=123)),
                                  content_type='application/json')
        self.assertEqual(400, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Invalid Request", result.json['errorCode'])













    def getDataSetForActor(self, actors, name):
        for actor in actors:
            if actor['name'] == name:
                return actor
        return None


if __name__ == "__main__":
    unittest.main()
