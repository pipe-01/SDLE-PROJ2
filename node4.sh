#!/bin/bash

cd src/frontend
export REACT_APP_API_PORT=7773
export PORT=3009
nohup npm start &
cd ../..

python3 -m src.main -i 127.0.0.5 -kp 8005 -mp 9005 -ap $REACT_APP_API_PORT -n 127.0.0.1 8001