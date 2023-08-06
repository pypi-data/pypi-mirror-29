#!/usr/bin/env python
# -*- coding: utf-8 -*-
import OpenSSL


fp = open('1.crl', 'r')


crl = "".join(fp.readlines())


crl_object = OpenSSL.crypto.load_crl(OpenSSL.crypto.FILETYPE_ASN1, crl)

revoked_objects = crl_object.get_revoked()

for rvk in revoked_objects:
    print rvk.get_serial()