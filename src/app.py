from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    # Mostrar directamente el formulario de validación de RUT en la raíz
    return render_template('rut.html')


def validate_rut(rut_raw: str) -> bool:
    """Valida un RUT chileno. Acepta formatos con o sin puntos y con o sin guión."""
    if not rut_raw:
        return False
    rut = rut_raw.replace('.', '').replace(' ', '').upper()
    if '-' in rut:
        parts = rut.split('-')
        if len(parts) != 2:
            return False
        body, dv = parts
    else:
        body, dv = rut[:-1], rut[-1]
    if not body.isdigit():
        return False
    reversed_digits = map(int, reversed(body))
    factors = [2, 3, 4, 5, 6, 7]
    s = 0
    factor_index = 0
    for d in reversed_digits:
        s += d * factors[factor_index]
        factor_index = (factor_index + 1) % len(factors)
    mod = 11 - (s % 11)
    if mod == 11:
        computed = '0'
    elif mod == 10:
        computed = 'K'
    else:
        computed = str(mod)
    return computed == dv


@app.route('/saludo')
def saludo():
    nombre = request.args.get('nombre')
    return render_template('saludo.html', nombre=nombre)


@app.route('/rut')
def rut_form():
    return render_template('rut.html')


@app.route('/validar_rut', methods=['POST'])
def validar_rut():
    # Acepta tanto formulario tradicional como JSON
    rut = request.form.get('rut') or (request.get_json(silent=True) or {}).get('rut')
    ok = validate_rut(rut)
    return jsonify({'rut': rut, 'valid': ok})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
