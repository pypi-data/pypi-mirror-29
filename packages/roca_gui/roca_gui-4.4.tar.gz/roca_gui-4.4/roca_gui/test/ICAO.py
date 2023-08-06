#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from ldif import LDIFParser,LDIFWriter

SKIP_DN = []

class MyLDIF(LDIFParser):

    init_num = 0

    def __init__(self,input,output):
        LDIFParser.__init__(self,input)
        self.writer = LDIFWriter(output)

    def handle(self,dn,entry):
        if entry.has_key("certificateRevocationList;binary"):
            self.init_num = self.init_num +1
            fname = str(self.init_num) + '.crl'
            print(dn)
            #print(entry["userCertificate;binary"])
            with open(fname,'w') as f:
                f.write(entry["certificateRevocationList;binary"][0])
        if dn not in SKIP_DN:
            return
        self.writer.unparse(dn,entry)

parser = MyLDIF(open("icaopkd-001-dsccrl-002609.ldif", 'rb'), sys.stdout)
parser.parse()