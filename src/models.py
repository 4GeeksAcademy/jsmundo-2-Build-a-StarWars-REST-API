from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite', back_populates='user', cascade='all, delete')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            
            # do not serialize the password, its a security breach
        }
        #tabala people
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.String(50))
    mass = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    ski_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    homeworld = db.Column(db.String(120))
    description = db.Column(db.Text, nullable=True)
    favorites = db.relationship('Favorite', back_populates='people', cascade='all, delete')  

    def __repr__(self):
        return f'<people {self.name}>'      
    
    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.ski_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "description": self.description,
            
        }
#tabla planet
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    population = db.Column(db.String(50))
    diameter = db.Column(db.String(50))
    rotation_period = db.Column(db.String(50))
    orbital_period = db.Column(db.String(50))
    favorites = db.relationship('Favorite', back_populates='planet', cascade='all, delete')

    def __repr__(self):
        return f'<planet {self.name}>'

    def serialize(self):
        return{
         "id": self.id,
        "name": self.name,
        "climate": self.climate,
        "terrain": self.terrain,
        "population": self.population,
        "diameter": self.diameter,
        "rotation_period": self.rotation_period,
        "orbital_period": self.orbital_period,

        }

 #tabla favorite   
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user = db.relationship('User', back_populates='favorites')
    people = db.relationship('People', back_populates='favorites')
    planet = db.relationship('Planet', back_populates='favorites')

    def __repr__(self):
        return f'<Favorite User: {self.user_id}, People: {self.people_id}, Planet: {self.planet_id} >'
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "people": self.people_id,
            "planet": self.Planet_id,

        }
            