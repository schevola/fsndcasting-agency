import os
import unittest
from app.main import app
from app.database.models import addTestData, deleteTestData, Actor, Movie
import json


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the unit tests for Casting Agency end points"""

    tokenEP = None
    tokenCA = None
    tokenCD = None

    @classmethod
    def setUpClass(cls):
        global tokenEP
        global tokenCA
        global tokenCD
        # set as globals because accessing them from system
        # every test was slowing the tests down
        tokenEP = os.environ.get('PRODUCER')
        tokenCA = os.environ.get('ASSISTANT')
        tokenCD = os.environ.get('DIRECTOR')
        addTestData()

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client()
        global tokenEP
        global tokenCA
        global tokenCD
        self.authHeaderEP = {"Authorization": "Bearer {}".format(tokenEP)}
        self.authHeaderCA = {"Authorization": "Bearer {}".format(tokenCA)}
        self.authHeaderCD = {"Authorization": "Bearer {}".format(tokenCD)}

    @classmethod
    def tearDownClass(cls):
        deleteTestData()

    def test_healthCheck_success(self):
        result = self.client.get('/')
        self.assertEqual(200, result.status_code)
        self.assertTrue(result.json['success'])
        self.assertEqual("Healthy", result.json['action'])

    def test_getActors_success(self):
        result = self.client.get('/actors', headers=self.authHeaderEP)
        self.assertEqual(200, result.status_code)
        actors = result.json['actors']
        self.assertTrue(len(actors) >= 3)
        dataset = self.getDataSetForActor(actors, "billyasdf")
        self.assertEqual(32, dataset['age'])
        self.assertEqual('M', dataset['gender'])
        self.assertIsNotNone(dataset['id'])
        dataset = self.getDataSetForActor(actors, "jimmyasdf")
        self.assertEqual(64, dataset['age'])
        self.assertEqual('M', dataset['gender'])
        self.assertIsNotNone(dataset['id'])
        dataset = self.getDataSetForActor(actors, "samasdf")
        self.assertEqual(21, dataset['age'])
        self.assertEqual('F', dataset['gender'])
        self.assertIsNotNone(dataset['id'])
        self.assertTrue(result.json['success'])

    def test_addActor_success(self):
        result = self.client.post('/actors', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      name="freddyasdf",
                                      age=123,
                                      gender='F')),
                                  content_type='application/json')
        self.assertEqual(200, result.status_code)
        actor = result.json['actor']
        self.assertEqual('freddyasdf', actor['name'])
        self.assertEqual(123, actor['age'])
        self.assertEqual('F', actor['gender'])
        self.assertIsNotNone(actor['id'])
        self.assertTrue(result.json['success'])
        actorDel = Actor.query.get(actor['id'])
        actorDel.delete()

    def test_addActorAlreadyExists_fail(self):
        result1 = self.client.post('/actors', headers=self.authHeaderEP,
                                   data=json.dumps(dict(
                                       name="freddyasdf",
                                       age=123,
                                       gender='F')),
                                   content_type='application/json')
        result = self.client.post('/actors', headers=self.authHeaderEP,
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

    def test_addActorNameNotProvided_fail(self):
        result = self.client.post('/actors', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      age=123,
                                      gender='F')),
                                  content_type='application/json')
        self.assertEqual(400, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Invalid Request", result.json['errorCode'])

    def test_addActorAgeNotProvided_fail(self):
        result = self.client.post('/actors', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      name='asdf',
                                      gender='F')),
                                  content_type='application/json')
        self.assertEqual(400, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Invalid Request", result.json['errorCode'])

    def test_addActorGenderNotProvided_fail(self):
        result = self.client.post('/actors', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      name='asdf',
                                      age=123)),
                                  content_type='application/json')
        self.assertEqual(400, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Invalid Request", result.json['errorCode'])

    def test_updateActor_success(self):
        result = self.client.post('/actors', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      name="freddyasdf",
                                      age=123,
                                      gender='F')),
                                  content_type='application/json')
        self.assertEqual(200, result.status_code)
        actor = result.json['actor']
        result = self.client.patch('/actors/' + str(actor['id']),
                                   headers=self.authHeaderEP,
                                   data=json.dumps(dict(
                                       name="freddyasdfasdf")),
                                   content_type='application/json')
        self.assertEqual(200, result.status_code)
        actor = result.json['actor']
        self.assertEqual('freddyasdfasdf', actor['name'])
        self.assertEqual(123, actor['age'])
        self.assertEqual('F', actor['gender'])
        self.assertIsNotNone(actor['id'])
        self.assertTrue(result.json['success'])
        actorDel = Actor.query.get(actor['id'])
        actorDel.delete()

    def test_updateActorDoesNotExist_fail(self):
        result = self.client.patch('/actors/999999', headers=self.authHeaderEP,
                                   data=json.dumps(dict(
                                       name="freddyasdfasdf")),
                                   content_type='application/json')
        self.assertEqual(404, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Resource Not Found", result.json['errorCode'])

    def test_deleteActor_success(self):
        result = self.client.post('/actors', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      name="freddyasdf",
                                      age=123,
                                      gender='F')),
                                  content_type='application/json')
        self.assertEqual(200, result.status_code)
        actor = result.json['actor']
        result = self.client.delete('/actors/' + str(actor['id']),
                                    headers=self.authHeaderEP)
        self.assertEqual(200, result.status_code)
        self.assertEqual(actor['id'], result.json['actorId'])
        self.assertTrue(result.json['success'])

    def test_deleteActorDoesNotExist_fail(self):
        result = self.client.delete('/actors/999999',
                                    headers=self.authHeaderEP)
        self.assertEqual(404, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Resource Not Found", result.json['errorCode'])

    def test_getMovies_success(self):
        result = self.client.get('/movies', headers=self.authHeaderEP)
        self.assertEqual(200, result.status_code)
        print(result.json['movies'])
        movies = result.json['movies']
        self.assertTrue(len(movies) >= 3)
        dataset = self.getDataSetForMovie(movies, "billyasdfMovie")
        self.assertEqual('12/25/2002', dataset['releaseDate'])
        self.assertIsNotNone(dataset['id'])
        dataset = self.getDataSetForMovie(movies, "jimmyasdfMovie")
        self.assertEqual('01/14/2022', dataset['releaseDate'])
        self.assertIsNotNone(dataset['id'])
        dataset = self.getDataSetForMovie(movies, "samasdfMovie")
        self.assertEqual('03/02/1978', dataset['releaseDate'])
        self.assertIsNotNone(dataset['id'])
        self.assertTrue(result.json['success'])

    def test_addMovie_success(self):
        result = self.client.post('/movies', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      title="freddyasdfMovie",
                                      releaseDate="07/05/1977")),
                                  content_type='application/json')
        self.assertEqual(200, result.status_code)
        movie = result.json['movie']
        self.assertEqual('freddyasdfMovie', movie['title'])
        self.assertEqual("07/05/1977", movie['releaseDate'])
        self.assertIsNotNone(movie['id'])
        self.assertTrue(result.json['success'])
        movieDel = Movie.query.get(movie['id'])
        movieDel.delete()

    def test_addMovieAlreadyExists_fail(self):
        result1 = self.client.post('/movies', headers=self.authHeaderEP,
                                   data=json.dumps(dict(
                                       title="freddyasdfMovie",
                                       releaseDate="07/05/1977")),
                                   content_type='application/json')
        result = self.client.post('/movies', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      title="freddyasdfMovie",
                                      releaseDate="07/05/1977")),
                                  content_type='application/json')
        movie = result1.json['movie']
        movieDel = Movie.query.get(movie['id'])
        movieDel.delete()
        self.assertEqual(409, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("DataBase insert error", result.json['errorCode'])

    def test_addMovieTitleNotProvided_fail(self):
        result = self.client.post('/movies', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      releaseDate="07/05/1977")),
                                  content_type='application/json')
        self.assertEqual(400, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Invalid Request", result.json['errorCode'])

    def test_addMovieReleaseDateNotProvided_fail(self):
        result = self.client.post('/movies', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      title="freddyasdfMovie")),
                                  content_type='application/json')
        self.assertEqual(400, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Invalid Request", result.json['errorCode'])

    def test_updateMovie_success(self):
        result = self.client.post('/movies', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      title="freddyasdfMovie",
                                      releaseDate="07/05/1977")),
                                  content_type='application/json')
        self.assertEqual(200, result.status_code)
        movie = result.json['movie']
        result = self.client.patch('/movies/' + str(movie['id']),
                                   headers=self.authHeaderEP,
                                   data=json.dumps(dict(
                                       title="freddyasdfMoviefreddyasdfMovi")),
                                   content_type='application/json')
        self.assertEqual(200, result.status_code)
        movie = result.json['movie']
        self.assertEqual('freddyasdfMoviefreddyasdfMovi', movie['title'])
        self.assertEqual("07/05/1977", movie['releaseDate'])
        self.assertIsNotNone(movie['id'])
        self.assertTrue(result.json['success'])
        movieDel = Movie.query.get(movie['id'])
        movieDel.delete()

    def test_updateMovieDoesNotExist_fail(self):
        result = self.client.patch('/movies/999999', headers=self.authHeaderEP,
                                   data=json.dumps(dict(
                                       title="freddyasdfasdf")),
                                   content_type='application/json')
        self.assertEqual(404, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Resource Not Found", result.json['errorCode'])

    def test_deleteMovie_success(self):
        result = self.client.post('/movies', headers=self.authHeaderEP,
                                  data=json.dumps(dict(
                                      title="freddyasdfMovie",
                                      releaseDate="07/05/1977")),
                                  content_type='application/json')
        self.assertEqual(200, result.status_code)
        movie = result.json['movie']
        print(movie)
        result = self.client.delete('/movies/' + str(movie['id']),
                                    headers=self.authHeaderEP)
        self.assertEqual(200, result.status_code)
        self.assertEqual(movie['id'], result.json['movieId'])
        self.assertTrue(result.json['success'])

    def test_deleteMovieDoesNotExist_fail(self):
        result = self.client.delete('/movies/999999',
                                    headers=self.authHeaderEP)
        self.assertEqual(404, result.status_code)
        self.assertFalse(result.json['success'])
        self.assertEqual("Resource Not Found", result.json['errorCode'])

    def test_assistant_getActors_success(self):
        result = self.client.get('/actors',
                                 headers=self.authHeaderCA)
        self.assertEqual(200, result.status_code)

    def test_assistant_postActors_success(self):
        result = self.client.post('/actors',
                                  headers=self.authHeaderCA)
        self.assertEqual(401, result.status_code)

    def test_assistant_patchActors_success(self):
        result = self.client.patch('/actors/1',
                                   headers=self.authHeaderCA)
        self.assertEqual(401, result.status_code)

    def test_assistant_deleteActors_success(self):
        result = self.client.delete('/actors/1',
                                    headers=self.authHeaderCA)
        self.assertEqual(401, result.status_code)

    def test_assistant_getMovies_success(self):
        result = self.client.get('/movies',
                                 headers=self.authHeaderCA)
        self.assertEqual(200, result.status_code)

    def test_assistant_postMovies_success(self):
        result = self.client.post('/movies',
                                  headers=self.authHeaderCA)
        self.assertEqual(401, result.status_code)

    def test_assistant_patchMovies_success(self):
        result = self.client.patch('/movies/1',
                                   headers=self.authHeaderCA)
        self.assertEqual(401, result.status_code)

    def test_assistant_deleteMovies_success(self):
        result = self.client.delete('/movies/1',
                                    headers=self.authHeaderCA)
        self.assertEqual(401, result.status_code)

    def test_director_getActors_success(self):
        result = self.client.get('/actors',
                                 headers=self.authHeaderCD)
        self.assertEqual(200, result.status_code)

    # all three test post/patch/delete done at once for database integrity
    def test_director_postPatchDeleteActors_success(self):
        result = self.client.post('/actors', headers=self.authHeaderCD,
                                  data=json.dumps(dict(
                                      name="freddyasdf",
                                      age=123,
                                      gender='F')),
                                  content_type='application/json')
        self.assertEqual(200, result.status_code)
        actor = result.json['actor']
        result = self.client.patch('/actors/' + str(actor['id']),
                                   headers=self.authHeaderCD,
                                   data=json.dumps(dict(
                                       name="freddyasdfasdf")),
                                   content_type='application/json')
        self.assertEqual(200, result.status_code)
        result = self.client.delete('/actors/' + str(actor['id']),
                                    headers=self.authHeaderCD)
        self.assertEqual(200, result.status_code)

    def test_director_getMovies_success(self):
        result = self.client.get('/movies',
                                 headers=self.authHeaderCD)
        self.assertEqual(200, result.status_code)

    def test_director_postMovies_success(self):
        result = self.client.post('/movies',
                                  headers=self.authHeaderCD)
        self.assertEqual(401, result.status_code)

    def test_director_deleteMovies_success(self):
        result = self.client.delete('/movies/1',
                                    headers=self.authHeaderCD)
        self.assertEqual(401, result.status_code)

    def getDataSetForActor(self, actors, name):
        for actor in actors:
            if actor['name'] == name:
                return actor
        return None

    def getDataSetForMovie(self, movies, title):
        for movie in movies:
            if movie['title'] == title:
                return movie
        return None


if __name__ == "__main__":
    unittest.main()
