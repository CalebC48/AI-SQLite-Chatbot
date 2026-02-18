from openai_client import OpenAIClient
from sqlite_manager import SQLiteManager


class QueryProcessor:
    """
    Orchestrates the flow of processing natural language queries:
    1. Converts NLQ to SQL using OpenAI
    2. Executes SQL on SQLite database
    3. Formats results using OpenAI
    4. Returns final response
    """

    def __init__(self, db_manager: SQLiteManager, ai_client: OpenAIClient):
        """
        Initialize query processor

        Args:
            db_manager: SQLiteManager instance
            ai_client: OpenAIClient instance
        """
        self.db_manager = db_manager
        self.ai_client = ai_client

    def process_query(self, question: str) -> str:
        """
        Processes a natural language question about the database

        Args:
            question: Natural language question

        Returns:
            Formatted natural language response
        """
        # Step 1: Get database schema
        schema = self.db_manager.get_schema()

        # Step 2: Convert natural language question to SQL
        print("Converting question to SQL...", flush=True)
        sql_query = self.ai_client.convert_to_sql(question, schema)
        print(f"Generated SQL: {sql_query}", flush=True)

        # Step 3: Execute SQL query
        print("Executing SQL query...", flush=True)
        results = self.db_manager.execute_query(sql_query)
        print("Query results retrieved.", flush=True)

        # Step 4: Format results into natural language response
        print("Formatting response...", flush=True)
        response = self.ai_client.format_response(question, sql_query, results)

        return response
