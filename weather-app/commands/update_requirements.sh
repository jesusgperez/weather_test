#!/bin/bash

pip freeze > requirements.txt
cp requirements.txt ../main-service
