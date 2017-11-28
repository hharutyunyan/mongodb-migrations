import argparse
import os
import logging
from configparser import ConfigParser


class Configuration(object):
    logger = logging.getLogger("config")
    config_file = os.getenv('MONGODB_MIGRATIONS_CONFIG', 'config.ini')
    mongo_host = '127.0.0.1'
    mongo_port = '27017'
    mongo_database = None
    mongo_migrations_path = 'migrations'

    def __init__(self):
        self._from_ini()
        self._from_console()

        if not self.mongo_database:
            raise Exception("No database name is provided")

    def _from_console(self):
        self.arg_parser = argparse.ArgumentParser(description="Mongodb migration parser")

        self.arg_parser.add_argument('--host', metavar='H', default=self.mongo_host,
                            help="host of MongoDB")
        self.arg_parser.add_argument('--port', type=int, metavar='p', default=self.mongo_port,
                            help="port of MongoDB")
        self.arg_parser.add_argument('--database', metavar='d',
                            help="database of MongoDB", required=(self.mongo_database==None), default=self.mongo_database)
        self.arg_parser.add_argument('--migrations', default=self.mongo_migrations_path,
                            help="directory of migration files")

        args = self.arg_parser.parse_args()

        self.mongo_host = args.host
        self.mongo_port = args.port
        self.mongo_database = args.database
        self.mongo_migrations_path = args.migrations

    def _from_ini(self):
        self.ini_parser = ConfigParser(defaults={'host': self.mongo_host, 'port': self.mongo_port, 'migrations': self.mongo_migrations_path, 'database': self.mongo_database})

        try:
            fp = open(self.config_file)
        except Exception:
            pass
        else:
            with fp:
                self.ini_parser.readfp(fp)
                if not self.ini_parser.sections():
                    raise Exception("Cannot find %s or it doesn't have sections." % self.config_file)

                self.mongo_host = self.ini_parser.get('mongo', 'host')
                self.mongo_port = self.ini_parser.getint('mongo', 'port')
                self.mongo_database = self.ini_parser.get('mongo', 'database')
                self.mongo_migrations_path = self.ini_parser.get('mongo', 'migrations')
