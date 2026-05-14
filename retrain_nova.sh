#!/bin/bash
# Weekly retraining script for Nova
# Run this with cron: 0 23 * * 5 /path/to/retrain_nova.sh

cd /path/to/customer_agent_pro
source .venv/bin/activate
python manage.py retrain_nova