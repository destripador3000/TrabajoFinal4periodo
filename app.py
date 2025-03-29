# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from datetime import datetime
from models import Prestamo, db, Libro, Usuario, Estudiante, Multa,Devolucion # Importa db desde models.py

app = Flask(__name__)
app.config.from_object(Config)

# Usa la instancia de db ya definida en models.py
db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/', methods=['GET', 'POST'])
def logginPrincipal():
    if request.method == 'POST':
        # Aquí se validan las credenciales
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
        fecha = request.form.get('fecha') #fecha de creación
        correo = request.form.get('correo') #correo del estudiante
        # Validar la fecha
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            flash('Fecha no válida. Usa el formato YYYY-MM-DD.', 'danger')
            return redirect(url_for('registrar_prestamo'))

        # Verificar si el código del estudiante existe en la base de datos
        c_estudiante = Estudiante.query.filter_by(codigo=codigo).first()  # Consultamos por el código del estudiante

    
        if not c_estudiante:
            flash('El estudiante no existe en la base de datos.', 'danger') # aqui se genera el aviso de alerta si no existe el estudiante
            return "El estudiante no existe en la base de datos."
        libroCodigo = int(libroCodigo) 
        libro = Libro.query.filter_by(codigo=libroCodigo).first()
        if not libro:
            flash('El libro no existe en la base de datos.', 'danger')
            return redirect(url_for('registrar_prestamo'))

        nuevo_prestamo = Prestamo(libro=libro.codigo, usuario=c_estudiante.nombre, fecha=fecha, correo=correo)
        db.session.add(nuevo_prestamo)
        db.session.commit()

        flash('Préstamo registrado con éxito.', 'success') #aqui se genera el aviso de alerta si el prestamo se registra exitosamente
        return redirect(url_for('registrar_prestamo'))


    # Si es una solicitud GET, solo se renderiza el formulario
    prestamos = Prestamo.query.all()
    return render_template('prestamos.html', prestamos=prestamos)
   
@app.route('/registrar_multa', methods=['GET', 'POST'])
def registrar_multa():
    if request.method == 'POST':
        libro = request.form.get('libro')  # Código del libro
        estudiante = request.form.get('estudiante')  # Nombre del estudiante
        codigo = request.form.get('codigo')  # Código del estudiante
        fecha_creacion = request.form.get('fecha_creacion')  # Fecha de creación de la multa
        fecha_creacion = datetime.strptime(fecha_creacion, '%Y-%m-%d')
        # Crear la nueva multa
        nueva_multa = Multa(libro=libro, usuario=estudiante, codigo=codigo, fecha_creacion=fecha_creacion)
        db.session.add(nueva_multa)
        db.session.commit()

        # Mensaje de éxito
        flash('Multa registrada con éxito.', 'success')
        return redirect(url_for('consultarMulta'))  # Redirigir a la vista de consultar multas
        
    multas = Multa.query.all()
        
    return render_template('multas.html', multas=multas) #Renderiza a la pagina de multas

@app.route('/gestionMulta', methods=['GET', 'POST'])
def gestionMulta():
    if request.method == 'POST':
        flash('Multa registrada con éxito.')
        return redirect(url_for('index'))
    return render_template('gestionMulta.html')

@app.route('/eliminarMulta', methods=['GET', 'POST'])
def eliminarMulta():
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
    return render_template('eliminarMulta.html')

@app.route('/consultarMulta', methods=['GET', 'POST'])
def consultarMulta():
    # Consultar únicamente los datos de la tabla Prestamo
    multa = db.session.query(
        Multa.id.label('id'),
        Multa.libro.label('libro'), 
        Multa.usuario.label('usuario'),
        Multa.codigo.label('codigo'),
        Multa.fecha_creacion.label('fecha_creacion')

    ).all()
    
    # Renderizar la plantilla con los datos
    return render_template('consultarMulta.html', multa=multa)  #Aqui renderiza a la pagina de Consultar la multa.


