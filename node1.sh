#!/bin/bash

cd src/frontend
export REACT_APP_API_PORT=7776
export PORT=3006
nohup npm start &
cd ../..

python3 -m src.main -i 127.0.0.2 -kp 8002 -mp 9002 -ap $REACT_APP_API_PORT -n 127.0.0.1 8001
