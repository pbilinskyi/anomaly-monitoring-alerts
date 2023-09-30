import os
import logging

from anomaly_monitoring.checks import QueryEmptyChecker
from anomaly_monitoring.database_io import read_sql_query
from anomaly_monitoring.google_sheets_io import update_google_sheets_table


def main():
    # initialize logging
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s',
                        filename=os.path.join('logs', 'log.txt'),
                        encoding='utf-8',
                        level=logging.DEBUG)

    logging.info('======== START ======== ')

    # 1. Perform anomaly detection & sending alert to Slack

    query_find_anomalies = """
    with order_history as (
            select order_id,
                   max(created_date)
                       filter (where transaction_type = 'auth')              as auth_date,
                   min(created_date)
                       filter (where transaction_type in ('settle', 'void')) as finish_date
            from transactions
            where transaction_status = 'success'
            group by order_id)
    select orders.merchant_id as "Merchant ID",
           count(order_id)    as "Anomaly Orders"
    from order_history
         left join orders
         on order_history.order_id = orders.id
    where auth_date is not null
      and (finish_date is null                               -- only anomaly orders
           or (finish_date - auth_date) > interval '7 days') -- only anomaly orders
    group by orders.merchant_id
    order by "Anomaly Orders" desc;
    """

    check_test_example = QueryEmptyChecker(
        sql_query=query_find_anomalies,
        alert_message_template=':error-alert: *Anomaly detected*: '
                               'orders without settle/void during 7 days.\n'
                               '\nDetails:\n```{query_result}```'
    )

    check_test_example.run_check()

    # 2. Update google sheet

    query = """
    with order_history as (
            select order_id,
                max(created_date) filter (where transaction_type = 'auth')              as auth_date,
                min(created_date) filter (where transaction_type in ('settle', 'void')) as finish_date
            from transactions
            where transaction_status = 'success'
            group by order_id)
    select order_id as "Order ID"
    from order_history
    where auth_date is not null
    and (finish_date is null                               -- only anomaly orders
        or (finish_date - auth_date) > interval '7 days') -- only anomaly orders
    order by "Order ID";
    """
    df_to_append = read_sql_query(query)
    update_google_sheets_table(df_to_append,
                               sheet_name='Anomaly: unfinished orders')

    logging.info('======== END ======== ')


if __name__ == '__main__':
    main()
