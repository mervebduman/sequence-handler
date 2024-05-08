import os

from sequencehandler.cli import parse_args
from sequencehandler.create_db import create_db
from sequencehandler.populate_db import populate_db
from sequencehandler.output_db import output_db
from sequencehandler.filter_query import filter_query
from sequencehandler.update_db import update_db
from sequencehandler.config import setup_logger


def main():
    logger = setup_logger()

    args = parse_args()

    if args.createDB:
        create_db()

    if args.populateDB:
        populate_db()

    if args.outputDB:
        output_db()

    if args.filterQuery:
        logger.info(f"Threshold set: {args.threshold}")
        filter_query("query", args.threshold)

    if args.updateDB:
        if os.path.isfile(args.updateDB):
            logger.info(f"File is selected to update the DB: {args.updateDB}")
            update_db("seq_handler.db", args.updateDB)
        else:
            logger.info(f"File not found!: {args.updateDB}")


if __name__ == "__main__":
    main()