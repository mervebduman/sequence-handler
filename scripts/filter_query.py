import sqlite3
import os
import gzip
import csv
import glob

from functools import partial

from Bio import SeqIO

def parse_fastq_file(query_folder):
    query_files = glob.glob(os.path.join(query_folder, '*.fastq*'))

    for f in query_files:
        # if zipped, unzip; else, just open
        _open = partial(gzip.open, mode='rt') if f.endswith(".gz") else open

        with _open(f) as handle:
            for record in SeqIO.parse(handle, "fastq"):
                yield str(record.seq)

def filter_query(query_folder):
    conn = sqlite3.connect('seq_handler.db')
    crsr = conn.cursor()

    unique_seqs = []

    # note: for the sake of simplicity, I added temporary lines. Normally, they should be removed.
    count = 0 #temporary
    for seq in parse_fastq_file(query_folder):
        if count >= 10000: #temporary
            break
        if crsr.execute("SELECT * FROM seq WHERE seq NOT LIKE ?", (seq,)):
            unique_seqs.append(seq)
            count += 1 #temporary

    crsr.close()
    conn.close()

    with open("out/unique_seqs.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        for seq in unique_seqs:
            writer.writerow([seq])


filter_query("query")
