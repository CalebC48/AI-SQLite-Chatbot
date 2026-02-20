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

    def __init__(self, db_manager: SQLiteManager, ai_client: OpenAIClient, use_few_shot: bool = False, examples: list = None):
        """
        Initialize query processor

        Args:
            db_manager: SQLiteManager instance
            ai_client: OpenAIClient instance
            use_few_shot: Whether to use few-shot prompting (default: False)
            examples: List of (question, sql_query) tuples for few-shot examples
        """
        self.db_manager = db_manager
        self.ai_client = ai_client
        self.use_few_shot = use_few_shot
        self.examples = examples

    def process_query(self, question: str, show_debug: bool = True) -> str:
        """
        Processes a natural language question about the database

        Args:
            question: Natural language question
            show_debug: Whether to show SQL query and raw results (default: True)

        Returns:
            Formatted natural language response
        """
        # Step 1: Get database schema
        schema = self.db_manager.get_schema()

        # Step 2: Convert natural language question to SQL
        strategy = "few-shot" if self.use_few_shot else "zero-shot"
        print(f"Converting question to SQL ({strategy})...", end=" ", flush=True)
        sql_query = self.ai_client.convert_to_sql(question, schema, self.use_few_shot, self.examples)
        print("✓")

        if show_debug:
            print(f"\n[DEBUG] Generated SQL:\n{sql_query}\n")

        # Step 3: Execute SQL query
        print("Executing SQL query...", end=" ", flush=True)
        results = self.db_manager.execute_query(sql_query)
        print("✓")

        if show_debug:
            print(f"\n[DEBUG] Raw Query Results:\n{results}\n")

        # Step 4: Format results into natural language response
        print("Formatting response...", end=" ", flush=True)
        response = self.ai_client.format_response(question, sql_query, results)
        print("✓")

        return response
