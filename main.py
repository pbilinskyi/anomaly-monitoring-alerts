import os
import logging

from anomaly_monitoring.checks import QueryEmptyChecker


def main():
    # initialize logging
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s',
                        filename=os.path.join('logs', 'log.txt'),
                        encoding='utf-8',
                        level=logging.DEBUG)

    logging.info('======== START ======== ')
    # perform anomaly detection & sending alerts

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
                               '\nDetails:\n```{query_result}```',
        alert_google_sheet_name='Anomaly: unfinished orders',
    )

    check_test_example.run_check()

    logging.info('======== END ======== ')


if __name__ == '__main__':
    main()
