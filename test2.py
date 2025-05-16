import faulthandler
import mysql.connector
import os

# === Activare faulthandler pentru debugging ===
faulthandler.enable()

# === Funcție pentru conectarea la baza de date ===
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="banca"
    )

# === Afișează mesajul de întâmpinare ===
def mesaj_bine_ai_venit():
    print("="*50)
    print("BINE AI VENIT LA BANCA VIRTUALĂ!")
    print("Apasă Enter pentru a continua spre logare...")
    print("="*50)
    input()  # Așteaptă apăsarea unei taste
    os.system('cls' if os.name == 'nt' else 'clear')  # Curăță ecranul

# === Funcție de logare ===
def logare():
    while True:
        parola = input("Introduceți parola: ")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT nume, rol FROM conturi WHERE parola = %s", (parola,))
        result = cursor.fetchone()
        conn.close()
        if result:
            print(f"Bine ai revenit, {result[0]}! Rol: {result[1]}")
            return result[0], result[1]  # returnează nume și rol
        else:
            print("Parolă incorectă. Încearcă din nou.")

# === Funcție pentru verificarea soldului ===
def verificare_sold(utilizator):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sold FROM conturi WHERE nume = %s", (utilizator,))
    sold = cursor.fetchone()[0]
    conn.close()
    print(f"Soldul contului tău este: {sold} RON")

# === Funcție pentru retragere bani ===
def retragere_bani(utilizator):
    suma = float(input("Introduceți suma de retras: "))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sold FROM conturi WHERE nume = %s", (utilizator,))
    sold = cursor.fetchone()[0]
    if suma <= sold:
        cursor.execute("UPDATE conturi SET sold = sold - %s WHERE nume = %s", (suma, utilizator))
        conn.commit()
        print("Retragere efectuată cu succes.")
    else:
        print("Fonduri insuficiente.")
    conn.close()

# === Funcție pentru depunere bani ===
def depunere_bani(utilizator):
    suma = float(input("Introduceți suma de depus: "))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE conturi SET sold = sold + %s WHERE nume = %s", (suma, utilizator))
    conn.commit()
    conn.close()
    print("Depunere efectuată cu succes.")

# === Funcție pentru transfer bani ===
def transfer_bani(utilizator):
    destinatar = input("Introduceți numele destinatarului: ")
    suma = float(input("Introduceți suma de transferat: "))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sold FROM conturi WHERE nume = %s", (utilizator,))
    sold = cursor.fetchone()[0]
    cursor.execute("SELECT nume FROM conturi WHERE nume = %s", (destinatar,))
    if cursor.fetchone() and suma <= sold:
        cursor.execute("UPDATE conturi SET sold = sold - %s WHERE nume = %s", (suma, utilizator))
        cursor.execute("UPDATE conturi SET sold = sold + %s WHERE nume = %s", (suma, destinatar))
        conn.commit()
        print("Transfer realizat cu succes.")
    else:
        print("Transfer eșuat. Cont inexistent sau fonduri insuficiente.")
    conn.close()

# === Funcții exclusive pentru Admin ===
def creare_cont():
    nume = input("Nume utilizator: ")
    parola = input("Parolă: ")
    tip = input("Tip cont (curent/depozit): ")
    rol = input("Rol (client/admin): ")
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO conturi (nume, parola, tip, rol) VALUES (%s, %s, %s, %s)", (nume, parola, tip, rol))
        conn.commit()
        print("Cont creat cu succes.")
    except mysql.connector.IntegrityError:
        print("Contul există deja.")
    conn.close()

def stergere_cont():
    nume = input("Introduceți numele contului de șters: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conturi WHERE nume = %s", (nume,))
    conn.commit()
    conn.close()
    print("Cont șters cu succes.")

def listare_conturi():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nume, tip, sold, rol FROM conturi")
    conturi = cursor.fetchall()
    conn.close()
    for c in conturi:
        print(f"Utilizator: {c[0]}, Tip: {c[1]}, Sold: {c[2]} RON, Rol: {c[3]}")

# === Meniul principal în funcție de rol ===
def meniu_principal(utilizator, rol):
    while True:
        print("\n=== MENIU ===")
        print("1. Verificare sold")
        print("2. Retragere bani")
        print("3. Depunere bani")
        print("4. Transfer bani")
        if rol == 'admin':
            print("5. Creare cont")
            print("6. Ștergere cont")
            print("7. Listare conturi")
        print("0. Deconectare")

        opt = input("Alege opțiunea: ")
        if opt == '1':
            verificare_sold(utilizator)
        elif opt == '2':
            retragere_bani(utilizator)
        elif opt == '3':
            depunere_bani(utilizator)
        elif opt == '4':
            transfer_bani(utilizator)
        elif opt == '5' and rol == 'admin':
            creare_cont()
        elif opt == '6' and rol == 'admin':
            stergere_cont()
        elif opt == '7' and rol == 'admin':
            listare_conturi()
        elif opt == '0':
            print("Deconectare cu succes.")
            break
        else:
            print("Opțiune invalidă.")

# === Punctul de intrare în aplicație ===
if __name__ == "__main__":
    mesaj_bine_ai_venit()
    utilizator, rol = logare()
    meniu_principal(utilizator, rol)
