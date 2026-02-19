#!/usr/bin/env python3
"""
AI-SQLite-Chatbot - Interactive natural language query tool for SQLite databases
"""

import argparse
import sys
from openai_client import OpenAIClient
from sqlite_manager import SQLiteManager
from query_processor import QueryProcessor

DEFAULT_DB_PATH = "centralglass_recon.sqlite"

def print_welcome(db_path: str):
    """Print welcome message"""
    print("\n" + "="*60)
    print("  AI-SQLite-Chatbot - Interactive Database Query Tool")
    print("="*60)
    print(f"\nConnected to database: {db_path}")
    print("\nYou can now ask questions about your database in natural language.")
    print("Type 'exit', 'quit', or 'q' to end the session.")
    print("Type 'help' for more information.\n")
    print("-"*60 + "\n")


def print_help():
    """Print help message"""
    print("\nCommands:")
    print("  help, ?          - Show this help message")
    print("  exit, quit, q    - Exit the program")
    print("\nYou can ask questions like:")
    print("  - How many records are in the users table?")
    print("  - What is the average age of all users?")
    print("  - Show me all products with price greater than 100")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Interactive natural language query tool for SQLite databases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  OPENAI_API_KEY        Your OpenAI API key (required)
  OPENAI_ORG_ID          Your OpenAI organization ID (optional)

Examples:
  %(prog)s                    # Start interactive session with default database
  %(prog)s -d mydb.db         # Start interactive session with specific database
        """
    )

    parser.add_argument(
        "-d", "--database",
        default=DEFAULT_DB_PATH,
        help=f"Path to SQLite database file (default: {DEFAULT_DB_PATH})"
    )

    args = parser.parse_args()

    try:
        db_manager = SQLiteManager()
        ai_client = OpenAIClient()
        processor = QueryProcessor(db_manager, ai_client)

        if not db_manager.open_database(args.database):
            print(f"Error: Failed to open database at {args.database}", file=sys.stderr)
            return 1

        print_welcome(args.database)

        while True:
            try:
                question = input("You: ").strip()

                if not question:
                    continue

                if question.lower() in ['exit', 'quit', 'q']:
                    print("\nGoodbye!\n")
                    break

                if question.lower() in ['help', '?']:
                    print_help()
                    continue

                print()
                try:
                    response = processor.process_query(question)
                    print(f"\nAssistant: {response}\n")
                    print("-"*60 + "\n")
                except Exception as e:
                    print(f"\nError: {e}\n")
                    print("-"*60 + "\n")

            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                break
            except EOFError:
                print("\n\nGoodbye!\n")
                break

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