@app.route('/informacionLibro', methods=['GET', 'POST'])
def mostrarInformacion():
    return render_template('informacionLibro.html') #Aqui devuelve la información del

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
        Prestamo.fecha.label('fecha'),
        Prestamo.correo.label('correo')
    ).all()
    
    # Renderizar la plantilla con los datos
    return render_template('consulta.html', prestamos=prestamos)


@app.route('/modificarPrestamo', methods=['GET', 'POST'])
def modificarPrestamo():
    prestamo = None
    
    if request.method == 'POST':
        if 'buscar' in request.form:
            id_prestamo = request.form['id_prestamo']
            prestamo = Prestamo.query.get(id_prestamo)
            if not prestamo:
                flash('ID de préstamo no encontrado.', 'danger')
        elif 'modificar' in request.form:
            id_prestamo = request.form['id_prestamo']
            prestamo = Prestamo.query.get_or_404(id_prestamo)
            
            prestamo.libro = request.form['libro']
            prestamo.usuario = request.form['usuario']
            prestamo.fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
            prestamo.correo = request.form['correo']
            
            db.session.commit()
            flash('Préstamo modificado con éxito.', 'success')
            return redirect(url_for('index'))
    
    return render_template('modificarPrestamo.html', prestamo=prestamo)

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
        genero=request.form.get('genero')
        # Crear una nueva instancia del modelo Libro
        nuevo_libro = Libro(codigo=codigo, nombre=nombre, autor=autor, disponibilidad='si',genero=genero) 
        
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
    libro = None  # Inicializamos la variable para el renderizado del template

    if request.method == 'POST':
        if 'buscar' in request.form:  # Si se busca un libro por ID
            id_libro = request.form['id_libro']
            libro = Libro.query.get(id_libro)

            if not libro:
                flash('ID de libro no encontrado.', 'danger')

        elif 'modificar' in request.form:  # Si se envían datos para modificar
            id_libro = request.form['id_libro']
            libro = Libro.query.get_or_404(id_libro)

            libro.codigo = request.form['codigo']
            libro.nombre = request.form['nombre']
            libro.autor = request.form['autor']
            libro.disponibilidad = request.form['disponibilidad']
            libro.genero = request.form['genero']

            db.session.commit()
            flash('Libro modificado con éxito.', 'success')
            return redirect(url_for('index'))

    return render_template('modificarLibro.html', libro=libro)


@app.route('/consultarLibro', methods=['GET', 'POST'])
def consultarLibro():
    if request.method == 'POST':
        return redirect(url_for('index')) 
    return render_template('consultarLibro.html')


@app.route('/consultarLibro2', methods=['GET', 'POST'])
def consultarLibro2():
    # Consultar únicamente los datos de la tabla Prestamo
    libro = db.session.query(
        Libro.id.label('id'),
        Libro.codigo.label('codigo'),
        Libro.nombre.label('nombre'),  # Aquí obtienes el identificador del libro
        Libro.autor.label('autor'),
        Libro.disponibilidad.label('disponibilidad'),
        Libro.genero.label('genero')   
    ).all()
    
    # Renderizar la plantilla con los datos
    return render_template('consultarLibro2.html', libro=libro)
@app.route('/registrarDevolucion', methods=['GET', 'POST'])
def registrarDevolucion():
    if request.method == 'POST':
        # Obtener los datos del formulario
        IDLibro = request.form['IDLibro']
        nombreLibro = request.form['nombreLibro']
        codigoEstudiante = request.form['codigoEstudiante']
        nombreEstudiante = request.form['nombreEstudiante']
        correoEstudiante = request.form['correoEstudiante']
    

        fechaDevolucion = datetime.strptime(request.form['fechaDevolucion'], '%Y-%m-%d').date()
        estado=request.form['estado']

        # Crear una instancia del modelo Devolucion
        nueva_devolucion = Devolucion(
            IDLibro=IDLibro,
            nombreLibro=nombreLibro,
            codigoEstudiante=codigoEstudiante,
            nombreEstudiante=nombreEstudiante,
            correoEstudiante=correoEstudiante,
            fechaDevolucion=fechaDevolucion,
            estado=estado
        )

        # Agregar a la sesión y confirmar la transacción
        db.session.add(nueva_devolucion)
        db.session.commit()

        # Redirigir al usuario después de registrar la devolución
        return redirect(url_for('index'))  # Redirige a la página principal después de registrar

    return render_template('registrarDevolucion.html')  # Si el método es GET
