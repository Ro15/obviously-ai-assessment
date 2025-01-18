# FastAPI Books API

This is a FastAPI-based application for managing books using an SQLite database (`books.db`). It includes endpoints for authentication, CRUD operations, and real-time updates via Server-Sent Events (SSE).

---

## **Features**
- User authentication using JWT.
- CRUD operations for managing books.
- Real-time updates using SSE.
- Role-based access control (Admin/Regular User).
- Fully documented API with OpenAPI integration at `/docs`.

---

## **Tech Stack**
- **Python**: Core programming language.
- **FastAPI**: Web framework.
- **SQLite**: Database.
- **SQLAlchemy**: ORM for database interaction.
- **pytest**: Testing framework.

---

## **Setup Instructions**
### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/fastapi-books-api.git
cd fastapi-books-api

python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
