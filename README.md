# Best Hackathon Team Ever

### Repo Setup
* Spin up virtual env `python -m venv .venv`
* Install requirements `python -m pip install -r requirements.txt`
* Put anthropic api key in environment vars, run `export ANTHROPIC_API_KEY=xxx`

### Spin up Elasticsearch
* run `docker-compose up -d`

### Populate elasticsearch
* get zendesk data from snowflake in csv format `ZENDESK_TICKET_ID, SUBJECT, COMMENTS`
* This should be called `snowflake_data.csv` under `files/`
* TODO: get sop data from confluence
* File name and structure tbd
* Uncomment `csv_file_path = 'files/snowflake_data.csv'` and `embed_data(csv_file_path)` in `controller.py`
* run `python controller.py` with `embed_sop` `embed_zendesk` or both.  e.g. `python controller.py index_zendesk index_sop`

### Searching with already populated elasticsearch
* run `python controller.py` with no command line args

### Clearing an index
* run 'python clear_index.py INDEX_NAME` to clear an elasticsearch index for repopulating