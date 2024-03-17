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

1. Clone the repository to your local machine.
    ```sh
    git clone git@github.com:matharano/deeplify-coding-task.git
    ```
2. Based on the `.env.template` file, create a `.env` file in the root directory and update the values if necessary.
    ```sh
    cp .env.template .env
    ```

### Backend

1. Enter the backend directory
    ```sh
    cd backend
    ```
2. Create a virtual environment
    ```sh
    python -m venv venv
    ```
3. Activate the virtual environment
    ```sh
    source venv/bin/activate
    ```
4. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
5. Download and extract the weights in `backend/weights` directory from the following link:
    https://drive.google.com/drive/folders/1dikJzuwqiObUdaXWm0AJ80rR5sYDK3d5?usp=sharing

### Frontend

Install dependencies
```sh
cd frontend
npm install
```

## Usage

1. Update the .env file if necessary
2. Navigate to the root directory
    ```sh
    cd deeplify-coding-task
    ```
3. Run backend and frontend
    ```sh
    source entrypoint.sh
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