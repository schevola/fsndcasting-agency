# Casting Agency

##Introduction(Motivation)
Casting Agency is an application that will facilitate the organization of movie production, and casting talent.
Making it quicker and easier to find talen to fill rolls for up and coming movies.

## Getting Started

### Install Dependancies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server

From within the `./` directory
To run the server, execute:
```bash
python run.py
```

## To Test the end points with [Postman](https://getpostman.com). 
- Import the postman collection `./CastingAgency.postman_collection.json`
- Run the collection runner with the CastingAgency Collection, tests are setup to store ids, for patch and delete process when required

ServerUrl:
https://fsndcasting-agency.herokuapp.com

Endpoints
```
GET    '/'                      no restirctions
GET    '/actors'                must have get:actors permissions
POST   '/actors'                must have post:actors permissions
PATCH  '/actors/{actorId}'      must have patch:actors permissions
DELETE '/actors/{actorId}'      must have delete:actors permissions
GET    '/movies'                must have get:movies permissions
POST   '/movies'                must have post:movies permissions
PATCH  '/movies/{movieId}'      must have patch:movies permissions
DELETE '/movies/{movieId}'      must have delete:movies permissions

GET    '/'
    - Checks if the server is running
    - sample output:
        {
            "action": "Healthy",
            "success": true
        }
        
        
GET    '/actors'
    - Fetches a list of all the actors in the database
    - sample output:
        {
            "actors": [
                {
                    "age": 65,
                    "gender": "M",
                    "id": 1,
                    "name": "Billy Bob"
                }
            ],
            "success": true
        }
        
        
POST   '/actors'
    - Adds an actor with the provided information to the database
    - Sample input:
        {
            "name": "Jessica Rabbit",
            "age": 22,
            "gender": "F"
        }
    - sample output:
        {
            "actor": {
                "age": 22,
                "gender": "F",
                "id": 2,
                "name": "Jessica Rabbit"
            },
            "success": true
        }
        
        
PATCH  '/actors/{actorId}'
    - Updates the actors information with the given actorId
    - Sample input:
        {
            "name": "Roger Rabbit",
            "age": 23,
            "gender": "M"
        }
    - Sample output:
        {
            "actor": {
                "age": 23,
                "gender": "M",
                "id": 2,
                "name": "Roger Rabbit"
            },
            "success": true
        }
    
DELETE '/actors/{actorId}'
     - Deletes the actors information with the given actorId
     - Sample output:
        {
            "actorId": 2,
            "success": true
        }
        
GET    '/movies'
    - Fetches a list of all the moives in the database
    - sample output:
        {
            "movies": [
                {
                    "id": 1,
                    "releaseDate": "05/01/1988",
                    "title": "Ghost Jailers"
                }
            ],
            "success": true
        }
        
        
POST   '/movies'
    - Adds a movie with the provided information to the database
    - Sample input:
        {
            "title": "Ghost Jailers II",
            "releaseDate": "05/01/1992"
        }
    - sample output:
        {
            "movie": {
                "id": 2,
                "releaseDate": "05/01/1992",
                "title": "Ghost Jailers II"
            },
            "success": true
        }

PATCH  '/movies/{movieId}'
    - Updates the actors information with the given actorId
    - Sample input:
        {
            "title": "Ghost Jailers III",
            "releaseDate": "05/09/1992"
        }
    - Sample output:
        {
            "actor": {
                "title": "Ghost Jailers III",
                "releaseDate": "05/09/1992",
                "id": 2
            },
            "success": true
        }
        
DELETE '/movies/{movieId}'
    - Deletes the movie information with the given actorId
    - Sample output:
        {
            "movieId": 2,
            "success": true
        }
```

