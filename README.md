# Anomaly Monitoring

This project is a simple anomaly monitoring system that detects anomalies in transactions data and notifies the user.

## Getting Started

### Prerequisites

You have to provide the credentials in `.env` file:
```bash
SLACK_ALERT_BOT_TOKEN=
SLACK_ALERT_CHANNEL_ID=
PATH_TO_GOOGLE_JSON_CREDENTIALS=
GOOGLE_SHEET_KEY=
```

### Installing

First, clone the repository and install the requirements:

```bash
git clone https://github.com/pbilinskyi/anomaly-monitoring-alerts.git
cd anomaly-monitoring-alerts
pip install -r requirements.txt
```

Then, run the following command to initialize demo database with data:

```bash
python init_db.py
```

### Running

Run the following command to perform anomaly detection and send notifications:

```bash
python main.py
```

## Project Structure

The project is structured as follows:

```
anomaly-monitoring
├── README.md
├── anomaly_monitoring
│   ├── __init__.py
│   ├── checks.py
│   ├── database_id.py
│   ├── google_sheets_io.py
│   ├── slack_io.py
│   └── utils.py
├── data
│   ├── ...
└── tests
    ├── __init__.py
    └── test_all.py
└── logs
    └── log.txt
├── init_db.py
├── main.py
├── requirements.in
├── requirements.txt
└── README.md
└── .gitignore

```

The `anomaly_monitoring` directory contains the main logic of the project. 
- File `checks.py` defines the classes for anomaly checks with methods to run checks.
- File `database_io.py` contains the functions to interact with database (e.g. execute SQL queries).
- File `google_sheets_io.py` contains the functions to interact with Google Sheets.
- File `slack_io.py` contains the functions to interact with Slack (e.g. post message to channel).
- File `utils.py` contains useful simple functions, used in many other scripts. 

The `data` directory contains the demo data of transactions and orders activity - both raw .csv files and local database file.

The `logs` directory contains the log file, where all the logs are written.

The `tests` directory contains the tests for the project. Tests help to ensure that the project works as expected.

Finally, the root directory. 
- File `init_db.py` contains the code for initializing the database with demo data. 
- File `main.py` contains the code for launching the whole process of performing anomaly detection and sending notifications.
- File `requirements.in` contains the _primary_ project dependencies. The `requirements.txt` file contains all project dependencies (primary and sub-dependencies) with pinned versions.
