# AI-SQLite-Chatbot

A Python command-line tool that allows you to ask natural language questions about a SQLite database. The tool uses OpenAI's API to convert questions to SQL queries, executes them, and formats the results into natural language responses.

## Features

- Natural language to SQL conversion using OpenAI API
- SQLite database query execution
- Natural language response formatting
- Configurable database path (with default)
- Secure API key management via environment variables
- Simple setup - no compilation needed!

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd AI-SQLite-Chatbot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

That's it! No compilation, no complex build systems.

## Configuration

You can configure the API key using either a `.env` file (recommended) or environment variables.

### Option 1: Using a .env file (Recommended)

1. Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-api-key-here
OPENAI_ORG_ID=your-org-id-here  # Optional
```

2. The `.env` file is automatically loaded when you run the script.

**Note:** Make sure `.env` is in your `.gitignore` (it already is) to keep your API key secure!

### Option 2: Environment Variables

You can also set environment variables directly:

#### Linux/macOS

```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_ORG_ID="your-org-id-here"  # Optional
```

#### Windows (Command Prompt)

```cmd
set OPENAI_API_KEY=your-api-key-here
set OPENAI_ORG_ID=your-org-id-here
```

#### Windows (PowerShell)

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
$env:OPENAI_ORG_ID="your-org-id-here"
```

#### Windows (Git Bash)

```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_ORG_ID="your-org-id-here"
```

**Note:** Environment variables take precedence over `.env` file values if both are set.

## Usage

### Basic Usage

```bash
python main.py "How many users are in the database?"
```

### Specify Database

```bash
python main.py -d path/to/database.db "What is the average age of users?"
```

### Help

```bash
python main.py --help
```

### Make it executable (Linux/macOS)

```bash
chmod +x main.py
./main.py "How many users are in the database?"
```

## Project Structure

```
AI-SQLite-Chatbot/
├── main.py                 # Entry point and CLI
├── openai_client.py        # OpenAI API client
├── sqlite_manager.py       # SQLite database manager
├── query_processor.py      # Query orchestration
├── requirements.txt        # Python dependencies
├── .env                    # Your API keys (create this, not in git)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## How It Works

1. **Question Input**: User provides a natural language question via command line
2. **Schema Retrieval**: The tool retrieves the database schema (tables and columns)
3. **SQL Generation**: OpenAI API converts the natural language question to a SQL query
4. **Query Execution**: The SQL query is executed on the SQLite database
5. **Response Formatting**: OpenAI API formats the results into a natural language response
6. **Output**: The formatted response is displayed to the user

## Default Database

If no database path is specified, the tool defaults to `database.db` in the current directory.

## Error Handling

The tool will report errors for:

- Missing OpenAI API key
- Invalid database path
- SQL query execution failures
- API communication errors

## Dependencies

- `requests` - For HTTP requests to OpenAI API
- `python-dotenv` - For loading `.env` file
- `sqlite3` - Built into Python standard library

## Example

```bash
# Option 1: Using .env file (create .env with OPENAI_API_KEY=sk-...)
python main.py "How many records are in the users table?"

# Option 2: Using environment variable
export OPENAI_API_KEY="sk-..."
python main.py "How many records are in the users table?"

# Output:
# Converting question to SQL...
# Generated SQL: SELECT COUNT(*) FROM users;
# Executing SQL query...
# Query results retrieved.
# Formatting response...
#
# There are 42 records in the users table.
```

## License

See LICENSE file for details.
