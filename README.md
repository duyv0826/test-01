# test-01

My first test repository - A collection of practical Python utilities and examples.

## 📋 Features

This repository contains a set of practical, production-ready Python modules:

- **`utils.py`** - Common utility functions (file I/O, hashing, data transformation)
- **`config_manager.py`** - Singleton configuration manager with JSON support
- **`logger.py`** - Simple logging utility with file and console output
- **`api_client.py`** - HTTP API client with automatic retries and error handling
- **`db_helper.py`** - SQLite database helper with CRUD operations
- **`data_processor.py`** - Data processing utilities (CSV, JSON, Excel) with pandas
- **`web_scraper.py`** - Web scraper with BeautifulSoup support
- **`api_app.py`** - FastAPI application example with CRUD operations
- **`main.py`** - Main application entry point with practical examples

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/duyv0826/test-01.git
cd test-01
```

### 2. Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the examples

```bash
python main.py
```

Check the `output/` directory for generated files and `logs/` for log output.

## 📚 Module Usage Examples

### utils.py - Utility Functions

```python
from utils import read_file, write_file, calculate_md5, get_timestamp

# Read/write files
content = read_file('input.txt')
write_file('output.txt', 'Hello, World!')

# Calculate hashes
md5_hash = calculate_md5('hello')
sha_hash = calculate_sha256('hello')

# Get timestamp
timestamp = get_timestamp('%Y-%m-%d %H:%M:%S')

# Flatten nested dictionary
nested = {'a': {'b': 1, 'c': 2}}
flat = flatten_dict(nested)  # {'a.b': 1, 'a.c': 2}

# Chunk list
chunks = chunk_list([1,2,3,4,5], 2)  # [[1,2], [3,4], [5]]
```

### config_manager.py - Configuration Management

```python
from config_manager import ConfigManager

# Load or create config (singleton)
config = ConfigManager()

if not config.load('config.json'):
    config.from_dict({
        'app_name': 'My App',
        'database': {'host': 'localhost', 'port': 5432}
    })
    config.save('config.json')

# Get values (dot notation)
app_name = config.get('app_name')
db_host = config.get('database.host')
db_port = config.get('database.port', 5432)  # With default

# Set values
config.set('database.port', 5433)
config.set('new_setting', 'value')
config.save()
```

### logger.py - Logging Utility

```python
from logger import Logger, get_logger

# Create logger
log = Logger('my_app')

# Log messages
log.debug('Debug message')
log.info('Application started')
log.warning('Warning message')
log.error('Error occurred', exc_info=True)

# Or use singleton
log = get_logger('my_app')
```

### api_client.py - API Client

```python
from api_client import APIClient

# Create client
client = APIClient(
    base_url='https://api.example.com',
    token='your-token',
    timeout=30,
    max_retries=3
)

# GET request
response = client.get('/users')

# POST request
response = client.post('/users', json_data={'name': 'Alice'})

# PUT request
response = client.put('/users/1', json_data={'name': 'Bob'})

# DELETE request
response = client.delete('/users/1')
```

### db_helper.py - Database Helper

```python
from db_helper import DBHelper

# Create helper
db = DBHelper('app.db')

# Create table
db.create_table('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    )
''')

# Insert
db.insert('users', {'name': 'Alice', 'email': 'alice@example.com'})

# Query
users = db.query('SELECT * FROM users')
for user in users:
    print(f"{user['name']} ({user['email']})")

# Update
db.update('users', {'name': 'Bob'}, 'WHERE id = ?', (1,))

# Delete
db.delete('users', 'WHERE id = ?', (1,))

# Close
db.close()
```

### data_processor.py - Data Processing

```python
from data_processor import DataProcessor

processor = DataProcessor()

# Read data
data = processor.read_csv('data.csv')
data = processor.read_json('data.json')
data = processor.read_excel('data.xlsx')

# Process data
filtered = processor.filter_by_column(data, 'age', lambda x: x > 25)
sorted_data = processor.sort_by_column(data, 'name')
grouped = processor.group_by_column(data, 'city')
stats = processor.get_statistics(data, 'salary')

# Write data
processor.write_csv('output.csv', data)
processor.write_json('output.json', data)
processor.write_excel('output.xlsx', data)
```

### web_scraper.py - Web Scraper

```python
from web_scraper import WebScraper

scraper = WebScraper()

# GET request
response = scraper.get('https://example.com')

# Download file
scraper.download_file('https://example.com/file.pdf', 'output/file.pdf')

# Parse HTML (requires beautifulsoup4)
# pip install beautifulsoup4
title = scraper.get_title(response.text)
links = scraper.get_links(response.text)
text = scraper.get_text(response.text)
```

### api_app.py - FastAPI Application

```bash
# Run the API server
uvicorn api_app:app --reload --host 0.0.0.0 --port 8000
```

Then visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

API Endpoints:
- `GET /` - Health check
- `GET /users` - Get all users (with pagination)
- `GET /users/{id}` - Get user by ID
- `POST /users` - Create new user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user
- `GET /stats` - Get statistics

## 🧪 Running Tests

```bash
# Run all tests
pytest test_utils.py -v

# Run with coverage
pytest test_utils.py --cov=utils --cov-report=html
```

## 📂 Project Structure

```
test-01/
├── __init__.py           # Package initialization
├── utils.py              # Utility functions
├── config_manager.py     # Configuration management
├── logger.py             # Logging utility
├── api_client.py         # HTTP API client
├── db_helper.py          # Database helper (SQLite)
├── data_processor.py     # Data processing (pandas)
├── web_scraper.py        # Web scraper (BeautifulSoup)
├── api_app.py            # FastAPI application
├── main.py               # Main application
├── test_utils.py         # Unit tests
├── requirements.txt      # Dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Python gitignore
├── LICENSE              # Apache 2.0 License
├── README.md            # This file
├── CONTRIBUTING.md      # Contribution guidelines
├── CHANGELOG.md         # Changelog
├── output/               # Output directory (generated)
└── logs/                # Log directory (generated)
```

## 🛠️ Development

### Code Style

This project follows PEP 8. Please format your code before submitting:

```bash
# Install formatters
pip install black isort flake8

# Format code
black .
isort .

# Lint
flake8
```

### Git Workflow

1. Create feature branch (`git checkout -b feature/your-feature`)
2. Make changes and commit (`git commit -m "Add: your feature"`)
3. Push to branch (`git push origin feature/your-feature`)
4. Create Pull Request to `dev` or `main` branch
5. Code review and merge

## 📝 License

This project is licensed under the Apache License 2.0 - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📧 Contact

- GitHub: [@duyv0826](https://github.com/duyv0826)
- Issues: [https://github.com/duyv0826/test-01/issues](https://github.com/duyv0826/test-01/issues)

---

⭐ If you find this project useful, please give it a star!
