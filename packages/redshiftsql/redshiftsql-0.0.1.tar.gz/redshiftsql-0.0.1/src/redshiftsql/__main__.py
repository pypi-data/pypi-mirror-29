from __future__ import print_function

import argparse
import atexit
import boto3
import os
import psycopg2
import sys
import logging

from botocore.client import Config


if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m redshiftsql"


@atexit.register
def app_exit():
    logging.getLogger().info("Terminating")


def _parse_command_line_arguments():
    argv_parser = argparse.ArgumentParser()
    argv_parser.add_argument(
        'host',
        help='The Redhshift cluster endpoint address to connect to'
    )
    argv_parser.add_argument(
        'dbname',
        help='The name of the Redshift DB to connect to'
    )
    argv_parser.add_argument(
        'user',
        help='The Redshift user to use to connect'
    )
    argv_parser.add_argument(
        '--password',
        help='The Redshift password to use to connect'
    )
    iam_group = argv_parser.add_argument_group(
        title='IAM credentials',
        description='IAM credentials for temporary Redshift credentials'
    )
    iam_group.add_argument(
        '--aws-access-key-id',
        help='The AWS IAM Access Key ID to use'
    )
    iam_group.add_argument(
        '--aws-secret-key',
        help='The AWS IAM Secret Key to use'
    )
    iam_group.add_argument(
        '--cluster-name',
        help='The Redshift cluster name (identifier)'
    )
    argv_parser.add_argument(
        '--port',
        default=5439,
        type=int,
        help='The Redshift cluster port to connect to'
    )
    argv_parser.add_argument(
        '--file',
        help='The file of commands to upload (replaces stdin)'
    )

    return argv_parser.parse_args()


def get_user_password(args):
    if not args.aws_access_key_id:
        print('Using user {} and password for direct Redshift access'.format(args.user))
        return args.user, args.password
    print('Found AWS Access Key Id {}, obtaining temporary credentials'.format(args.aws_access_key_id))
    redshift = boto3.client(
        'redshift',
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_key,
        config=Config(signature_version='s3v4')
    )
    credentials = redshift.get_cluster_credentials(
        ClusterIdentifier=args.cluster_name,
        DbName=args.dbname,
        DbUser=args.user
    )
    print('Using user {} and temporary password for Redshift access'.format(credentials['DbUser']))
    return credentials['DbUser'], credentials['DbPassword']


def execute_command(cursor, command):
    print('Executing: {}'.format(command))
    cursor.execute(command)
    print('Results:')
    for record in cursor:
        print(record)


def main():
    try:
        args = _parse_command_line_arguments()

        # set AWS logging level
        logging.getLogger('botocore').setLevel(logging.ERROR)
        logging.getLogger('boto3').setLevel(logging.ERROR)

        (user, password) = get_user_password(args)

        print('Connecting to database {} on {}:{}'.format(args.dbname, args.host, args.port))
        with psycopg2.connect(
                dbname=args.dbname,
                user=user,
                password=password,
                host=args.host,
                port=args.port
        ) as redshift_connection:
            with redshift_connection.cursor() as cursor:
                if not args.file:
                    for command in sys.stdin:
                        execute_command(cursor, command)
                else:
                    with open(args.file, 'r') as commands:
                        for command in commands:
                            execute_command(cursor, command)

    except psycopg2.OperationalError as oe:
        print('Database error:', oe.message, file=sys.stderr)
        print('')
        raise oe
    except KeyboardInterrupt:
        print("Service interrupted", file=sys.stderr)

    except Exception as e:
        print('Initialization FAILED:', e.message, file=sys.stderr)
        print('')
        raise e


if __name__ == '__main__':
    main()

