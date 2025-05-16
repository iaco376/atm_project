from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="banca"
    )

@app.route('/')
def home():
    print("Folderul curent este:", os.getcwd())
    print("Există index.html?:", os.path.exists('templates/index.html'))
    return render_template('index.html')

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Server ok"}), 200

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "Date JSON lipsă"}), 400

        username = data.get('username', '').lower()
        parola = data.get('password', '')

        if not username or not parola:
            return jsonify({"success": False, "message": "Username și parola sunt necesare"}), 400

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM conturi WHERE nume = %s AND parola = %s", (username, parola))
        user = cursor.fetchone()

        if user:
            return jsonify({"success": True, "rol": user["rol"]})
        else:
            return jsonify({"success": False, "message": "Date incorecte"}), 401

    except mysql.connector.Error as err:
        print("Eroare DB:", err)
        return jsonify({"success": False, "message": "Eroare server"}), 500

    except Exception as e:
        import traceback
        print("EROARE NEAȘTEPTATĂ:", e)
        traceback.print_exc()
        return jsonify({"success": False, "message": "Eroare server"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# ===================== CLIENT =====================

@app.route('/client/verificare_sold', methods=['POST'])
def verificare_sold():
    data = request.json
    utilizator = data.get('utilizator')
    if not utilizator:
        return jsonify({"message": "Utilizatorul este necesar"}), 400
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sold FROM conturi WHERE nume = %s", (utilizator,))
    sold = cursor.fetchone()
    cursor.close()
    conn.close()
    if sold is not None:
        return jsonify({"sold": sold[0]})
    else:
        return jsonify({"message": "Utilizator inexistent"}), 404

@app.route('/client/retragere_bani', methods=['POST'])
def retragere_bani():
    data = request.json
    utilizator = data.get('utilizator')
    suma = data.get('suma')
    if not utilizator or suma is None:
        return jsonify({"message": "Utilizator și suma sunt necesare"}), 400
    try:
        suma = float(suma)
    except:
        return jsonify({"message": "Suma trebuie să fie un număr"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sold FROM conturi WHERE nume = %s", (utilizator,))
    sold = cursor.fetchone()
    if not sold:
        cursor.close()
        conn.close()
        return jsonify({"message": "Utilizator inexistent"}), 404
    if suma <= sold[0]:
        cursor.execute("UPDATE conturi SET sold = sold - %s WHERE nume = %s", (suma, utilizator))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Retragere efectuată cu succes."})
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Fonduri insuficiente."}), 400

@app.route('/client/depunere_bani', methods=['POST'])
def depunere_bani():
    data = request.json
    utilizator = data.get('utilizator')
    suma = data.get('suma')
    if not utilizator or suma is None:
        return jsonify({"message": "Utilizator și suma sunt necesare"}), 400
    try:
        suma = float(suma)
    except:
        return jsonify({"message": "Suma trebuie să fie un număr"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE conturi SET sold = sold + %s WHERE nume = %s", (suma, utilizator))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Depunere efectuată cu succes."})

@app.route('/client/transfer_bani', methods=['POST'])
def transfer_bani():
    data = request.json
    utilizator = data.get('utilizator')
    destinatar = data.get('destinatar')
    suma = data.get('suma')
    if not utilizator or not destinatar or suma is None:
        return jsonify({"message": "Utilizator, destinatar și suma sunt necesare"}), 400
    try:
        suma = float(suma)
    except:
        return jsonify({"message": "Suma trebuie să fie un număr"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sold FROM conturi WHERE nume = %s", (utilizator,))
    sold = cursor.fetchone()
    cursor.execute("SELECT nume FROM conturi WHERE nume = %s", (destinatar,))
    destinatar_exista = cursor.fetchone()
    if sold and destinatar_exista and suma <= sold[0]:
        cursor.execute("UPDATE conturi SET sold = sold - %s WHERE nume = %s", (suma, utilizator))
        cursor.execute("UPDATE conturi SET sold = sold + %s WHERE nume = %s", (suma, destinatar))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Transfer realizat cu succes."})
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Transfer eșuat. Cont inexistent sau fonduri insuficiente."}), 400

# ===================== ADMIN =====================

@app.route('/admin/creare_cont', methods=['POST'])
def creare_cont():
    data = request.json
    nume = data.get('nume')
    parola = data.get('parola')
    tip = data.get('tip')
    rol = data.get('rol')
    sold_initial = data.get('sold_initial', 0)
    if not all([nume, parola, tip, rol]):
        return jsonify({"message": "Toate câmpurile sunt obligatorii"}), 400
    try:
        sold_initial = float(sold_initial)
    except:
        return jsonify({"message": "Soldul inițial trebuie să fie un număr valid"}), 400
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conturi (nume, parola, tip, rol, sold) VALUES (%s, %s, %s, %s, %s)",
                   (nume, parola, tip, rol, sold_initial))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Cont creat cu succes"})

@app.route('/admin/inchidere_cont', methods=['POST'])
def inchidere_cont():
    data = request.json
    nume = data.get('nume')
    if not nume:
        return jsonify({"message": "Numele contului este necesar"}), 400
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conturi WHERE nume = %s", (nume,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Contul {nume} a fost șters cu succes"})

@app.route('/admin/listare_conturi')
def listare_conturi():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nume, tip, rol, sold FROM conturi")
    conturi = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"conturi": conturi})

@app.route('/admin/conturi_curente')
def conturi_curente():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nume, sold FROM conturi WHERE tip = 'curent'")
    conturi = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"conturi_curente": conturi})

@app.route('/admin/depozite_bancare')
def depozite_bancare():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nume, sold FROM conturi WHERE tip = 'depozit'")
    depozite = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"depozite_bancare": depozite})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
