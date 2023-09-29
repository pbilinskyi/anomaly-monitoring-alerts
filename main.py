import os
import logging


def main():
    # initialize logging
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s',
                        filename=os.path.join('logs', 'log.txt'),
                        encoding='utf-8',
                        level=logging.DEBUG)

    logging.info('======== START ======== ')
    # perform anomaly detection & sending alerts
    # ...
    logging.info('======== END ======== ')


if __name__ == '__main__':
    main()
