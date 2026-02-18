import argparse
import sys
from openai_client import OpenAIClient
from sqlite_manager import SQLiteManager
from query_processor import QueryProcessor

DEFAULT_DB_PATH = "database.db"


def main():
    parser = argparse.ArgumentParser(
        description="Ask natural language questions about a SQLite database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  OPENAI_API_KEY        Your OpenAI API key (required)
  OPENAI_ORG_ID          Your OpenAI organization ID (optional)

Examples:
  %(prog)s "How many users are in the database?"
  %(prog)s -d mydb.db "What is the average age of users?"
        """
    )

    parser.add_argument(
        "-d", "--database",
        default=DEFAULT_DB_PATH,
        help=f"Path to SQLite database file (default: {DEFAULT_DB_PATH})"
    )

    parser.add_argument(
        "question",
        nargs="+",
        help="Natural language question about the database"
    )

    args = parser.parse_args()

    question = " ".join(args.question)

    try:
        db_manager = SQLiteManager()
        ai_client = OpenAIClient()
        processor = QueryProcessor(db_manager, ai_client)

        if not db_manager.open_database(args.database):
            print(f"Error: Failed to open database at {args.database}", file=sys.stderr)
            return 1

        response = processor.process_query(question)
        print(f"\n{response}\n")

        db_manager.close_database()

        return 0

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
