import os
import requests
from dotenv import load_dotenv


class OpenAIClient:
    """Client for interacting with OpenAI API"""

    def __init__(self):
        """Initialize OpenAI client and load credentials from environment or .env file"""
        load_dotenv()

        self.base_url = "https://api.openai.com/v1"
        self.api_key = None
        self.org_id = None

        if not self._load_credentials():
            raise RuntimeError(
                "Failed to load OpenAI credentials. "
                "Please set OPENAI_API_KEY environment variable or create a .env file."
            )

    def _load_credentials(self) -> bool:
        """Load API key and organization ID from environment variables or .env file"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.org_id = os.getenv("OPENAI_ORG_ID")

        if not self.api_key:
            return False

        return True

    def _make_request(self, endpoint: str, payload: dict) -> dict:
        """Make HTTP POST request to OpenAI API"""
        url = f"{self.base_url}{endpoint}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        if self.org_id:
            headers["OpenAI-Organization"] = self.org_id

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"OpenAI API request failed: {e}")

    def send_prompt(self, prompt: str, model: str = "gpt-4.1", temperature: float = 0.3) -> str:
        """
        Sends a prompt to OpenAI API and returns the response

        Args:
            prompt: The prompt to send
            model: The model to use (default: gpt-4.1)
            temperature: Temperature for response randomness

        Returns:
            The response text from OpenAI
        """
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }

        response = self._make_request("/chat/completions", payload)

        # Extract message content from response
        try:
            content = response["choices"][0]["message"]["content"]
            return content.strip()
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Failed to parse OpenAI response: {e}")

    def convert_to_sql(self, question: str, schema: str, use_few_shot: bool = False, examples: list = None) -> str:
        """
        Converts natural language question to SQL query using either zero-shot or few-shot prompting

        Args:
            question: Natural language question about the database
            schema: Schema information about the database
            use_few_shot: Whether to use few-shot prompting (default: False for zero-shot)
            examples: List of (question, sql_query) tuples for few-shot examples

        Returns:
            SQL query string
        """
        if use_few_shot and examples:
            # Few-shot prompting: include example question-SQL pairs
            examples_text = "\n\n".join([
                f"Question: {ex_question}\nSQL: {ex_sql}"
                for ex_question, ex_sql in examples
            ])

            prompt = f"""You are a SQL expert. Given the following database schema:

{schema}

Here are some example questions and their corresponding SQL queries for this database:

{examples_text}

Now convert the following natural language question into a SQLite SQL query:
{question}

Return ONLY the SQL query, nothing else. Do not include explanations or markdown formatting."""
        else:
            # Zero-shot prompting: no examples, just schema and question
            prompt = f"""You are a SQL expert. Given the following database schema:

{schema}

Convert the following natural language question into a SQLite SQL query:
{question}

Return ONLY the SQL query, nothing else. Do not include explanations or markdown formatting."""

        sql_query = self.send_prompt(prompt)

        # Clean up the SQL query (remove markdown code blocks if present)
        sql_query = sql_query.strip()

        # Remove markdown code blocks
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        elif sql_query.startswith("```"):
            sql_query = sql_query[3:]

        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]

        return sql_query.strip()

    def format_response(self, question: str, sql_query: str, results: str) -> str:
        """
        Converts SQL query results to natural language response

        Args:
            question: Original natural language question
            sql_query: The SQL query that was executed
            results: The query results in a formatted string

        Returns:
            Natural language response
        """
        prompt = f"""A user asked: "{question}"

The following SQL query was executed:
{sql_query}

The EXACT results from the database are:
{results}

IMPORTANT: You must ONLY use the numbers and data shown in the results above. Do NOT make up, estimate, or calculate any numbers that are not explicitly shown in the results. If the results show specific values, use those exact values. If you need to calculate something, show the calculation using only the numbers from the results.

Provide a clear, natural language answer to the user's question based EXCLUSIVELY on these results."""

        return self.send_prompt(prompt)
