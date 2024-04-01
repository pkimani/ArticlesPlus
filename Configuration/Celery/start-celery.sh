#!/bin/bash

# Enter Python virtual environment
source /home/pkimani/venv/bin/activate

# Navigate to the Django project directory
cd /home/pkimani/getting-started-app/djrssproj/

# Start the Celery worker
celery -A djrssproj worker --concurrency=1000 --pool=threads --loglevel=INFO