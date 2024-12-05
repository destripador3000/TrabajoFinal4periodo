# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from datetime import datetime
from models import Prestamo, db, Libro, Usuario, Estudiante  # Importa db desde models.py

app = Flask(__name__)
app.config.from_object(Config)

# Usa la instancia de db ya definida en models.py
db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/', methods=['GET', 'POST'])
def logginPrincipal():
    if request.method == 'POST':
        # Aquí se podrían validar las credenciales más tarde.
        return redirect(url_for('index'))  # Redirigir a la página principal después del login.
    return render_template('loggin.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/registrar_prestamo', methods=['GET', 'POST'])
def registrar_prestamo():
    if request.method == 'POST':
        libroCodigo = request.form.get('libro')
        codigo = request.form.get('codigo')  # El código del estudiante
        nombre=request.form.get('nombre') #Nombre del estudiante
        fecha = request.form.get('fecha')

        # Validar la fecha
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            flash('Fecha no válida. Usa el formato YYYY-MM-DD.', 'danger')
            return redirect(url_for('registrar_prestamo'))

        # Verificar si el código del estudiante existe en la base de datos
        c_estudiante = Estudiante.query.filter_by(codigo=codigo).first()  # Consultamos por el código del estudiante
        n_estudiante = Estudiante.query.filter_by(nombre=nombre).first() 
      
    
        if not c_estudiante and n_estudiante:
            flash('El estudiante no existe en la base de datos.', 'danger')
            return "El estudiante no existe en la base de datos."
        libroCodigo = int(libroCodigo) 
        libro = Libro.query.filter_by(codigo=libroCodigo).first()
        if not libro:
            flash('El libro no existe en la base de datos.', 'danger')
            return 'No existe el libro en la base de datos.'

        nuevo_prestamo = Prestamo(libro=libro.codigo, usuario=c_estudiante.nombre, fecha=fecha)
        db.session.add(nuevo_prestamo)
        db.session.commit()

        flash('Préstamo registrado con éxito.', 'success')
        return redirect(url_for('registrar_prestamo'))


    # Si es una solicitud GET, solo se renderiza el formulario
    prestamos = Prestamo.query.all()
    return render_template('prestamos.html', prestamos=prestamos)
   
@app.route('/registrar_multa', methods=['GET', 'POST'])
def registrar_multa():
    if request.method == 'POST':
        flash('Multa registrada con éxito.')
        return redirect(url_for('index'))
    return render_template('multas.html')


@app.route('/informacionLibro', methods=['GET', 'POST'])
def mostrarInformacion():
    return render_template('informacionLibro.html')

@app.route('/registrarPrestamos', methods=['GET', 'POST'])
def registrarPrestamos():
    if request.method == 'POST':
        flash('Préstamo registrado con éxito.')
        return redirect(url_for('index'))
    return render_template('registrarPrestamos.html')


@app.route('/eliminarPrestamos', methods=['GET', 'POST'])
def eliminarPrestamos():
    if request.method == 'POST':
        prestamo_id = request.form.get('codigo')  # Recoge el ID o código del préstamo desde el formulario
        # Validar que el campo no esté vacío y sea numérico
        if not prestamo_id or not prestamo_id.isdigit():
            flash('Por favor, ingresa un ID válido.', 'danger')
            return redirect(url_for('prestamos'))
        # Buscar el préstamo en la base de datos
        prestamo = Prestamo.query.filter_by(id=prestamo_id).first()
        if prestamo:
            # Eliminar el préstamo
            db.session.delete(prestamo)
            db.session.commit()
            return 'Préstamo eliminado con éxito.'
        else:
            # Si no se encuentra el préstamo
            return 'Préstamo no encontrado.'
      
    # Renderizar el formulario de eliminación
    return render_template('consultarPrestamo.html')

@app.route('/consultarPrestamo', methods=['GET', 'POST'])
def consultarPrestamo():
    # Consultar únicamente los datos de la tabla Prestamo
    prestamos = db.session.query(
        Prestamo.id.label('id'),
        Prestamo.libro.label('libro'),  # Aquí obtienes el identificador del libro
        Prestamo.usuario.label('usuario'),
        Prestamo.fecha.label('fecha')
    ).all()
    
    # Renderizar la plantilla con los datos
    return render_template('consulta.html', prestamos=prestamos)

   
@app.route('/modificarPrestamo', methods=['GET', 'POST'])
def modificarPrestamo():
    if request.method == 'POST':
        flash('Préstamo modificado con éxito.')
        return redirect(url_for('index'))
    return render_template('modificarPrestamo.html')

@app.route('/loggin', methods=['GET', 'POST'])
def loggin():
    if request.method == 'POST':
        codigo = request.form.get("codigo")
        password = request.form.get("password")
        # Consulta en la base de datos para verificar las credenciales
        usuario = Usuario.query.filter_by(codigo=codigo, password=password).first()
        if usuario:
            # Si las credenciales son correctas, redirige al index
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else: 
            flash('Código o contraseña incorrectos', 'danger')

    return render_template('loggin.html')


@app.route('/buscar', methods=['GET', 'POST'])
def buscarLibro():
    libro = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        # Buscar el libro en la base de datos
        libro = Libro.query.filter_by(nombre=nombre).first()
        return render_template('libros.html', libro=libro)
    else:
        return "No existe el libro"
    

@app.route('/gestionLibro', methods=['GET', 'POST'])
def gestionLibro():
    if request.method == 'POST':
        return redirect(url_for('index')) 
    return render_template('gestionLibro.html')

@app.route('/agregarLibro', methods=['GET', 'POST'])
def agregarLibro():
    
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nombre = request.form.get('nombre')
        autor = request.form.get('autor')
        # Crear una nueva instancia del modelo Libro
        nuevo_libro = Libro(codigo=codigo, nombre=nombre, autor=autor, disponibilidad='si')  # Incluye 'disponibilidad' si es relevante
    
        db.session.add(nuevo_libro)
        db.session.commit()
    
        print(f"El codigo es {codigo} nombre: {nombre} autor: {autor}")
       
    return render_template('agregarLibro.html')



@app.route('/eliminarLibro', methods=['GET', 'POST'])
def eliminarLibro():
    if request.method == 'POST':
        # Obtener el código del libro desde el formulario
        codigo = request.form.get('codigo')  # El campo en el formulario es "Préstamo"
        # Validar que el código no esté vacío
        if not codigo:
            return "Por favor ingresa un código de libro válido", 400
        try:
            # Buscar el libro en la base de datos por código
            libro = Libro.query.filter_by(codigo=codigo).first()  # Filtrar por el código
            # Verificar si el libro existe
            if not libro:
                return "El libro con ese código no existe", 404
            # Eliminar el libro
            db.session.delete(libro)
            db.session.commit()  # Realizar la transacción en la base de datos
            flash("El libro ha sido eliminado", "danger")
            return redirect(url_for('index'))  # Redirigir a la página principal después de eliminar el libro
        except Exception as e:
            # Si ocurre un error, devolver un mensaje
            return f"Error al eliminar el libro: {str(e)}", 500
    return render_template('eliminarLibro.html')



@app.route('/modificarLibro', methods=['GET', 'POST'])
def modificarLibro():
    if request.method == 'POST':
        return redirect(url_for('index')) 
    return render_template('modificarLibro.html')

@app.route('/consultarLibro', methods=['GET', 'POST'])
def consultarLibro():
    if request.method == 'POST':
        return redirect(url_for('index')) 
    return render_template('consultarLibro.html')



if __name__ == '__main__':
    app.run(debug=True)
