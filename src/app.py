"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200
#listar usuarios
@app.route('/users', methods=['GET'])
def list_users():
    try:
        # aqui estoy con sultado  todos los registros de la tabla User
        users = User.query.all()
        print(users)
        if not users:
            raise APIException("No hay registros en la base de datos", status_code=404)
        
        # aqui serializo los datos usando el método `serialize` definido en el modelo
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        # En caso de error, lanzar una excepción con el mensaje
        raise APIException(str(e))
    

#listar people
@app.route('/people', methods=['GET'])
def list_people():
    try:
        people = People.query.all()
        if not people:
            raise APIException("no hay regstros de personas en la base de datos", status_code=404)
        return jsonify([person.serealize() for person in people]), 200
    except Exception as e:
        raise APIException(str(e)) 
       
#identificar people por su id
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_by_id(people_id):
    try:
        #consulta un people por su id
        person = People.query.get(people_id)

        if not person:
            raise APIException("Persona con ID {people_id} no encontrado", status_code=404)
        #serializar y devolver el usuario
        return jsonify(person.serialize()), 200
    except Exception as e:
        #menejo de error
        raise APIException(str(e))

#listar planetas
@app.route('/planets', methods=['GET'])
def list_planets():
    try:
        planets = Planet.query.all()

        if not planets:
            raise APIException("No hay registros de planetas en la base de datos", status_code=404)
        return jsonify([planet.serialize() for planet in planets]), 200
    except Exception as e:
        raise APIException(str(e))     

#identificar planetas por su id
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    try:
        planet = Planet.query.get(planet_id)

        if not planet:
            raise APIException(f"Planeta con ID {planet_id} no encontrado", status_code=404)
        return jsonify(planet.serialize()), 200
    except Exception as e:
        raise APIException(str(e))

#asociar un usuario con favorito    
@app.route('/users/<int:user_id>/favorites', methods=['GET']) 
def get_user_favorites(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            raise APIException(f"Usuario con ID {user_id} no encontrado", status_code=404)
        
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        if not favorites:
            raise APIException(f"No se encontraron favoritos para el usuario con ID {user_id}", status_code=404)
        
        return jsonify([favorite.serialize() for favorite in favorites]), 200
    except Exception as e:
        raise APIException(str(e))
    

#asociar un planeta con favorito
@app.route('/favorites/planets/<int:planet_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    try:
        #virifica si el usuario existe
        user = User.query.get(user_id)
        if not user:
            raise APIException(f"Usuario con ID {user_id} no encontrado",status_code=404)

        #verifica si el planeta existe
        planet = Planet.query.get(planet_id)
        if not planet:
            raise APIException(f"Planeta con ID {planet_id} no encontrado", status_code=404)
        
        #verifica si el favorito ya existe
        existing_favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if existing_favorite:
            raise APIException(f"El planeta con ID {planet_id} ya está en los favoritos del usuario", status_code=400)

        #create un nuevo favorito
        new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()


        return jsonify({
            "msg": f"Planeta con ID {planet_id} añadido a los favoritos del usuario con ID {user_id}"
        }),201
    except Exception as e:
        raise APIException(str(e))


#asociar people con favorito
@app.route('/favorites/people/<int:people_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):
    try:
        #verifico si el usuario existe
        user = User.query.get(user_id)
        if not user:
            raise APIException(f"Usuario con ID {user_id} no encontrado",status_code=404)
        #verifico si el personaje existe
        people = People.query.get(people_id)
        if not people:
            raise APIException(f"Personaje con ID {people_id} no encontrado", status_code=404)

        #verifacar si el favorito ya existe
        existing_favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
        if existing_favorite:
            raise APIException(f"El personaje con ID {people_id} ya está en los favoritos del usuario con ID {user_id}", status_code=400)

        #creo un nuevo favorito
        new_favorite = Favorite(user_id=user_id, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({
            "msg": f"People con ID {people_id} añadido a los favoritos del usuario con ID {user_id}"
        }),201
    except Exception as e:
        raise APIException(str(e)) 
    
#delete people
@app.route('/favorites/people/<int:people_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    try:
        #verifico si existe el usurio
        user = User.query.get(user_id)
        if not user:
            raise APIException(f"Usuario con ID {user_id} no encontrado", status_code=404)

        #verifico si el personaje favorito existe para este usuario
        favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first() 
        if not favorite:
            raise APIException(f"El personaje con ID {people_id} no está en los favoritos del usuario con ID {user_id}", status_code=404)

        #elimino favorito
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({
            "msg": f"Personaje con ID {people_id} eliminado de los favoritos del usuario con ID {user_id}"
        }),200
    except APIException as e:
        raise APIException(str(e))

#delete planet 
@app.route('/favorites/planets/<int:planet_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    try:
        #vericar si existe el usuario
        user = User.query.get(user_id)
        if not user:
            raise APIException(f"Usuario con ID {user_id} no encontrado", status_code=404)


        #verifacamos si el planeta existe para este usuario
        favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if not favorite:
            raise APIException(f"El planeta con ID {planet_id} no está en los favoritos del usuario con ID {user_id}", status_code=404)

        #eliminar el favorito de la base de datos
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({
            "msg": f"Planeta con ID {planet_id} eliminado de los favoritos del usuario con ID {user_id}"

        }),200
    except APIException as e:
         raise APIException(str(e))
       


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
