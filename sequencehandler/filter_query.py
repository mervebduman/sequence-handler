import sqlite3
import os
import gzip
import csv
import glob

from functools import partial
from Levenshtein import distance
from Bio import SeqIO
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)

def parse_fastq_file(query_folder):
    query_files = glob.glob(os.path.join(query_folder, '*.fastq*'))

    for f in query_files:
        logger.info(f"Query found: {f}")
        logger.info("Parsing the query...")

        # if zipped, unzip; else, just open
        _open = partial(gzip.open, mode='rt') if f.endswith(".gz") else open

        with _open(f) as handle:
            count = 0
            for record in SeqIO.parse(handle, "fastq"):
                yield record.id, str(record.seq)
                count += 1
        logger.info(f"Total seq count: {count}")

def filter_query(query_folder, threshold):
    conn = sqlite3.connect('seq_handler.db')
    crsr = conn.cursor()

    sys_datetime = datetime.now().strftime("%Y%m%d_%H%M")

    with open(f"out/unique_seqs_{sys_datetime}.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        count = 0
        for seq_id, seq in parse_fastq_file(query_folder):
            similar = False
            crsr.execute("SELECT seq FROM seq;")
            for (db_seq,) in crsr.fetchall():
                if distance(seq, db_seq) <= threshold:
                    similar = True
                    # add here to output a csv file listing sequences found in the database,
                    # including their frequencies within the same FASTQ file (intra-frequency) 
                    # and across different FASTQ files (inter-frequency).
                    break

            if not similar:
                writer.writerow([seq_id, seq])
                count += 1
        logger.info(f"Total unique seq count: {count}")

    crsr.close()
    conn.close()
