from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista en memoria para almacenar inscritos
inscritos = []

# Ruta para mostrar el formulario de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Captura de datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')

        # Crear un registro de inscrito
        inscrito = {
            'id': len(inscritos) + 1,
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminarios': "; ".join(seminarios)
        }

        # Agregar inscrito a la lista en memoria
        inscritos.append(inscrito)

        return redirect(url_for('index'))

    return render_template('registro_seminario.html')

# Ruta para mostrar el listado de inscritos
@app.route('/')
def index():
    return render_template('index.html', inscritos=inscritos)

# Ruta para eliminar un inscrito
@app.route('/eliminar/<int:id>')
def eliminar(id):
    global inscritos
    inscritos = [i for i in inscritos if i['id'] != id]
    return redirect(url_for('index'))

# Ruta para editar un inscrito
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    inscrito = next((i for i in inscritos if i['id'] == id), None)
    if request.method == 'POST' and inscrito:
        inscrito['fecha'] = request.form['fecha']
        inscrito['nombre'] = request.form['nombre']
        inscrito['apellidos'] = request.form['apellidos']
        inscrito['turno'] = request.form['turno']
        inscrito['seminarios'] = "; ".join(request.form.getlist('seminarios'))
        return redirect(url_for('index'))
    
    return render_template('registro_seminario.html', inscrito=inscrito)

if __name__ == '__main__':
    app.run(debug=True)