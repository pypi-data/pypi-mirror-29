#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
for line in sys.stdin:
    parts = line.split()
    if int(parts[6]) in (1, 5, 7, 8, 10):

        pubkeys = ''.join(parts[7:]).replace(' ', '')
        pubkey = pubkeys.decode('base64')
        expoffset = 1
        explen = ord(pubkey[0])
        if not explen:
            explen = ord(pubkey[1]) * 256 + ord(pubkey[2])
            expoffset = 4
        exponent = pubkey[expoffset:expoffset+explen]
        modulus = pubkey[expoffset+explen:]
        #print("exponent:", exponent.encode('base64'))
        #print("modulus:", modulus.encode('base64'))
        print modulus.encode('base64').replace('\n', ''), pubkeys
