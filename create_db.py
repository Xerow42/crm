import sqlite3

def creer_base_de_donnees():
    try:
        conn = sqlite3.connect('crm.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            email TEXT NOT NULL
        );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS motifs_email (
            id INTEGER PRIMARY KEY,
            nom_motif TEXT NOT NULL
        );''')

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reclamations';")
        table_existe = cursor.fetchone()

        if table_existe:
            cursor.execute("PRAGMA table_info(reclamations);")
            colonnes = [col[1] for col in cursor.fetchall()]

            if 'date_reclamation' not in colonnes:
                cursor.execute('ALTER TABLE reclamations ADD COLUMN date_reclamation TEXT;')
                print("✅ Colonne 'date_reclamation' ajoutée.")
        else:
            cursor.execute('''CREATE TABLE reclamations (
                id INTEGER PRIMARY KEY,
                id_utilisateur INTEGER,
                id_motif INTEGER,
                description TEXT NOT NULL,
                date_reclamation TEXT,
                langue_origine TEXT,
                description_originale TEXT,
                sentiment TEXT,
                compound_score FLOAT,
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id),
                FOREIGN KEY (id_motif) REFERENCES motifs_email(id)
            );''')
            print("Table 'reclamations' créée.")

        cursor.execute('''CREATE TABLE IF NOT EXISTS logs_email (
            id INTEGER PRIMARY KEY,
            id_utilisateur INTEGER,
            statut_email TEXT NOT NULL,
            date_envoi TEXT,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id)
        );''')

        conn.commit()
        print("Base de données et tables créées/mises à jour avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur de base de données: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    creer_base_de_donnees()
