#!/bin/bash

cd src/frontend
export REACT_APP_API_PORT=7775
export PORT=3007
nohup npm start &
cd ../..

python3 -m src.main -i 127.0.0.3 -kp 8003 -mp 9003 -ap $REACT_APP_API_PORT -n 127.0.0.1 8001