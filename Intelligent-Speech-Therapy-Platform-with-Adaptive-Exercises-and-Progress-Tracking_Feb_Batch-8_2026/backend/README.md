# 🎙️ Speech Therapy Backend API

A robust **FastAPI** backend for the Speech Therapy application with **JWT-based authentication**, **SQLite** database, and a complete user management flow.

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app entry point
│   ├── database.py           # SQLite DB connection & session
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic request/response schemas
│   ├── crud.py               # Database CRUD operations
│   ├── auth.py               # JWT token creation & verification
│   └── routers/
│       ├── __init__.py
│       └── users.py          # User authentication routes
├── speech_therapy.db         # SQLite database (auto-created)
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (SECRET_KEY, etc.)
└── README.md                 # This file
```

---

## ⚙️ Prerequisites

- Python **3.10+**
- pip
- Git (optional)

---

## 🚀 Getting Started

### 1. Clone / Navigate to the Backend Directory

```bash
cd backend
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv

# macOS / Linux
python3 -m venv venv
```

### 3. Activate the Virtual Environment

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

> ✅ You should see `(venv)` at the beginning of your terminal prompt.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file inside the `backend/` folder:

```env
SECRET_KEY=your_super_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ **Important:** Never commit your `.env` file to version control. Add it to `.gitignore`.

### 6. Run the Development Server

```bash
# From inside the backend/ directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be live at: **http://localhost:8000**

---

## 📖 Interactive API Documentation

FastAPI provides auto-generated docs out of the box:

| Tool         | URL                                      |
|--------------|------------------------------------------|
| Swagger UI   | http://localhost:8000/docs               |
| ReDoc        | http://localhost:8000/redoc              |

---

## 🔌 API Endpoints

### Base URL: `http://localhost:8000`

---

### 🔓 Authentication Routes — `/auth`

#### 1. Register a New User

| Field        | Value                     |
|--------------|---------------------------|
| **Method**   | `POST`                    |
| **Endpoint** | `/auth/register`          |
| **Auth**     | ❌ Not required            |

**Request Body (JSON):**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Success Response `201 Created`:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-02-28T10:00:00"
}
```

**Error Responses:**
- `400 Bad Request` — Email or username already registered

---

#### 2. Login (Get Access Token)

| Field        | Value                     |
|--------------|---------------------------|
| **Method**   | `POST`                    |
| **Endpoint** | `/auth/login`             |
| **Auth**     | ❌ Not required            |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Request Body (Form Data):**
```
username: john_doe
password: SecurePass123
```

**Success Response `200 OK`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` — Incorrect username or password

---

#### 3. Logout

| Field        | Value                     |
|--------------|---------------------------|
| **Method**   | `POST`                    |
| **Endpoint** | `/auth/logout`            |
| **Auth**     | ✅ Bearer Token required   |

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response `200 OK`:**
```json
{
  "message": "Successfully logged out"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid or missing token

---

### 👤 User Routes — `/users`

#### 4. Get Current User Details

| Field        | Value                     |
|--------------|---------------------------|
| **Method**   | `GET`                     |
| **Endpoint** | `/users/me`               |
| **Auth**     | ✅ Bearer Token required   |

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response `200 OK`:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-02-28T10:00:00"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid or expired token

---

## 🧪 Postman Testing Guide

### ⚠️ Common Mistakes — Read First!

| Mistake | Symptom | Fix |
|---|---|---|
| Using `GET` for login/logout/register | `405 Method Not Allowed` | Change method to **`POST`** |
| Sending login as JSON body | `422 Unprocessable Entity` | Login uses **form-data**, not JSON |
| Missing `Authorization` header | `401 Unauthorized` | Add Bearer token to **Auth tab** |
| Calling a protected route after logout | `401 Unauthorized` | Log in again to get a new token |
| Wrong Content-Type for register | `422 Unprocessable Entity` | Use `raw` → `JSON` for register |

---

### Step 1: Set Up Collection & Variables

1. Open **Postman** → Click **New Collection** → Name it `Speech Therapy API`
2. Go to **Collection → Variables** tab and add:

| Variable | Initial Value | Current Value |
|---|---|---|
| `base_url` | `http://localhost:8000` | `http://localhost:8000` |
| `access_token` | *(leave empty)* | *(auto-filled after login)* |

---

### Step 2: Health Check

| Field | Value |
|---|---|
| **Method** | `GET` |
| **URL** | `{{base_url}}/` |
| **Auth** | None |
| **Body** | None |

**Expected Response `200 OK`:**
```json
{
  "status": "ok",
  "message": "🎙️ Speech Therapy API is running!",
  "docs": "/docs"
}
```

---

### Step 3: Register a New User

| Field | Value |
|---|---|
| **Method** | `POST` ← must be POST |
| **URL** | `{{base_url}}/auth/register` |
| **Body tab** | `raw` → `JSON` |
| **Auth** | None |

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**✅ Success Response `201 Created`:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-02-28T10:00:00"
}
```

**❌ Error — Duplicate username/email `400 Bad Request`:**
```json
{
  "detail": "Username already registered. Please choose a different one."
}
```

**❌ Error — Invalid email format `422 Unprocessable Entity`:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address"
    }
  ]
}
```

---

### Step 4: Login (Get JWT Token)

> ⚠️ **Login uses `x-www-form-urlencoded`, NOT JSON.** This is required by the OAuth2 standard.

