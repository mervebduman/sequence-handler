import sqlite3
import yaml
import os

from Bio import SeqIO

conn = sqlite3.connect('seq_handler.db')
crsr = conn.cursor()

# get fixed seqs
def get_fixed_sequences():
    with open("config/fixed_sequences.yaml", 'r') as f:
        file = yaml.safe_load(f)
        seq1 = file.get('seq1')
        seq2 = file.get('seq2')
    return seq1, seq2

seq1, seq2 = get_fixed_sequences()

# parse db files
# note: for the sake of simplicity, I added temporary lines. Normally, they should be removed.
def parse_fastq_files():
    fastqs = [f for f in os.listdir("db") if f.endswith(".fq")]
    for f in fastqs:
        file_path = os.path.join("db", f)
        count = 0 #temporary
        with open(file_path, "r") as handle:
            for record in SeqIO.parse(handle, "fastq"):
                if count >= 10000: #temporary
                    break #temporary
                yield record.id, (seq1+str(record.seq)+seq2)
                count += 1 #temporary

insert_query = """
    INSERT INTO seq (id, seq)
    VALUES (?, ?)
"""

crsr.executemany(insert_query, parse_fastq_files())

conn.commit()

conn.close()