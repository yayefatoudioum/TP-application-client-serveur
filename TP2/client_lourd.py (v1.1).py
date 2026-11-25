"""
client_lourd.py — Application de scolarité en architecture 2-TIERS (TP2).

Tier 1 : présentation + logique métier.
Tier 2 : serveur MariaDB.

Le client se connecte directement à la base de données (port 3306).
"""
import sys
import time

import pymysql

# Paramètres de connexion
SERVEUR_BDD = "192.168.56.11"
PORT_BDD = 3306
UTILISATEUR = "etudiant"
MOT_DE_PASSE = "Etudiant@2026"
BASE = "scolarite"

VERSION = "1.1"
SEUIL_VALIDATION = 10.0
NOTE_ELIMINATOIRE = 8


def connexion():
    return pymysql.connect(
        host=SERVEUR_BDD,
        port=PORT_BDD,
        user=UTILISATEUR,
        password=MOT_DE_PASSE,
        database=BASE,
        charset="utf8mb4",
        connect_timeout=5
    )


def moyenne(notes):
    """Calcule la moyenne pondérée par les crédits."""
    total_credits = sum(c for _, c in notes)
    return (
        sum(float(v) * c for v, c in notes) / total_credits
        if total_credits else 0.0
    )


def octets_recus(cur):
    """Retourne les octets envoyés par le serveur sur cette connexion."""
    cur.execute("SHOW SESSION STATUS LIKE 'Bytes_sent'")
    return int(cur.fetchone()[1])


def lister_etudiants(cur):
    cur.execute(
        "SELECT matricule, prenom, nom, filiere "
        "FROM etudiant ORDER BY nom, prenom"
    )
    for mat, pre, nom, fil in cur.fetchall():
        print(f"  {mat}  {nom:<8} {pre:<10} {fil}")


def releve(cur, matricule):
    cur.execute(
        "SELECT prenom, nom FROM etudiant WHERE matricule = %s",
        (matricule,)
    )
    ligne = cur.fetchone()

    if not ligne:
        print("  matricule inconnu")
        return

    print(f"  Relevé de {ligne[0]} {ligne[1]} ({matricule})")

    cur.execute(
        """SELECT e.code, e.intitule, e.credits, n.valeur
           FROM note n JOIN ec e ON e.code = n.ec
           WHERE n.matricule = %s ORDER BY e.code""",
        (matricule,)
    )

    notes = []
    valeurs = []

    for code, intitule, credits, valeur in cur.fetchall():
        print(
            f"    {code:<5} {intitule:<36} "
            f"{credits} cr.  {valeur:>5}"
        )
        notes.append((valeur, credits))
        valeurs.append(float(valeur))

    m = moyenne(notes)
    elimine = any(v < NOTE_ELIMINATOIRE for v in valeurs)

    decision = (
        "VALIDÉ"
        if m >= SEUIL_VALIDATION and not elimine
        else "NON VALIDÉ"
    )

    print(f"  Moyenne pondérée : {m:.2f} / 20  ->  {decision}")


def classement(cur):
    """Le client rapatrie toutes les notes et calcule le classement."""
    octets_avant = octets_recus(cur)
    debut = time.perf_counter()

    cur.execute(
        """SELECT n.matricule, n.valeur, e.credits
           FROM note n JOIN ec e ON e.code = n.ec"""
    )

    lignes = cur.fetchall()
    duree = time.perf_counter() - debut
    volume = octets_recus(cur) - octets_avant

    par_etudiant = {}

    for mat, valeur, credits in lignes:
        par_etudiant.setdefault(mat, []).append((valeur, credits))

    rang = sorted(
        (
            (moyenne(notes), mat)
            for mat, notes in par_etudiant.items()
        ),
        reverse=True
    )

    print(
        f"  {len(lignes)} lignes rapatriées du serveur en "
        f"{duree * 1000:.0f} ms ({volume / 1024:.1f} Kio)"
    )

    for i, (m, mat) in enumerate(rang[:10], 1):
        print(f"  {i:>2}. {mat}  {m:.2f}")

    admis = sum(
        1 for m, mat in rang
        if m >= SEUIL_VALIDATION
        and all(
            float(valeur) >= NOTE_ELIMINATOIRE
            for valeur, credits in par_etudiant[mat]
        )
    )

    print(f"  Admis : {admis} / {len(rang)}")


def main():
    print(
        f"Scolarité — client lourd v{VERSION} — "
        f"serveur {SERVEUR_BDD}:{PORT_BDD}"
    )

    try:
        cnx = connexion()
    except pymysql.MySQLError as e:
        sys.exit(
            f"Connexion impossible au serveur de base de données : {e}"
        )

    with cnx, cnx.cursor() as cur:
        while True:
            print(
                "\n1. Liste des étudiants   "
                "2. Relevé de notes   "
                "3. Classement   0. Quitter"
            )

            choix = input("> ").strip()

            if choix == "1":
                lister_etudiants(cur)
            elif choix == "2":
                releve(cur, input("  Matricule : ").strip())
            elif choix == "3":
                classement(cur)
            elif choix == "0":
                break


if __name__ == "__main__":
    main()