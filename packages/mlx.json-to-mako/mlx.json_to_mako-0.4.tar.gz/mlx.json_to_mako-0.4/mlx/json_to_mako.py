#! /usr/bin/env python3

'''
Convert any json input to any output format defined by mako template
'''

from argparse import ArgumentParser
from json import loads
from mako.template import Template
import os
import re
import sys

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "__version__.py")).read())


def to_identifier(name):
    '''
    Convert string to identifier

    Removing invalid chars and leading non-letter characters

    Args:
        name (str): input name
    Returns
        str: Valid identifier based on input name
    '''
    return re.sub('\W|^(?=\d)', '', name)


class InputDatabase(object):
    '''
    Store data from input database

    The data is contained in self.data.
    Some meta information is stored in self.source (path to source json file)
    and self.name (derived from path to source json file)
    '''
    def __init__(self, json):
        '''

        Args:
            json: Name of the json file
        '''
        self.data = None
        self.source = json
        self.name = to_identifier(os.path.splitext(os.path.basename(self.source))[0])
        with open(json, 'r') as finput:
            self.data = loads(finput.read())


def json_to_mako_wrapper(args):
    '''
    Main entry for json_to_mako
    '''
    PARSER = ArgumentParser(description='Convert any JSON data base to a mako-templated output.')
    PARSER.add_argument("-v", "--version", action="version", version="%(prog)s " + __version__)
    PARSER.add_argument('-i', '--input', action='append',
                        required=True,
                        help='Input file(s): JSON file(s).')
    PARSER.add_argument('-o', '--output', action='store',
                        required=True,
                        help='Output file.')
    PARSER.add_argument('-t', '--template', action='store',
                        required=True,
                        help='Custom MAKO template file for which to render the given JSON input.')
    ARGS = PARSER.parse_args(args)

    database = []
    for inputfile in ARGS.input:
        db = InputDatabase(inputfile)
        database.append(db)
    tmpl = Template(filename=ARGS.template)
    rendered = tmpl.render(db=database)
    with open(ARGS.output, 'w') as out:
        out.write(rendered)


def main():
    sys.exit(json_to_mako_wrapper(sys.argv[1:]))


if __name__ == '__main__':
    main()
