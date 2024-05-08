import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Command-line tool for creating & populating a db and filtering input against it.",
    )

    parser.add_argument(
        "-c",
        "--createDB",
        help="Create a SQL DB and a table",
        action='store_true'
    )
    parser.add_argument(
        "-p",
        "--populateDB",
        help="Populate the DB with data",
        action='store_true'
    )
    parser.add_argument(
        "-o",
        "--outputDB",
        help="Output DB as csv.",
        action='store_true'
    )
    parser.add_argument(
        "-f",
        "--filterQuery",
        help="Filter the query against DB and output unique sequences",
        action='store_true'
    )
    parser.add_argument(
        "-t",
        "--threshold",
        help="Levenshtein edit distance threshold (default = 51)",
        type=int,
        default= 51
    )
    parser.add_argument(
        "-u",
        "--updateDB",
        help="Update DB with unique sequences that are found after filtering.",
        type=str
    )

    return parser.parse_args()
