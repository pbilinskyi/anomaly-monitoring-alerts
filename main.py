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

    check_test_example = QueryEmptyChecker(
        sql_query='SELECT * FROM countries limit 3',
        alert_message_template=':error-alert: *Anomaly detected*'
                               '\nDetails:\n```{query_result}```'
    )

    check_test_example.run_check()

    logging.info('======== END ======== ')


if __name__ == '__main__':
    main()
