# Anomaly Monitoring

This project is a simple anomaly monitoring system that detects anomalies in transactions data and notifies the user.

## Getting Started

First, clone the repository and install the requirements:

```bash
git clone
cd anomaly-monitoring
pip install -r requirements.txt
```

Second, make sure you have these data files available:
```bash
data/countries.csv
data/orders.csv
data/transactions.csv
data/test_aggregate_data.csv
```

Then, run the following command to initialize demo database with data:

```bash
python init_db.py
```

Finally, run the following command to perform anomaly detection and send notifications:

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
│   ├── database_io.py
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

The `anomaly_monitoring` directory contains the main logic of the project. The `db.py` file contains the functions to interact with database, and the `utils.py` file contains useful simple functions, used in many other scripts. 


The `data` directory contains the demo data of transactions and orders activity - both raw .csv files and local database file.

The `logs` directory contains the log file, where all the logs are written.


The `tests` directory contains the tests for the project. Tests help to ensure that the project works as expected.

Finally, the root directory. The `init_db.py` file contains the code for initializing the database with demo data. The `main.py` file contains the code for launching the whole process of performing anomaly detection and sending notifications. The `requirements.in` file contains the _primary_ project dependencies. The `requirements.txt` file contains all project dependencies (primary and sub-dependencies) with pinned versions.