# API Documentation

## Authentication

All endpoints except `/api/token` and `/api/token/refresh` require JWT authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

### Token Endpoints

#### 1. Obtain Token
- **URL:** `/api/token/`
- **Method:** `POST`
- **Description:** Get JWT tokens for authentication
- **Request Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
- **Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 2. Refresh Token
- **URL:** `/api/token/refresh/`
- **Method:** `POST`
- **Description:** Refresh expired access token
- **Request Body:**
```json
{
    "refresh": "your_refresh_token"
}
```
- **Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Submissions

### 1. List All Submissions
- **URL:** `/api/submissions`
- **Method:** `GET`
- **Description:** Retrieve all user submissions
- **Authentication:** Required
- **Use**: By judges
- **Todo**: Make it domain specific to the judge, the shape itself does not change, backend is updated
- **Response:**
```json
{
    "submissions": [
        {
            "id": 1,
            "player_name": "username",
            "submitted_at": "2025-01-20T10:00:00Z",
            "status": "pending",
            "score": null,
            "feedback": null,
            "files": [
                {
                    "id": 1,
                    "file": "submissions/username_2025-01-20_solution.py",
                    "uploaded_at": "2025-01-20T10:00:00Z"
                }
            ],
            "question": {
                "question_id": 1,
                "domain": "Algorithms",
                "problem_title": "Sample Problem",
                "difficulty_level": "Medium"
            },
            "special_notes": "Solution notes here"
        }
    ]
}
```

### 2. Judge Submission
- **URL:** `/api/submissions/<submission_id>/judge/`
- **Method:** `POST`
- **Description:** Submit judgment for a submission
- **Authentication:** Required
- **Request Body:**
```json
{
    "score": 95.5,
    "feedback": "Great solution!"
}
```
- **Response:**
```json
{
    "status": "approved",
    "score": 95.5,
    "feedback": "Great solution!"
}
```

### 3. Submit Solution
- **URL:** `/player/solutions/`
- **Method:** `POST`
- **Description:** Submit a solution for a problem
- **Authentication:** Required
- **TODO:** Make the system separate between the individual type of file, atm everything is in the same uploads directory keep everything separate. Current plan: Domain -> Submission -> Type
- **Request Body (multipart/form-data):**
```
problemId: 1
description: "Solution description"
file1: [file]
file2: [file]
...

```
- **Response:**
```json
{
    "message": "Solution submitted successfully!",
    "submission_id": 1,
    "files": [
        {
            "filename": "username_2025-01-20_solution.py",
            "file_url": "/media/submissions/username_2025-01-20_solution.py"
        }
    ]
}
```

### 4. Download Submission File
- **URL:** `/api/download/submissions/<file_name>/`
- **Method:** `GET`
- **Description:** Download a submitted file
- **Authentication:** Required
- **Response:** Binary file download response with appropriate Content-Disposition header

## Error Responses

All endpoints may return the following error responses:

### Authentication Error (401)
```json
{
    "error": "Invalid or expired token"
}
```

### Bad Request Error (400)
```json
{
    "error": "Problem ID is required"
}
```

### Server Error (500)
```json
{
    "error": "Failed to save submission"
}
```

### Not Found Error (404)
```json
{
    "error": "The file example.py does not exist"
}
```

## Data Models

### Question
```json
{
    "question_id": 1,
    "domain": "string",
    "problem_title": "string",
    "difficulty_level": "Easy|Medium|Hard"
}
```

### UserSubmission
```json
{
    "id": 1,
    "player_name": "string",
    "submitted_at": "datetime",
    "status": "pending|approved|rejected",
    "score": "number|null",
    "feedback": "string|null",
    "files": [
        {
            "id": 1,
            "file": "string",
            "uploaded_at": "datetime"
        }
    ],
    "question": {
        "question_id": 1,
        "domain": "string",
        "problem_title": "string",
        "difficulty_level": "string"
    },
    "special_notes": "string"
}
```