| Field | Value |
|---|---|
| **Method** | `POST` ← must be POST |
| **URL** | `{{base_url}}/auth/login` |
| **Body tab** | `x-www-form-urlencoded` |
| **Auth** | None |

**Body (form fields — NOT JSON):**

| Key | Value |
|---|---|
| `username` | `john_doe` |
| `password` | `SecurePass123` |

**✅ Success Response `200 OK`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX2RvZSIsImV4cCI6MTc0MDczNjQwMH0.abc123xyz",
  "token_type": "bearer"
}
```

**Auto-save token script — paste in the "Tests" tab:**
```javascript
const response = pm.response.json();
if (response.access_token) {
    pm.collectionVariables.set("access_token", response.access_token);
    console.log("✅ Token saved successfully!");
}
```

**❌ Error — Wrong credentials `401 Unauthorized`:**
```json
{
  "detail": "Incorrect username or password."
}
```

---

### Step 5: Get Current User Profile

| Field | Value |
|---|---|
| **Method** | `GET` |
| **URL** | `{{base_url}}/users/me` |
| **Auth tab** | Type: `Bearer Token`, Token: `{{access_token}}` |
| **Body** | None |

**✅ Success Response `200 OK`:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-02-28T10:00:00"
}
```

**❌ Error — No / invalid token `401 Unauthorized`:**
```json
{
  "detail": "Could not validate credentials. Please log in again."
}
```

---

### Step 6: Logout

> ⚠️ **Logout is a `POST` request, NOT a `GET` request.**  
> Sending `GET /auth/logout` will return `405 Method Not Allowed`.

| Field | Value |
|---|---|
| **Method** | `POST` ← must be POST, not GET |
| **URL** | `{{base_url}}/auth/logout` |
| **Auth tab** | Type: `Bearer Token`, Token: `{{access_token}}` |
| **Body** | None / empty |

**✅ Success Response `200 OK`:**
```json
{
  "message": "User 'john_doe' successfully logged out."
}
```

**❌ Error — Already logged out / token blacklisted `401 Unauthorized`:**
```json
{
  "detail": "Token has been invalidated. Please log in again."
}
```

---

### Step 7: Verify Token is Invalidated After Logout

Call `GET /users/me` again using the **same token** you just logged out with.

**Expected `401 Unauthorized`:**
```json
{
  "detail": "Token has been invalidated. Please log in again."
}
```

This confirms the server-side token blacklist is working correctly.

---

### 🔁 Full Flow Summary (Order to Test)

```
1. POST /auth/register   → Create account
2. POST /auth/login      → Get token (auto-saved to {{access_token}})
3. GET  /users/me        → View profile ✅ (should work)
4. POST /auth/logout     → Invalidate token
5. GET  /users/me        → View profile ❌ (should return 401)
6. POST /auth/login      → Login again to get a fresh token
```

---

### 🖥️ Quick Test with curl (Windows PowerShell)

```powershell
# 1. Register
curl -X POST http://localhost:8000/auth/register `
  -H "Content-Type: application/json" `
  -d '{"username":"john_doe","email":"john@example.com","password":"SecurePass123"}'

# 2. Login (form-data)
curl -X POST http://localhost:8000/auth/login `
  -d "username=john_doe&password=SecurePass123"

# 3. Get profile (replace TOKEN with actual token from login)
curl http://localhost:8000/users/me `
  -H "Authorization: Bearer TOKEN"

# 4. Logout (replace TOKEN)
curl -X POST http://localhost:8000/auth/logout `
  -H "Authorization: Bearer TOKEN"
```

---

## 📦 Dependencies (`requirements.txt`)

```
fastapi==0.110.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.29
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
python-dotenv==1.0.1
pydantic[email]==2.6.4
```

---

## 🔐 Security Notes

- Passwords are hashed using **bcrypt** before storage — never stored in plain text.
- JWT tokens use **HS256** algorithm with a secret key from your `.env`.
- Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30 minutes).
- Logout is handled by a **server-side token blacklist** stored in memory (upgradeable to Redis for production).

---

## 🗄️ Database

- **Engine:** SQLite (file-based, zero-config)
- **ORM:** SQLAlchemy
- **Database file:** `backend/speech_therapy.db` (auto-created on first run)
- No migrations needed for development; tables are created automatically via `create_all()`.

---

## 🛠️ Development Tips

```bash
# Check if server is running
curl http://localhost:8000

# View all registered routes
curl http://localhost:8000/openapi.json

# Deactivate virtual environment
deactivate
```

---

## 🚦 Quick Status Check

| Step                      | Command / Action                              | Expected Result         |
|---------------------------|-----------------------------------------------|-------------------------|
| Virtual env created       | `python -m venv venv`                         | `venv/` folder created  |
| Virtual env activated     | `.\venv\Scripts\Activate.ps1`                 | `(venv)` in prompt      |
| Dependencies installed    | `pip install -r requirements.txt`             | No errors               |
| Server running            | `uvicorn app.main:app --reload`               | `Uvicorn running on...` |
| Docs accessible           | Open http://localhost:8000/docs               | Swagger UI visible      |
| Register works            | `POST /auth/register`                         | `201 Created`           |
| Login works               | `POST /auth/login`                            | Token returned          |
| Protected route works     | `GET /users/me` with token                    | User details returned   |
| Logout works              | `POST /auth/logout` with token                | Logout message          |

---

*Built with ❤️ using FastAPI · SQLite · JWT · Passlib*
