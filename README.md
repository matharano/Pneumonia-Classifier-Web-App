# deeplify-coding-task
Coding task for technical assessment at Deeplify

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#testing">Testing</a></li>
  </ol>
</details>

## Installation

To start, clone the repository to your local machine.
```sh
git clone git@github.com:matharano/deeplify-coding-task.git
```

### Backend

Install dependencies
```sh
pip install -r requirements.txt
```

### Frontend

Install dependencies
```sh
cd frontend
npm install
```

## Usage

### Backend

1. Run the server
   ```sh
   uvicorn backend.app:app --host 127.0.0.1 --port 8000
   ```

Documentation can be found at http://127.0.0.1:8000/docs

### Frontend

1. Navigate to the frontend directory
   ```sh
   cd frontend
   ```
2. Run the server
   ```sh
   npm start
   ```

## Testing

Execute the following command to run the tests:

1. Enter the backend directory
   ```sh
   cd backend
   ```
2. Run the tests
    ```sh
    pytest
    ```