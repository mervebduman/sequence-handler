import sqlite3

conn = sqlite3.connect('seq_handler.db')
crsr = conn.cursor()
 
# create table
sql_command = """CREATE TABLE seq ( 
id TEXT, 
seq TEXT
);"""
 
crsr.execute(sql_command)

conn.close()