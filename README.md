## Beginner-Friendly Flask REST API Backend

This is a very small Flask project that shows how to build a beginner-friendly REST API with:

- **Flask** (web framework)
- **Flask-CORS** (to allow requests from any front-end)
- **Flask-SQLAlchemy** with **SQLite** (`todo.db` file)

### Project structure

- **`app.py`** – main application file (Flask app, database model, routes)
- **`requirements.txt`** – Python dependencies to install
- **`todo.db`** – SQLite database file (auto-created when you run the app)

### 1. Create and activate a virtual environment (recommended)

On Windows PowerShell:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Flask server

```bash
python app.py
```

You should see Flask start on `http://localhost:5000`.

### 4. Test the API

- **Health check**
  - Method: `GET`
  - URL: `http://localhost:5000/`

- **Get all todos**
  - Method: `GET`
  - URL: `http://localhost:5000/todos`

The database tables (for the `Todo` model) are automatically created when the server starts, and the SQLite file is named `todo.db` in the project folder.


