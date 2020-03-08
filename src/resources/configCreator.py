#!/usr/bin/env python

import sys
import argparse
import os
import jinja2
from pathlib import Path

ACTUAL_FILE_PATH = os.path.abspath(os.path.dirname(__file__))


def create_config(outputPath, **kwargs):
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=ACTUAL_FILE_PATH))
    template = template_env.get_template("config.toml.jinja")
    output_text = template.render(kwargs)
    Path(os.path.abspath(outputPath)).mkdir(parents=True, exist_ok=True)
    config_path = os.path.abspath(os.path.join(outputPath, "config.toml"))
    f = open(config_path, "w")
    f.write(output_text)
    f.close()
    print("Saved file to {}".format(config_path))


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--outputPath", dest="outputPath", required=True)
    parser.add_argument("--level", dest="logging_level")
    parser.add_argument("--host", dest="mysql_host")
    parser.add_argument("--user", dest="mysql_user")
    parser.add_argument("--password", dest="mysql_password")
    parser.add_argument("--db", dest="mysql_db")

    args = vars(parser.parse_args())
    configs = {'_mysql_conf': {}, '_logging_conf': {}}

    for key, value in args.items():
        if value is not None:
            if "logging_" in key:
                configs["_logging_conf"][key.replace("logging_", "")] = value
            if "mysql_" in key:
                configs["_mysql_conf"][key.replace("mysql_", "")] = value

    create_config(outputPath=args['outputPath'], **configs)


if __name__ == "__main__":
    main(sys.argv[1:])