from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/libreria'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

class Autores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    nacionalidad = db.Column(db.String(100))

class Libros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'))
    fecha_obra = db.Column(db.Date)
    resumen = db.Column(db.Text)
    autor = db.relationship('Autores', backref='libros')


def autor_to_dict(autor):
    autor_dict = {
        'id': autor.id,
        'nombre': autor.nombre,
        'nacionalidad': autor.nacionalidad
    }
    return autor_dict

@app.route('/autores', methods=['GET'])
def get_autores():
    autores = Autores.query.all()
    autores_data = [autor_to_dict(autor) for autor in autores]
    return jsonify(autores_data)

@app.route('/autores/<int:autor_id>', methods=['GET'])
def get_autor(autor_id):
    autor = Autores.query.get(autor_id)
    if autor is None:
        return jsonify({'error': 'Autor no encontrado'}), 404

    autor_dict = {
        'id': autor.id,
        'nombre': autor.nombre,
        'nacionalidad': autor.nacionalidad 
    }

    return jsonify(autor_dict)


@app.route('/autores', methods=['POST'])
def create_autor():
    data = request.json
    autor = Autores(nombre=data['nombre'], nacionalidad=data['nacionalidad'])
    db.session.add(autor)
    db.session.commit()
    return jsonify({'message': 'Autor creado con éxito', 'id': autor.id})

def libro_to_dict(libro):
    libro_dict = {
        'id': libro.id,
        'titulo': libro.titulo,
        'autor_id': libro.autor_id,
        'fecha_obra': libro.fecha_obra,
        'resumen': libro.resumen
    }
    return libro_dict

@app.route('/libros', methods=['GET'])
def get_libros():
    libros = Libros.query.all()
    libros_data = [libro_to_dict(libro) for libro in libros]
    return jsonify(libros_data)

@app.route('/libros/<int:libro_id>', methods=['GET'])
def get_libro(libro_id):
    libro = Libros.query.get(libro_id)
    if libro is None:
        return jsonify({'error': 'Libro no encontrado'}), 404

    libro_data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'autor_id': libro.autor_id,
        'fecha_obra': libro.fecha_obra,
        'resumen': libro.resumen
    }

    return jsonify(libro_data)

@app.route('/libros/autor/<int:autor_id>', methods=['GET'])
def get_libros_by_autor(autor_id):
    libros = Libros.query.filter_by(autor_id=autor_id).all()
    
    if not libros:
        return jsonify({'error': 'No se encontraron libros para este autor'}), 404
    
    libros_data = [
        {
            'id': libro.id,
            'titulo': libro.titulo,
            'autor_id': libro.autor_id,
            'nombre_autor': libro.autor.nombre,
            'fecha_obra': libro.fecha_obra,
            'resumen': libro.resumen 
        }
        for libro in libros
    ]

    return jsonify(libros_data)

@app.route('/libros', methods=['POST'])
def create_libro():
    data = request.json
    # print('titulo', data['titulo'] )
    libro = Libros(titulo=data['titulo'], autor_id=data['autor_id'], fecha_obra=data['fecha_obra'], resumen=data['resumen'])
    db.session.add(libro)
    db.session.commit()
    return jsonify({'message': 'Libro creado con éxito', 'id': data['titulo']})

@app.route('/autores/<int:autor_id>', methods=['PUT'])
def update_autor(autor_id):
    # Obtener el autor a actualizar desde la base de datos
    autor = Autores.query.get(autor_id)

    if autor is None:
        return jsonify({'message': 'Autor no encontrado'}), 404

    # Actualizar los datos del autor con los valores proporcionados en la solicitud
    autor.nombre = request.json.get('nombre', autor.nombre)
    autor.nacionalidad = request.json.get('nacionalidad', autor.nacionalidad)

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({'message': 'Autor actualizado con éxito'})

@app.route('/libros/<int:libro_id>', methods=['PUT'])
def update_libro(libro_id):
    # Obtener el libro a actualizar desde la base de datos
    libro = Libros.query.get(libro_id)

    if libro is None:
        return jsonify({'message': 'Libro no encontrado'}), 404

    # Actualizar los datos del libro con los valores proporcionados en la solicitud
    libro.titulo = request.json.get('titulo', libro.titulo)
    # libro.autor_id = request.json.get('autor_id', libro.autor_id)

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({'message': 'Libro actualizado con éxito'})

@app.route('/autores/<int:autor_id>', methods=['DELETE'])
def delete_autor(autor_id):
    # Obtener el autor a eliminar desde la base de datos
    autor = Autores.query.get(autor_id)

    if autor is None:
        return jsonify({'message': 'Autor no encontrado'}), 404

    # Eliminar el autor de la base de datos
    db.session.delete(autor)
    db.session.commit()

    return jsonify({'message': 'Autor eliminado con éxito'})

@app.route('/libros/<int:libro_id>', methods=['DELETE'])
def delete_libro(libro_id):
    # Obtener el libro a eliminar desde la base de datos
    libro = Libros.query.get(libro_id)

    if libro is None:
        return jsonify({'message': 'Libro no encontrado'}), 404

    # Eliminar el libro de la base de datos
    db.session.delete(libro)
    db.session.commit()

    return jsonify({'message': 'Libro eliminado con éxito'})

if __name__ == '__main__':
    app.run(debug=True)