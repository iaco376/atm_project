import faulthandler
import mysql.connector

# Crearea conexiunii la baza de date MySQL
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",           # Înlocuiește cu utilizatorul tău MySQL
        password="1234",        # Înlocuiește cu parola ta MySQL
        database="banca"        # Numele bazei de date
    )
    return conn

# Identificarea utilizatorului pe baza parolei
def identificare_utilizator():
    parola = input("Introduceți parola: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nume FROM conturi WHERE parola = %s", (parola,))
    result = cursor.fetchone()
    conn.close()
    if result:
        print(f"Utilizator identificat: {result[0]}")
        return result[0]
    else:
        print("Parolă incorectă.")
        return None

# Crearea unui nou cont
def creare_cont():
    nume = input("Introduceți numele utilizatorului: ")
    parola = input("Setați o parolă: ")
    tip = input("Tip cont (curent/depozit): ").lower()
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO conturi (nume, parola, tip) VALUES (%s, %s, %s)", (nume, parola, tip))
        conn.commit()
        print("Cont creat cu succes.")
    except mysql.connector.IntegrityError:
        print("Contul există deja.")
    conn.close()

# Ștergerea unui cont existent
def stergere_cont():
    utilizator = identificare_utilizator()
    if utilizator:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conturi WHERE nume = %s", (utilizator,))
        conn.commit()
        conn.close()
        print("Cont șters cu succes.")

# Listarea conturilor din bancă
def listare_conturi():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nume, tip, sold FROM conturi")
    conturi = cursor.fetchall()
    conn.close()
    if conturi:
        for c in conturi:
            print(f"Utilizator: {c[0]}, Tip: {c[1]}, Sold: {c[2]} RON")
    else:
        print("Nu există conturi.")

# Retragerea de bani dintr-un cont
def retragere_bani():
    utilizator = identificare_utilizator()
    if utilizator:
        try:
            suma = float(input("Introduceți suma de retras: "))
        except ValueError:
            print("Sumă invalidă.")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT sold FROM conturi WHERE nume = %s", (utilizator,))
        sold = cursor.fetchone()[0]
        if suma <= sold:
            cursor.execute("UPDATE conturi SET sold = sold - %s WHERE nume = %s", (suma, utilizator))
            conn.commit()
            print("Retragere efectuată.")
        else:
            print("Fonduri insuficiente.")
        conn.close()

# Depunerea de bani într-un cont
def depunere_bani():
    utilizator = identificare_utilizator()
    if utilizator:
        try:
            suma = float(input("Introduceți suma de depus: "))
        except ValueError:
            print("Sumă invalidă.")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE conturi SET sold = sold + %s WHERE nume = %s", (suma, utilizator))
        conn.commit()
        conn.close()
        print("Depunere efectuată.")

# Transferul de bani între conturi
def transfer_bani():
    utilizator = identificare_utilizator()
    if utilizator:
        destinatar = input("Introduceți numele destinatarului: ")
        try:
            suma = float(input("Suma de transferat: "))
        except ValueError:
            print("Sumă invalidă.")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT sold FROM conturi WHERE nume = %s", (utilizator,))
        sold_sursa = cursor.fetchone()[0]

        cursor.execute("SELECT nume FROM conturi WHERE nume = %s", (destinatar,))
        if cursor.fetchone() and suma <= sold_sursa:
            cursor.execute("UPDATE conturi SET sold = sold - %s WHERE nume = %s", (suma, utilizator))
            cursor.execute("UPDATE conturi SET sold = sold + %s WHERE nume = %s", (suma, destinatar))
            conn.commit()
            print("Transfer realizat cu succes.")
        else:
            print("Transfer eșuat. Cont inexistent sau fonduri insuficiente.")
        conn.close()

# Listarea conturilor curente
def conturi_curente():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nume, sold FROM conturi WHERE tip = 'curent'")
    conturi = cursor.fetchall()
    conn.close()
    for c in conturi:
        print(f"{c[0]}: {c[1]} RON")

# Listarea depozitelor conturire
def depozite_conturire():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nume, sold FROM conturi WHERE tip = 'depozit'")
    conturi = cursor.fetchall()
    conn.close()
    for c in conturi:
        print(f"{c[0]}: {c[1]} RON")

# Funcție nouă: afișează soldul curent al utilizatorului
def afiseaza_sold():
    utilizator = identificare_utilizator()
    if utilizator:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT sold FROM conturi WHERE nume = %s", (utilizator,))
        sold = cursor.fetchone()[0]
        print(f"Soldul contului {utilizator} este: {sold} RON")
        conn.close()

# Meniul pentru admin (fără identificare utilizator și proprietar cont)
def meniu_admin():
    while True:
        print("\n=== MENIU ADMIN ===")
        print("1. Creare cont nou")
        print("2. Ștergere cont")
        print("3. Listare conturi")
        print("4. Retragere bani")
        print("5. Depunere bani")
        print("6. Transfer bani")
        print("7. Conturi curente")
        print("8. Depozite conturire")
        print("0. Ieșire")
        optiune = input("Alege o opțiune: ")

        if optiune == '1':
            creare_cont()
        elif optiune == '2':
            stergere_cont()
        elif optiune == '3':
            listare_conturi()
        elif optiune == '4':
            retragere_bani()
        elif optiune == '5':
            depunere_bani()
        elif optiune == '6':
            transfer_bani()
        elif optiune == '7':
            conturi_curente()
        elif optiune == '8':
            depozite_conturire()
        elif optiune == '0':
            print("Ieșire din meniul admin.")
            break
        else:
            print("Opțiune invalidă.")

# Meniul pentru client (fără istoric tranzacții, afișează sold în loc de vezi informații)
def meniu_client():
    while True:
        print("\n=== MENIU CLIENT ===")
        print("1. Retragere bani")
        print("2. Depunere bani")
        print("3. Transfer bani")
        print("4. Afișează sold")
        print("0. Ieșire")
        optiune = input("Alege o opțiune: ")

        if optiune == '1':
            retragere_bani()
        elif optiune == '2':
            depunere_bani()
        elif optiune == '3':
            transfer_bani()
        elif optiune == '4':
            afiseaza_sold()
        elif optiune == '0':
            print("Ieșire din meniul client.")
            break
        else:
            print("Opțiune invalidă.")

# Funcție principală de selecție a meniului (admin sau client)
def main():
    faulthandler.enable()
    while True:
        print("\n=== BUN VENIT ===")
        print("1. Meniu Admin")
        print("2. Meniu Client")
        print("0. Ieșire")
        optiune = input("Selectează tipul utilizatorului: ")
        if optiune == '1':
            meniu_admin()
        elif optiune == '2':
            meniu_client()
        elif optiune == '0':
            print("La revedere!")
            break
        else:
            print("Opțiune invalidă.")

if __name__ == "__main__":
    main()
