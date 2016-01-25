#!/bin/bash
source env/bin/activate
pip install -r requeriments.txt
cd NeuralOCR
python manage.py runserver 127.0.0.1:8080