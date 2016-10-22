"""Process npm artifacts.

The main function is exposed as a console script named `chomp` via setup.py.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import sys

import requests
from gratipay.utils import markdown


def from_npm(package):
    """Given an npm package dict, return a dict of info and a list of emails.
    """
    out= {}
    out['name'] = package['name']
    out['description'] = package['description']
    out['long_description'] = markdown.marky(package['readme'])
    out['long_description_raw'] = package['readme']
    out['long_description_type'] = 'x-text/marky-markdown'

    emails = []
    for key in ('authors', 'maintainers'):
        for person in package.get(key, []):
            if type(person) is dict:
                email = person.get('email')
                if email:
                    emails.append(email)

    return out, emails


def process_catalog(catalog):
    SQL = ''
    return SQL


def fetch_catalog():
    r = requests.get('https://registry.npmjs.com/-/all')
    r.raise_for_status()
    return r.json()


def update_database(SQL):
    pass


def parse_args(argv):
    p = argparse.ArgumentParser()
    p.add_argument( 'if_modified_since'
                  , help='a number of minutes in the past, past which we need new updates'
                   )
    return p.parse_args(argv)


def main(argv=sys.argv):
    ims = parse_args(argv[1:]).if_modified_since
    process_catalog(fetch_catalog(), ims)
