import sqlite3
import yaml
import os

from Bio import SeqIO
from logging import getLogger

logger = getLogger(__name__)

# get fixed seqs from config
def get_fixed_sequences():
    if os.path.isfile("config/fixed_sequences.yaml"):
            logger.info("Getting the fixed sequences from the config file...")

    with open("config/fixed_sequences.yaml", 'r') as f:
        file = yaml.safe_load(f)
        seq1 = file.get('seq1')

        if seq1:
            logger.info(f"Seq1 found!: {seq1}")
        else:
            logger.error("Please provide fixed sequences in the config file.")

        seq2 = file.get('seq2')

        if seq2:
            logger.info(f"Seq2 found!: {seq2}")
        else:
            logger.error("Please provide fixed sequences in the config file.")

    return seq1, seq2

# parse db files
def parse_fastq_files():
    seq1, seq2 = get_fixed_sequences()

    logger.info("Finding the database files...")
    fastqs = [f for f in os.listdir("db") if f.endswith(".fq")]
    for f in fastqs:
        file_path = os.path.join("db", f)

        logger.info(f"File found!: {file_path}")

        with open(file_path, "r") as handle:
            logger.info("Flanking and saving the sequences...")
            for record in SeqIO.parse(handle, "fastq"):
                yield record.id, (seq1+str(record.seq)+seq2)


def populate_db():
    conn = sqlite3.connect('seq_handler.db')
    crsr = conn.cursor()

    insert_query = """
    INSERT INTO seq (id, seq)
    VALUES (?, ?)
    """

    crsr.executemany(insert_query, parse_fastq_files())

    conn.commit()

    conn.close()

    logger.info("Done! Please check the db file.")


