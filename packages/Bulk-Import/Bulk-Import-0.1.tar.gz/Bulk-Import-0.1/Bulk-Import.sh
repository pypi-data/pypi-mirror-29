#!/bin/bash
BULK_SCRIPT = "Bulk-Import.py"
AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
INPUT_BUCKET = "talendhirocapush"
INPUT_FILE = "MachineBulk.json"
AWS_REGION = 'ca-central-1'
MULE_URL = "https://ca-connect.hiroca.compucom.com:8184/connectit/api"
MULE_USER = "mule"
MULE_PASSWORD = "mule123"
exec python "${BULK_SCRIPT}" ${AWS_ACCESS_KEY_ID} ${AWS_SECRET_ACCESS_KEY} ${INPUT_BUCKET} ${INPUT_FILE} ${AWS_REGION} ${MULE_URL} ${MULE_USER} ${MULE_PASSWORD}