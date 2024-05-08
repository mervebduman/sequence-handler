import sqlite3
import os
from logging import getLogger

logger = getLogger(__name__)

def create_db():
    if os.path.isfile("seq_handler.db"):
        logger.error("Database already exists!")
    else:
        logger.info("Creating the database...")
        conn = sqlite3.connect('seq_handler.db')
        crsr = conn.cursor()
        
        # create table
        sql_command = """CREATE TABLE seq ( 
        id TEXT, 
        seq TEXT
        );"""
        
        crsr.execute(sql_command)

        conn.close()

        if os.path.isfile("seq_handler.db"):
            logger.info("File created. Please populate.")
