import sqlite3
import csv
from logging import getLogger

logger = getLogger(__name__)

# This function is not tested thorougly!

def update_db(db_file, csv_file):
    logger.info("Updating the database...")
    conn = sqlite3.connect(db_file)
    crsr = conn.cursor()

    try:
        with open(csv_file, 'r') as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                id = row[0]
                seq = row[1]

                update_query = """
                    UPDATE seq
                    SET seq = ?
                    WHERE id = ?
                """
                crsr.execute(update_query, (seq, id))

                # Commit changes to the database
                conn.commit()

        logger.info("Database updated successfully.")
    except Exception as e:
        logger.error(f"Error updating database: {e}")
    finally:
        conn.close()


