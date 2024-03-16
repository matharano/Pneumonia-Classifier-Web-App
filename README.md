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

### Backend

1. Clone the repo
   ```sh
   git clone git@github.com:matharano/deeplify-coding-task.git
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```

### Frontend

No action required.

## Usage

### Backend

1. Run the server
   ```sh
   uvicorn backend.app:app --host 127.0.0.1 --port 8000
   ```

Documentation can be found at http://127.0.0.1:8000/docs

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