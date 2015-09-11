#!/usr/bin/env python

""" 
check_certs.py

A tiny script to check which certificates in a given directory will expire soon.
"""

from pyasn1_modules import pem, rfc2459
from pyasn1.codec.der import decoder
from pyasn1_modules.rfc2459 import id_at_commonName as COMMON_NAME
from pyasn1_modules.rfc2459 import DirectoryString

import glob
import sys
import datetime

# Amount of days to warn ahead.
delta_ahead = datetime.timedelta(days=7)

def read_certificate(pemfile):
    """Reads an X509-encoded certificate file."""

    substrate = pem.readPemFromFile(open(pemfile))
    return decoder.decode(substrate, asn1Spec=rfc2459.Certificate())[0]

def expire_date(certificate):
    """Obtains the expiration date for the certificate as a datetime."""

    utctime_expire = certificate.getComponentByName('tbsCertificate').  \
                                 getComponentByName('validity').        \
                                 getComponentByName('notAfter').        \
                                 getComponentByName('utcTime')

    return datetime.datetime.strptime(str(utctime_expire), '%y%m%d%H%M%SZ')

def subject_common_name(certificate):
    """Obtains the common name for the certificate subject as a string."""

    subject = certificate.getComponentByName('tbsCertificate'). \
                          getComponentByName('subject')

    for rdnss in subject:
        for rdns in rdnss:
            for name in rdns:
                # Search through values until for the OID of a common name.
                oid = name.getComponentByName('type')
                value = name.getComponentByName('value')

                if oid != COMMON_NAME:
                    continue

                value = decoder.decode(value, asn1Spec=DirectoryString())[0]
                return bytes(value.getComponent()).decode('utf-8')

def expiring_certs(directory):
    """
    Returns a list of tuples (common name, time left) sorted by time left
    for all certificates in the given directory.
    """

    expirations = []
    for certificate_file in glob.glob("%s/*.pem" % directory):
        certificate = read_certificate(certificate_file)

        name = subject_common_name(certificate)
        expiration = expire_date(certificate)
        time_left = expiration - datetime.datetime.now()

        if(time_left < delta_ahead):
            expirations.append((name, time_left))

    return sorted(expirations, key=lambda x: x[1])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s <certificate directory>" % sys.argv[0])
        sys.exit(1)

    expirations = expiring_certs(sys.argv[1])
    if expirations:
        print("The following certificates will expire soon:")
        for name, left in expirations:
            print(" * %s: %s days, %s hours" % (name, left.days, int(left.seconds/3600)))
