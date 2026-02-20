import sqlite3
from typing import List, Tuple, Optional


class SQLiteManager:
    """Manages SQLite database operations"""

    def __init__(self):
        self.db: Optional[sqlite3.Connection] = None
        self.is_open = False

    def open_database(self, db_path: str) -> bool:
        """
        Opens a connection to the SQLite database

        Args:
            db_path: Path to the SQLite database file

        Returns:
            True if successful, False otherwise
        """
        if self.is_open:
            self.close_database()

        try:
            self.db = sqlite3.connect(db_path)
            self.is_open = True
            return True
        except sqlite3.Error as e:
            print(f"Error opening database: {e}", file=__import__('sys').stderr)
            return False

    def close_database(self):
        """Closes the database connection"""
        if self.db:
            self.db.close()
            self.db = None
        self.is_open = False

    def execute_query(self, query: str) -> str:
        """
        Executes a SQL query and returns results as formatted string

        Args:
            query: SQL query to execute

        Returns:
            Formatted string representation of results
        """
        if not self.is_open or not self.db:
            raise RuntimeError("Database is not open")

        try:
            cursor = self.db.cursor()
            cursor.execute(query)

            columns = [description[0] for description in cursor.description]

            rows = cursor.fetchall()

            if not columns:
                return "Query executed successfully (no results)"

            col_widths = [len(col) for col in columns]
            for row in rows:
                for i, cell in enumerate(row):
                    cell_str = str(cell) if cell is not None else "NULL"
                    col_widths[i] = max(col_widths[i], len(cell_str))

            output_lines = []

            header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
            output_lines.append(header)

            separator = "-+-".join("-" * col_widths[i] for i in range(len(columns)))
            output_lines.append(separator)

            if rows:
                for row in rows:
                    row_str = " | ".join(
                        (str(cell) if cell is not None else "NULL").ljust(col_widths[i])
                        for i, cell in enumerate(row)
                    )
                    output_lines.append(row_str)
            else:
                output_lines.append("(No rows returned)")

            return "\n".join(output_lines)

        except sqlite3.Error as e:
            raise RuntimeError(f"SQL query failed: {e}")

    def get_schema(self) -> str:
        """
        Gets the database schema as a formatted string with business context

        Returns:
            Schema information including tables and columns with business context
        """
        if not self.is_open or not self.db:
            return "Database not open"

        try:
            tables = self._get_table_names()
            if not tables:
                return "No tables found in database"

            schema_lines = ["Database Schema:\n"]

            business_context = {
                "invoice": "REVENUE: Invoices sent to customers (money coming in). Use invoice.total_amount for revenue calculations.",
                "payment": "REVENUE: Actual payments received from customers for invoices. Use payment.amount for actual cash received.",
                "expense": "COSTS: Expenses paid to vendors/suppliers (money going out). Use expense.amount for cost calculations.",
                "job": "Jobs/work performed for customers. Links customers to companies.",
                "company": "Companies in the system (e.g., 'Central Glass DC', 'Recon Pest Control').",
                "customer": "Customers who receive services.",
                "employee": "Employees who work for companies.",
                "payroll": "Employee payroll records (costs).",
            }

            for table_name in tables:
                schema_lines.append(f"Table: {table_name}")
                if table_name in business_context:
                    schema_lines.append(f"  NOTE: {business_context[table_name]}")
                columns = self._get_table_columns(table_name)

                for col_name, col_type in columns:
                    schema_lines.append(f"  - {col_name} ({col_type})")

                schema_lines.append("")

            schema_lines.append("\nIMPORTANT BUSINESS RULES:")
            schema_lines.append("- Revenue = sum of payment.amount for a company (actual money received from customers)")
            schema_lines.append("- Expenses = sum of expense.amount for a company (ALL expenses, not just those linked to specific jobs)")
            schema_lines.append("- Profit = Revenue - Expenses (calculate separately, then subtract)")
            schema_lines.append("- For profit calculations: Use separate subqueries for revenue and expenses, then subtract")
            schema_lines.append("- Example profit query: SELECT (SELECT SUM(p.amount) FROM payment p JOIN invoice i ON p.invoice_id = i.invoice_id JOIN company c ON i.company_id = c.company_id WHERE c.name = 'X') - (SELECT SUM(e.amount) FROM expense e JOIN company c ON e.company_id = c.company_id WHERE c.name = 'X')")
            schema_lines.append("- Do NOT join expenses through jobs/invoices for profit - use ALL company expenses")
            schema_lines.append("")

            return "\n".join(schema_lines)

        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to retrieve schema: {e}")

    def _get_table_names(self) -> List[str]:
        """Gets table names in the database"""
        if not self.db:
            return []

        cursor = self.db.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        return [row[0] for row in cursor.fetchall()]

    def _get_table_columns(self, table_name: str) -> List[Tuple[str, str]]:
        """Gets column information for a specific table"""
        if not self.db:
            return []

        cursor = self.db.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = []
        for row in cursor.fetchall():
            col_name = row[1]
            col_type = row[2] if row[2] else "TEXT"
            columns.append((col_name, col_type))

        return columns

    def is_open(self) -> bool:
        """Checks if database is open"""
        return self.is_open
