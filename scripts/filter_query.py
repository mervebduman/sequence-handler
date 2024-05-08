import sqlite3
import os
import gzip
import csv
import glob

from functools import partial
from Levenshtein import distance
from Bio import SeqIO

def parse_fastq_file(query_folder):
    query_files = glob.glob(os.path.join(query_folder, '*.fastq*'))

    for f in query_files:
        # if zipped, unzip; else, just open
        _open = partial(gzip.open, mode='rt') if f.endswith(".gz") else open

        with _open(f) as handle:
            for record in SeqIO.parse(handle, "fastq"):
                yield str(record.seq)

# note: for the sake of simplicity, I added temporary lines. Normally, they should be removed.
def filter_query(query_folder, threshold):
    conn = sqlite3.connect('seq_handler.db')
    crsr = conn.cursor()

    count = 0 #temporary
    with open("out/unique_seqs.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        for seq in parse_fastq_file(query_folder):
            if count >= 150: #temporary
                break #temporary

            # Check similarity with existing sequences in the database
            similar = False
            crsr.execute("SELECT seq FROM seq")
            for (db_seq,) in crsr.fetchall():
                if distance(seq, db_seq) <= threshold:
                    similar = True
                    break

            if not similar:
                writer.writerow([seq])
                count += 1 #temporary

    crsr.close()
    conn.close()

edit_distance_threshold = 3
filter_query("query", edit_distance_threshold)