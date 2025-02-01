import requests
import psycopg2
import pandas as pd
from fastapi import FastAPI
import os
import logging

app = FastAPI()
# Configuration de logging pour écrire dans un fichier
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration de la connexion PostgreSQL
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")


@app.get("/file")
async def import_csv():
    logging.info("Début de l'importation du fichier CSV")
    
    url = "https://raw.githubusercontent.com/france-connect/data-provider-example/refs/heads/master/database.csv"
    file_path = "data/database.csv"
    if not os.path.exists('data'):
        os.makedirs('data')
        logging.info("Création du répertoire 'data'")

    # Télécharger le fichier
    response = requests.get(url)
    if response.status_code == 200:
        try:
            # Enregistrer le fichier localement
            with open(file_path, 'wb') as f:
                f.write(response.content)
            logging.info("Fichier téléchargé et enregistré sous %s", file_path)

            try:
                create_schema_and_insert_data('demo', file_path)
                logging.info("Données insérées avec succès dans la table %s", 'demo')
                return {"message": "Données insérées avec succès dans la table."}  # Message de succès
            except psycopg2.Error as db_error:
                logging.error("Erreur de connexion à la base de données : %s", db_error)
                return {"error": f"Erreur de connexion à la base de données : {db_error}"}

        except Exception as e:
            logging.error("Erreur lors de la lecture du fichier : %s", str(e))
            return {"file": str(e)}
    else:
        logging.error("Problème lors du téléchargement du fichier, statut : %s", response.status_code)
        return {"file": "Il y a un problème", "status": response.status_code}

def connect_to_db():
    logging.info("Connexion à la base de données")
    return psycopg2.connect(database=DB_NAME,
                             user=DB_USER,
                             password=DB_PASS,
                             host=DB_HOST,
                             port=DB_PORT)

def disconnect_from_db(conn, cursor):
    if cursor:  # Si le curseur existe
        cursor.close()
    if conn:  # Si la connexion existe
        conn.close()
    logging.info("Déconnexion de la base de données")


def create_schema_and_insert_data(table_name, file_url):
    logging.info("Création du schéma et insertion des données dans la table %s", table_name)

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        logging.info("Connexion à la base de données réussie")

        df = pd.read_csv(file_url)
        logging.info("Fichier CSV lu avec succès")

        # Générer le schéma de la table à partir des colonnes du DataFrame
        try:
            columns = df.columns
            column_definitions = ", ".join([f"{col} VARCHAR" for col in columns])  # Vous pouvez ajuster le type de données selon vos besoins
        except Exception as e:
            logging.error("Erreur lors de la récupération des colonnes du DataFrame : %s", str(e))
            return {"file": str(e)}
        
        # Création de la table
        try:
            logging.info("Création de la table %s", table_name)
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {column_definitions}
            );
            """)
            logging.info("Table %s créée ou déjà existante", table_name)
        except Exception as e:
            logging.error("Erreur lors de la création de la table : %s", str(e))
            return {"table": str(e)}

        # Insérer les données dans la table
        try:
            for index, row in df.iterrows():
                cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))});", tuple(row))
            conn.commit()
            logging.info("Données insérées dans la table %s", table_name)
        except Exception as e:
            logging.error("Erreur lors de l'insertion des données : %s", str(e))
            return {"data": str(e)}
        
    except Exception as e:
        logging.error("Erreur lors de la création du schéma ou de l'insertion des données : %s", str(e))
    finally:
        # Déconnexion de la base de données
        disconnect_from_db(conn, cursor)