import sqlite3
import csv
import os
from logging import getLogger

logger = getLogger(__name__)

def output_db():
    conn = sqlite3.connect('seq_handler.db')
    crsr = conn.cursor()

    try:
        crsr.execute("SELECT * FROM seq")
        rows = crsr.fetchall()

        logger.info("Creating the csv output of the database...")

        with open("db.csv", 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([description[0] for description in crsr.description]) 
            writer.writerows(rows) 

        if os.path.isfile("db.csv"):
            logger.info(f"Output created.")

    except sqlite3.Error as e:
        logger.error(f"Error exporting database to CSV: {e}")

    finally:
        crsr.close()
        conn.close()
