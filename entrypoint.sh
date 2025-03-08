#!/bin/bash

flask db init
flask db migrate -m "Schema"
flask db upgrade

# Run the application using python run.py
python run.py