###Authentication
```
This application uses Auth0 for authentication, the follow tokens will grant access to the given roles
Casting Agent
    permissions: 
        get:actors
        get:movies
    Token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVZclR5NG04ZmIwbVZGWmtRVl9EUSJ9.eyJpc3MiOiJodHRwczovL3NjaGV2b2xhLWNvZmZlZS1zaG9wLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDU5MjIzZDhhMjRkNzAwNzBlZmUwNGMiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNjE2NDgzNjI0LCJleHAiOjE2MTY1NzAwMjQsImF6cCI6Ikl6NXpPR1hXWm03Sk1VbDVRYm1XUWZuQUFJMGU2MEpGIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.k-vyNoj0sP2aCKi-6IEtSkiJTpz6D2wOz-j91dQSeuPnafGyPIUOhsGFPoW51lo9rMrZs6iZ7nPkRi-xsf9xhS0DU3QgZz1Rh3qwx_mYlzC16GljQ1qNVn8h_mGXWgX-40i6aYo-YLd2oVZ1nycNRI2s5XcJfiBS_r9XFOSa_euDSn7yNcLBAgJnnMFabGKs_V7WtpEr6Xpm-GUufWL-3LFx8nWS5NGy2SCmRwa9XYReCuhmynIMRJPBGKPpfesw2yh26ZG9TOe1z8Yvs_LaKPbKoQSS4Y31_O3idd3YxjN5f0Bp-xsDUSUBO7lJ99-8lqngg2EIpTr1JPXaRlVWCw
    
Casting Director
    permissions:
        get:actors
        get:movies
        post:actors
        patch:actors
        delete:actors
        patch:movies 
    Token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVZclR5NG04ZmIwbVZGWmtRVl9EUSJ9.eyJpc3MiOiJodHRwczovL3NjaGV2b2xhLWNvZmZlZS1zaG9wLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDU5MjFkNmVhNDM3ZTAwNjg2M2ViNjYiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNjE2NDgzNzUxLCJleHAiOjE2MTY1NzAxNTEsImF6cCI6Ikl6NXpPR1hXWm03Sk1VbDVRYm1XUWZuQUFJMGU2MEpGIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.mJSOwFgqp4y3Sq1qIY4lkEtPni4XT0Psm9d7DSu7sVo4JgSfI7RlWjYVRNz5W_qOxKJlzL3TLtJDCcgbdopsw2gupod6u_K7Ven6vVcc2oi75Q_ggzQZFAa2ijL8xXSNwf9mPV7Ix7l9MVGms_F_LqAH_LwWm3kuUiWsYn4OLFoG2qmLGgyQ8Bi-KTZnJqi9UESfKrhGsD_PksTAhZ0ctrg8jZaOAsREv7uOFBff3OthWG2mzf3MsK7SfZTSxcgmaTg7W_DlD-wqQ_VFWumJU-PUl_l5ZAJBOCE1QFmXMjs1nFYGnUEisml47sv7kby7EUH7NIoPWv6FVO3pPTMkAg
    
Executive Producer:
    permissions:
        get:actors
        get:movies
        post:actors
        patch:actors
        delete:actors
        post:movies
        patch:movies
        delete:movies
    Token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVZclR5NG04ZmIwbVZGWmtRVl9EUSJ9.eyJpc3MiOiJodHRwczovL3NjaGV2b2xhLWNvZmZlZS1zaG9wLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDU5MjIwYTNhZDU3YTAwNjkxZmIzMWIiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNjE2NDgzODQ2LCJleHAiOjE2MTY1NzAyNDYsImF6cCI6Ikl6NXpPR1hXWm03Sk1VbDVRYm1XUWZuQUFJMGU2MEpGIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.blTUDYzqDBGfg2lNAS5qL6SAOv98Ql-rgGPx_rrmWW7sYTV4ouRuM9sb28fZXEBNg_XDRczeE_bvBXDX1tWwYg0OUxAls_mRkanC3Io_bwNrfNR9cjowYwYBgYvd_3txRdf4vE6usP7f1leKOuETQsrtSJqRlmvaFSm0OsuqCUJyAkVUebkbGWcoY-P5nnL2ajaNZ7fc01KFMWd6Wh6Lh_3bo8dALICyzuwASCyq0gvCesbC5beP3zf38tejuOlPZXkjfBrUywcrSPnGtfmE_8SgJHZoQvYW1OZVhfKeYe4IW8H7FTVEBSp_Vk8itGIYPeA_osIFmaPssGt-U_9-Mg
```


####NOTES for reviewer
For get actors and get movies there is not error flow tests because if there are no actors or movies an empty list is returned, there is not error logic in those flows

All Rbac tests are done in postman