@app.route('/consultarDevolucion', methods=['GET', 'POST'])
def consultarDevolucion():
    # Consultar los datos de la tabla Devolucion
    devoluciones = db.session.query(
        Devolucion.id.label('id'),
        Devolucion.IDLibro.label('IDLibro'),
        Devolucion.nombreLibro.label('nombreLibro'),
        Devolucion.codigoEstudiante.label('codigoEstudiante'),
        Devolucion.nombreEstudiante.label('nombreEstudiante'),
        Devolucion.correoEstudiante.label('correoEstudiante'),
        Devolucion.fechaDevolucion.label('fechaDevolucion'),
        Devolucion.estado.label('estado')
    ).all()
    
    # Renderizar la plantilla con los datos
    return render_template('consultarDevolucion.html', devoluciones=devoluciones)
@app.route('/devoluciones', methods=['GET', 'POST'])
def devoluciones():
    if request.method == 'POST':
        return redirect(url_for('index')) 
    return render_template('devoluciones.html')



from datetime import datetime

@app.route('/modificarDevolucion', methods=['GET', 'POST'])
def modificarDevolucion():
    devolucion = None

    if request.method == 'POST':
        id_devolucion = request.form.get('id_devolucion')

        if 'buscar' in request.form:
            if not id_devolucion:
                flash('Debe ingresar un ID de devolución.', 'danger')
            else:
                devolucion = Devolucion.query.get(id_devolucion)
                if not devolucion:
                    flash('ID de devolución no encontrado.', 'danger')

        elif 'modificar' in request.form:
            devolucion = Devolucion.query.get(id_devolucion)
            if devolucion:
                devolucion.IDLibro = request.form['IDLibro']
                devolucion.nombreLibro = request.form['nombreLibro']
                devolucion.codigoEstudiante = request.form['codigoEstudiante']
                devolucion.nombreEstudiante = request.form['nombreEstudiante']
                devolucion.correoEstudiante = request.form['correoEstudiante']

                # ✅ Convertir la fecha de string a date
                fecha_texto = request.form['fechaDevolucion']
                devolucion.fechaDevolucion = datetime.strptime(fecha_texto, '%Y-%m-%d').date()
                devolucion.estado=request.form['estado']

                db.session.commit()
                flash('Devolución modificada con éxito.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Error al modificar: ID no encontrado.', 'danger')

    return render_template('modificarDevolucion.html', devolucion=devolucion)


@app.route('/modificarMulta', methods=['GET', 'POST'])
def modificarMulta():
    multa = None  # Inicializamos la variable para la plantilla

    if request.method == 'POST':
        if 'buscar' in request.form:  # Buscar multa por ID
            id_multa = request.form['id_multa']
            multa = Multa.query.get(id_multa)

            if not multa:
                flash('ID de multa no encontrado.', 'danger')

        elif 'modificar' in request.form:  # Modificar multa existente
            id_multa = request.form['id_multa']
            multa = Multa.query.get_or_404(id_multa)

            multa.libro = request.form['libro']
            multa.usuario = request.form['usuario']
            multa.codigo = request.form['codigo']
            
            # Convertir fecha a objeto date antes de guardarla
            fecha_creacion_str = request.form['fecha_creacion']
            multa.fecha_creacion = datetime.strptime(fecha_creacion_str, '%Y-%m-%d').date()

            db.session.commit()
            flash('Multa modificada con éxito.', 'success')
            return redirect(url_for('index'))

    return render_template('modificarMulta.html', multa=multa)


if __name__ == '__main__':
    app.run(debug=True)
