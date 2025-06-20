import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000/todos";

function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const fetchTodos = async () => {
    try {
      const res = await axios.get(`${API_URL}/`);
      setTodos(res.data);
    } catch (err) {
      console.error("Ошибка получения задач:", err);
    }
  };

  const addTodo = async () => {
    if (!title.trim()) return;
    try {
      const res = await axios.post(`${API_URL}/add`, {
        title,
        description,
        status: "not_started", // по умолчанию
      });
      setTodos([...todos, res.data]);
      setTitle("");
      setDescription("");
    } catch (err) {
      console.error("Ошибка при добавлении:", err);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}/delete`);
      setTodos(todos.filter((todo) => todo.id !== id));
    } catch (err) {
      console.error("Ошибка удаления:", err);
    }
  };

  const updateStatus = async (id, action) => {
    try {
      const res = await axios.patch(`${API_URL}/${id}/${action}`);
      setTodos((prev) =>
        prev.map((todo) => (todo.id === id ? res.data : todo))
      );
    } catch (err) {
      console.error(`Ошибка при ${action}:`, err);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>📋 ToDo App</h1>

      <div style={styles.form}>
        <input
          style={styles.input}
          placeholder="Название задачи"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          style={styles.textarea}
          placeholder="Описание задачи"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button style={styles.addButton} onClick={addTodo}>
          ➕ Добавить
        </button>
      </div>

      <ul style={styles.todoList}>
        {todos.map((todo) => (
          <li key={todo.id} style={styles.todoCard}>
            <h3>{todo.title}</h3>
            <p>{todo.description}</p>
            <p>
              <strong>Статус:</strong> {todo.status}
            </p>
            <div style={styles.buttonRow}>
              <button onClick={() => updateStatus(todo.id, "not-start")} style={styles.statusButton}>
                ⏹ Not started
              </button>
              <button onClick={() => updateStatus(todo.id, "activate")} style={styles.statusButton}>
                ▶️ Activate
              </button>
              <button onClick={() => updateStatus(todo.id, "archive")} style={styles.statusButton}>
                📦 Archive
              </button>
              <button onClick={() => deleteTodo(todo.id)} style={styles.deleteButton}>
                ❌ Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 700,
    margin: "auto",
    padding: 20,
    fontFamily: "Arial, sans-serif",
  },
  heading: {
    textAlign: "center",
    marginBottom: 30,
  },
  form: {
    marginBottom: 30,
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  input: {
    padding: 10,
    fontSize: 16,
  },
  textarea: {
    padding: 10,
    fontSize: 14,
    minHeight: 60,
  },
  addButton: {
    padding: "10px 20px",
    fontSize: 16,
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    cursor: "pointer",
    borderRadius: 5,
    alignSelf: "flex-start",
  },
  todoList: {
    listStyle: "none",
    padding: 0,
  },
  todoCard: {
    border: "1px solid #ccc",
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    backgroundColor: "#f9f9f9",
  },
  buttonRow: {
    marginTop: 10,
    display: "flex",
    flexWrap: "wrap",
    gap: 10,
  },
  statusButton: {
    padding: "6px 10px",
    fontSize: 14,
    backgroundColor: "#e0e0e0",
    border: "none",
    borderRadius: 5,
    cursor: "pointer",
  },
  deleteButton: {
    padding: "6px 10px",
    fontSize: 14,
    backgroundColor: "#ff4d4f",
    color: "white",
    border: "none",
    borderRadius: 5,
    cursor: "pointer",
  },
};

export default App;
