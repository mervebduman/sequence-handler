from sequencehandler.cli import parse_args
from sequencehandler.create_db import create_db
from sequencehandler.populate_db import populate_db
from sequencehandler.output_db import output_db
from sequencehandler.filter_query import filter_query
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

if __name__ == "__main__":
    main()