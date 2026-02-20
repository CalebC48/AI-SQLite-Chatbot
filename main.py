#!/usr/bin/env python3
"""
AI-SQLite-Chatbot - Interactive natural language query tool for SQLite databases
"""

import argparse
import sys
import os
from openai_client import OpenAIClient
from sqlite_manager import SQLiteManager
from query_processor import QueryProcessor
from few_shot_examples import FEW_SHOT_EXAMPLES

DEFAULT_DB_PATH = "centralglass_recon.sqlite"

def print_welcome(db_path: str, strategy_info: str = ""):
    """Print welcome message"""
    print("\n" + "="*60)
    print("  AI-SQLite-Chatbot - Interactive Database Query Tool")
    print("="*60)
    print(f"\nConnected to database: {db_path}")
    if strategy_info:
        print(f"{strategy_info}")
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

    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Hide SQL query and raw results debugging information"
    )

    args = parser.parse_args()

    try:
        db_manager = SQLiteManager()
        ai_client = OpenAIClient()

        # Determine if we should use few-shot prompting (only for default database)
        is_default_db = os.path.basename(args.database) == DEFAULT_DB_PATH or args.database == DEFAULT_DB_PATH
        use_few_shot = is_default_db
        examples = FEW_SHOT_EXAMPLES if use_few_shot else None

        processor = QueryProcessor(db_manager, ai_client, use_few_shot=use_few_shot, examples=examples)

        if not db_manager.open_database(args.database):
            print(f"Error: Failed to open database at {args.database}", file=sys.stderr)
            return 1

        # Show which prompting strategy is being used
        strategy_info = "Using few-shot prompting" if use_few_shot else "Using zero-shot prompting"
        print_welcome(args.database, strategy_info)

        # Track debug mode (can be toggled)
        show_debug = not args.no_debug

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

                if question.lower() == 'debug':
                    show_debug = not show_debug
                    print(f"\nDebug mode: {'ON' if show_debug else 'OFF'}\n")
                    continue

                print()
                try:
                    response = processor.process_query(question, show_debug=show_debug)
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
