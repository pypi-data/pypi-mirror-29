#!/usr/bin/env python3
# coding: utf-8
"""
Query VCFs by phenotype, position and other parameters.
"""
import argparse
from aws_requests_auth.aws_auth import AWSRequestsAuth
import boto3
from filecache import filecache
import json
import python_jsonschema_objects as pjs
import requests
import sys

API_HOST = "nnaiyf9q24.execute-api.ap-southeast-2.amazonaws.com"
API_ROOT = "https://" + API_HOST + "/test"
API_RESOURCE_QUERY = API_ROOT + "/vcfquery"

session = boto3.Session()
credentials = session.get_credentials()
auth = AWSRequestsAuth(aws_access_key=credentials.access_key,
                       aws_secret_access_key=credentials.secret_key,
                       aws_host=API_HOST,
                       aws_region=session.region_name,
                       aws_service='execute-api')


def main():
    """
    Do the work.
    """
    schema = request_jsonschema()
    Query = schema_class(schema)
    parser, names = build_parser(Query)

    # simple Python type errors in the arguments will be raised here
    args = parser.parse_args()

    if args.subcommand is None:
        print("no command chosen", file=sys.stderr)
        sys.exit(0)
    elif args.subcommand == "meta":
        if args.schema:
            print(schema)
        if args.apiurl:
            print(API_RESOURCE_QUERY)
        sys.exit(0)

    # perform additional validation as specified by the schema
    json_validation_errors = []
    q = Query()
    for propname, optname, destname in names:
        cli_value = getattr(args, destname)
        if cli_value is not None:  # could be 0 or ''
            try:
                setattr(q, propname, cli_value)
            except Exception as e:
                json_validation_errors.append(optname + ": " + str(e))
    if json_validation_errors:
        print('\n'.join(json_validation_errors), file=sys.stderr)
        sys.exit(1)

    # valid data here
    data = q.for_json()
    response = requests.post(API_RESOURCE_QUERY, auth=auth, json=data)
    print(response.text)


def build_parser(klass):
    """
    Create the CLI interace inferred from the class defined in the schema.
    Returns (parser, names) where "names" is a list of 3-tuples:
    (<class property name>, <option display name> <option dest name>)
    """
    # map from property names to human-friendly CLI option names
    cliopt = {p: p.replace("_", "-") for p in klass.__prop_names__}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.epilog = parser.prog + \
        " {meta,query} -h, --help for help on subcommands"
    subparsers = parser.add_subparsers(dest='subcommand')
    meta = subparsers.add_parser('meta')
    group = meta.add_mutually_exclusive_group()
    group.add_argument("--apiurl", action='store_true',
                       help='show the URL used for API requests')
    group.add_argument("--schema", action='store_true',
                       help='show the JSON schema used for API requests')
    query = subparsers.add_parser('query', epilog=(
        "The (gte|lte) arguments specify inclusive bounds: " +
        "'gte' = 'greater than or equal to' (lower bound) and " +
        "'lte' = 'lower than or equal to' (upper bound)."))
    names = []
    for propname in klass.__prop_names__:
        info = klass.__propinfo__[propname]
        typ = info['type']
        # string name of simple JSON type
        if isinstance(typ, str):
            arg_type = basicjson2py(typ)
            helpstr = arg_type.__name__
        # it's a more complex defined type
        else:
            info = typ.propinfo('__literal__')
            arg_type = basicjson2py(info['type'])
            helpstr = str(info)
        required = propname in klass.__required__
        optname = "--" + cliopt[propname]
        destname = query.add_argument(
            optname,
            type=arg_type,
            help=helpstr,
            required=required).dest
        names.append((propname, optname, destname))
    return (parser, names)


def basicjson2py(typename):
    """
    Return the Python builtin type for basic JSON types.
    'array' and 'object' are not supported.
    """
    try:
        return {
            'boolean': bool,
            'integer': int,
            'number': float,
            'null': None,
            'string': str,
        }[typename]
    except KeyError as e:
        raise ValueError("Unsupported JSON type: '" + typename + "'")


@filecache(24 * 60 * 60)
def request_jsonschema():
    """
    Return the JSON schema for API requests. The schema is cached locally.
    """
    # API is configured to return the schema when an empty body is POST'ed
    # to the /vcfquery resource
    return requests.post(API_RESOURCE_QUERY, auth=auth, json={}).json()


def schema_class(schema):
    """
    Return the top python_jsonschema_objects class inferred from the schema
    """
    builder = pjs.ObjectBuilder(schema)
    ns = builder.build_classes()
    return ns[schema['title'].lower().capitalize()]


if __name__ == '__main__':
    main()
