# !/bin/bash

# Enter virtual environment
source backend/venv/bin/activate

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Start frontend
HOST=$FRONTEND_IP PORT=$FRONTEND_PORT REACT_APP_BACKEND_IP=$BACKEND_IP REACT_APP_BACKEND_PORT=$BACKEND_PORT npm start --prefix frontend 2>&1 &

# Start backend
FRONTEND_IP=$FRONTEND_IP FRONTEND_PORT=$FRONTEND_PORT uvicorn backend.app:app --host $BACKEND_IP --port $BACKEND_PORT