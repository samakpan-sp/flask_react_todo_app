from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todos.db'
db = SQLAlchemy(app)
CORS(app)

class Todo(db.Mode):
    id = db.column(db.Integer, primary_key=True)
    content = db.column(db.String(200))
    done = db.column(db.Boolean, default=False)

@app.route('./todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    output = []
    for todo in todos:
        todo_data = {'id': todo.id, 'content':todo.content, 'done':todo.done}
        output.append(todo_data)
    return jsonify({'todos':output})

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = Todo(content=data['content'], done=False)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

