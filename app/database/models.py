import os
from sqlalchemy import Column, String, Integer, CHAR
from flask_sqlalchemy import SQLAlchemy

database_file = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_file))

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def addTestData():
    print("adding")
    actor = Actor()
    actor.name = "billyasdf"
    actor.age = "32"
    actor.gender = "M"
    actor.add()
    actor = Actor()
    actor.name = "jimmyasdf"
    actor.age = "64"
    actor.gender = "M"
    actor.add()
    actor = Actor()
    actor.name = "samasdf"
    actor.age = "21"
    actor.gender = "F"
    actor.add()
    movie = Movie()
    movie.title = "billyasdfMovie"
    movie.releaseDate = "12/25/2002"
    movie.add()
    movie = Movie()
    movie.title = "jimmyasdfMovie"
    movie.releaseDate = "01/14/2022"
    movie.add()
    movie = Movie()
    movie.title = "samasdfMovie"
    movie.releaseDate = "03/02/1978"
    movie.add()


def deleteTestData():
    print("deleting")
    actor = Actor.query.filter_by(name="jimmyasdf").first()
    actor.delete()
    actor = Actor.query.filter_by(name="billyasdf").first()
    actor.delete()
    actor = Actor.query.filter_by(name="samasdf").first()
    actor.delete()
    movie = Movie.query.filter_by(title="jimmyasdfMovie").first()
    movie.delete()
    movie = Movie.query.filter_by(title="billyasdfMovie").first()
    movie.delete()
    movie = Movie.query.filter_by(title="samasdfMovie").first()
    movie.delete()

def resetDb():
    print("reseting")
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(160), unique=True)
    releaseDate = Column(String(10))

    def toString(self):
        return {
            'id': self.id,
            'title': self.title,
            'releaseDate': self.releaseDate
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), unique=True)
    age = Column(Integer)
    gender = Column(CHAR)

    def toString(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()






