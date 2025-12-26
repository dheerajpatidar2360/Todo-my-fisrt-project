from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# ---------------------------------------------------------------------
# App and extension setup
# ---------------------------------------------------------------------

app = Flask(__name__)

# Enable CORS for all routes and all origins (simple for teaching)
CORS(app)

# ---------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------

# Use SQLite database file named "todo.db" in the project folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------------------------------------------------------------
# Database models
# ---------------------------------------------------------------------

class Todo(db.Model):
    """
    A simple database model for a todo item.

    Fields (match the exercise exactly):
    - id: Integer, primary key
    - title: String, required
    - description: String, optional
    - is_completed: Boolean, default = False
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        """Return data in a JSON-friendly format."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_completed": self.is_completed,
        }


# ---------------------------------------------------------------------
# Simple REST API routes
# ---------------------------------------------------------------------

@app.route("/")
def index():
    """
    A simple "health check" route.
    Visit: http://localhost:5000/
    """
    return jsonify({"message": "Flask API is running"}), 200


@app.route("/todos", methods=["GET"])
def get_todos():
    """
    GET /todos
    Returns a list of all todo items in the database.
    """
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos]), 200


@app.route("/todos", methods=["POST"])
def create_todo():
    """
    POST /todos
    Create a new todo item.

    Expected JSON body:
    {
        "title": "Buy milk",        # required
        "description": "2 liters",  # optional
        "is_completed": false       # optional, defaults to False
    }
    """
    data = request.get_json(silent=True)

    # Ensure we received valid JSON
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get("title")
    description = data.get("description")
    is_completed = data.get("is_completed", False)

    # Validate required field: title
    if not title:
        return jsonify({"error": '"title" is required'}), 400

    # Create and save the new todo
    new_todo = Todo(
        title=title,
        description=description,
        is_completed=bool(is_completed),
    )
    db.session.add(new_todo)
    db.session.commit()

    # Return the newly created todo with 201 Created
    return jsonify(new_todo.to_dict()), 201


@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    """
    PUT /todos/<id>
    Update an existing todo item.

    Expected JSON body (all fields optional, only what you want to change):
    {
        "title": "New title",
        "description": "New description",
        "is_completed": true
    }
    """
    data = request.get_json(silent=True)

    # Ensure we received valid JSON
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Find the todo by ID
    todo = Todo.query.get(id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    # Update allowed fields only if they are provided
    if "title" in data:
        todo.title = data["title"]
    if "description" in data:
        todo.description = data["description"]
    if "is_completed" in data:
        todo.is_completed = bool(data["is_completed"])

    db.session.commit()

    # Return the updated todo
    return jsonify(todo.to_dict()), 200


@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    """
    DELETE /todos/<id>
    Remove an existing todo item.
    """
    # Find the todo by ID
    todo = Todo.query.get(id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    # Delete the todo from the database
    db.session.delete(todo)
    db.session.commit()

    # Return a simple success message
    return jsonify({"message": "Todo deleted successfully"}), 200


# ---------------------------------------------------------------------
# App entry point
# ---------------------------------------------------------------------

def create_tables():
    """
    Create the database tables if they do not exist yet.

    This function is called once when the server starts.
    """
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    # Auto-create tables before the first request
    create_tables()

    # Run the development server on http://localhost:5000
    app.run(host="127.0.0.1", port=5000, debug=True)


