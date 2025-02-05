# Best Hackathon Team Ever

### Repo Setup
* Spin up virtual env `python -m venv .venv`
* Install requirements `python -m pip install -r requirements.txt`
* Put anthropic api key in environment vars, run `export ANTHROPIC_API_KEY=xxx`

### Spin up Elasticsearch
* run `docker-compose up -d`

### Populate elasticsearch
* get data from snowflake in csv format `ZENDESK_TICKET_ID, SUBJECT, COMMENTS`
* This should be called `snowflake_data.csv` under `files/`
* Uncomment `csv_file_path = 'files/snowflake_data.csv'` and `embed_data(csv_file_path)` in `controller.py`
* run `python controller.py`

### Searching with already populated elasticsearch
* Ensure `csv_file_path = 'files/snowflake_data.csv'` and `embed_data(csv_file_path)` in `controller.py` are commented out
* run `python controller.py`