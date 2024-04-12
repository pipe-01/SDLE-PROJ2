#!/bin/bash

cd src/frontend
export REACT_APP_API_PORT=7774
export PORT=3008
nohup npm start &
cd ../..

python3 -m src.main -i 127.0.0.4 -kp 8004 -mp 9004 -ap $REACT_APP_API_PORT -n 127.0.0.1 8001