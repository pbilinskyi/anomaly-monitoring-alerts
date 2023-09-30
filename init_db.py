import os
import logging

from anomaly_monitoring.database_io import (
    create_database,
    open_conn
)


logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s',
                    level=logging.DEBUG)

# INITIALIZE empty database, which would be used as a Data Warehouse
logging.info('Initializing empty database.')
create_database()
con = open_conn()

# CREATE tables to store data
logging.info('Started: Creating empty tables')
con.execute("""
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS test_aggregate_data;

CREATE TABLE orders (
    id BIGINT,
    created_date TIMESTAMP,
    merchant_id SMALLINT
);

CREATE TABLE transactions (
    id BIGINT,
    created_date TIMESTAMP,
    transaction_type VARCHAR(6),
    order_id BIGINT,
    transaction_status VARCHAR(7)
);
""")
logging.info('SUCCESS: tables were successfully created.')


# UPLOAD the data in to database tables
logging.info('STARTED: Uploading data to database')

table_names = ('orders', 'transactions')
for table_name in table_names:
    logging.info("STARTED: Uploading data to the table '%s'", table_name)
    csv_filename = os.path.join('data', f'{table_name}.csv')

    # check if file exists
    if not os.path.exists(csv_filename):
        raise FileNotFoundError(f"ERROR: File '{csv_filename}' not found.")

    con.execute(f"""
        INSERT INTO {table_name}
        SELECT *
        FROM read_csv_auto('{csv_filename}',
                           timestampformat='%m/%d/%y %-H:%M',
                           header=true);
    """)
    logging.info("DONE")


# add some syntetic cases of anomalies
# 1. Transaction was finished after 6 days 23 hours 59 minutes 59 seconds of authorization.

con.execute("""
    insert into transactions
           (id, created_date, transaction_type, order_id, transaction_status)
    values

    -- Case 1: settle after 6 days 23 hours 59 minutes 59 seconds, [NORMAL]
    (8, timestamp '2023-05-15 10:02:00', 'auth', 5, 'success'),
    (9, timestamp '2023-05-22 10:01:59', 'settle', 5, 'success'),

    -- Case 2: settle after 7 days 1 second, [ANOMALY]
    (10, timestamp '2023-05-16 10:02:00', 'auth', 6, 'success'),
    (11, timestamp '2023-05-23 10:02:01', 'settle', 6, 'success'),  

    -- Case 3: no settle, only auth, [ANOMALY]
    (12, timestamp '2023-05-17 19:36:00', 'auth', 7, 'success'),

    -- Case 4: void after 30 days, [ANOMALY]
    (13, timestamp '2023-05-17 19:36:00', 'auth', 8, 'success'),
    (14, timestamp '2023-06-16 19:36:00', 'void', 8, 'success'),

    -- Case 5: failed settle after 5 days, [ANOMALY]
    (15, timestamp '2023-05-17 19:36:00', 'auth', 9, 'success'),
    (16, timestamp '2023-05-22 19:36:00', 'settle', 9, 'fail'),

    -- Case 6: failed settle after 5 days,
    --         then successful settle after 8 days, [ANOMALY]
    (17, timestamp '2023-05-17 19:36:00', 'auth', 10, 'success'),
    (18, timestamp '2023-05-22 19:36:00', 'settle', 10, 'fail'),
    (19, timestamp '2023-05-25 19:36:00', 'settle', 10, 'success');

    insert into orders
              (id, created_date, merchant_id)
    values
            (5, timestamp '2023-05-15 10:02:00', 1),
            (6, timestamp '2023-05-16 10:02:00', 1),
            (7, timestamp '2023-05-17 19:36:00', 2),
            (8, timestamp '2023-05-17 19:36:00', 4),
            (9, timestamp '2023-05-17 19:36:00', 4),
            (10, timestamp '2023-05-17 19:36:00', 4);
""")

# close connection
con.close()
