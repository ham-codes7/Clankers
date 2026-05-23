# TestGen AI

This is an AI Test Case Generation tool project.

## Setup Instructions (for beginners)

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd testgen-ai
    ```

2.  **Set up the backend:**
    a.  Navigate to the backend directory:
        ```bash
        cd backend
        ```
    b.  Create a virtual environment (recommended):
        ```bash
        python3 -m venv venv
        ```
    c.  Activate the virtual environment:
        -   On macOS/Linux:
            ```bash
            source venv/bin/activate
            ```
        -   On Windows:
            ```bash
            .\venv\Scripts\activate
            ```
    d.  Install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```
    e.  Create a `.env` file:
        Copy the `.env.example` file to `.env`:
        ```bash
        cp .env.example .env
        ```
    f.  Open the newly created `.env` file and replace `your-key-here` with your actual Groq API key:
        ```
        GROQ_API_KEY=your-key-here
        ```
    g.  Run the backend server:
        ```bash
        uvicorn main:app --reload
        ```
        The backend server will typically run on `http://127.0.0.1:8000`.

3.  **Frontend (To be implemented):**
    Instructions for the frontend will be added here once it's developed.
