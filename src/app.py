import json
import logging
import sys
import os
import toml

from flask import Flask, request, Response
from flask_mysqldb import MySQL
from jsonschema import ValidationError

from schema_validator import validate_request

LOGGING_OPTIONS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET
}

logging.basicConfig(level=LOGGING_OPTIONS.get(os.getenv("LOGLEVEL"), "NOTSET"))
logger = logging.getLogger(__name__)
logger.info("ApiExample starting up on %s" % (str.replace(sys.version, '\n', ' ')))

app = Flask("ApiExample")

config = toml.load(os.getenv("API_EXAMPLE_CONFIG_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "default.toml"))))

app.config['MYSQL_HOST'] = config["mysql"]["host"]
app.config['MYSQL_USER'] = config["mysql"]["user"]
app.config['MYSQL_PASSWORD'] = config["mysql"]["password"]
app.config['MYSQL_DB'] = config["mysql"]["db"]

mysql = MySQL(app)


def configure():
    mysql.connection.cursor().execute('CREATE TABLE IF NOT EXISTS `car_table` ('
                                      '`Placa` VARCHAR(10) PRIMARY KEY,'
                                      '`Cor` VARCHAR(4),'
                                      '`Ano` VARCHAR(5),'
                                      '`Modelo` VARCHAR(5))')


app.before_first_request(configure)


@app.route('/healthCheck', methods=['GET'])
def health_check():
    return Response('Ok', 200)


@app.route('/add/car', methods=['POST'])
def add_car():
    car_json = json.loads(request.data)
    validate_request(car_json, "car")
    cur = mysql.connection.cursor()
    stmt = "INSERT INTO `car_table` ({columns}) values ('{values}');".format(columns=",".join(car_json.keys()),
                                                                             values="', '".join(car_json.values()))
    cur.execute(stmt)
    mysql.connection.commit()
    cur.close()
    return "OK"


@app.route('/get/car/<placa>', methods=['GET'])
def get_car(placa):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM car_table WHERE Placa='{placa}'".format(placa=placa))
    return str(cur.fetchall())


@app.errorhandler(ValidationError)
def invalid_json_format(error):
    logger.exception(error)
    return Response(error.message, 400)


def get_app():
    return app


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
