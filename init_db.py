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

CREATE TABLE countries (
    country VARCHAR(3),
    country_rn SMALLINT
);

CREATE TABLE transactions (
    id BIGINT,
    created_date TIMESTAMP,
    transaction_type VARCHAR(6),
    merchant_id SMALLINT,
    transaction_status VARCHAR(7)
);

CREATE TABLE test_aggregate_data (
    created_day DATE,
    channel_id TINYINT,
    order_type VARCHAR(5),
    payment_source VARCHAR(100),
    merchant_token_type VARCHAR(20),
    is_secured BOOLEAN,
    bin_amount_usd VARCHAR(20),
    status VARCHAR(20),
    error_code VARCHAR(4),
    error_message VARCHAR,
    bank_issuer INT,
    card_brand VARCHAR(100),
    card_type VARCHAR(50),
    card_country SMALLINT,
    ip_country SMALLINT,
    invoice_number SMALLINT,
    retry_number VARCHAR(15),
    count_orders SMALLINT,
    count_emails SMALLINT
);
""")
logging.info('SUCCESS: tables were successfully created.')


# UPLOAD the data in to database tables
logging.info('STARTED: Uploading data to database')

date_format = r'%Y-%m-%d %H:%M:%S.%f'
timestamp_format = r'%m/%d/%y %-H:%M'

table_names = ('countries', 'orders', 'transactions', 'test_aggregate_data')
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
                           timestampformat='{timestamp_format}',
                           header=true);
    """)
    logging.info("DONE")

# close connection
con.close()
