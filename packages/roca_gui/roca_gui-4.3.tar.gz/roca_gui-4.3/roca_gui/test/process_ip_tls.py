#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import logging
import coloredlogs
LOG_FORMAT = '%(asctime)s [%(process)d] %(levelname)s %(message)s'
logger = logging.getLogger(__name__)
coloredlogs.install(filename='logger.log', level=logging.DEBUG, fmt=LOG_FORMAT)
from roca_gui.detector import Detector
from ssl import get_server_certificate
csv.field_size_limit(1000000000)
r = csv.reader(open('c62dvw0katttejln-443-https-rsa_export-full_ipv4-20180308T033837-zmap-results.csv', 'rb'))
detect = Detector()
port = 443
ret = []
i=0
for host in r:
    i = i +1
    if i%100 == 0:
        print(i)
    if host[0] != '':
        try:
            pem_cert = get_server_certificate((host[0], port))
        except Exception as e0:
            logger.error('Error getting server certificate from %s:%s: %s' %
                         (host, port, e0))
            continue
        result = detect.process_pem_certificate(pem_cert, host, 0)
        if result is not None:
            ret.extend(result)
if len(ret) > 0:
    logger.warning("Warning", "Subject to ROCA vulnerability, insecure!")
    with open('result_tls.txt', 'w') as f:
        """
        save ip address to result.txt
        """
        for i, dic in enumerate(ret):
            f.write('%s\n' % (dic['fname']))