import os

from flask import Flask, jsonify

from config import DATABASE_NAME
from instance import config
import pandas as pd

from config import LOG_DIR
from logger import setup_logger
from medmap.core.kmeans import get_center_from_data
from medmap.db import get_db
from medmap.meta import DISEASES
from streaming.stream_data import start_streaming


server_logger = setup_logger(name=__name__, log_file=os.path.join(LOG_DIR, 'server_log'), level="DEBUG")


def set_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=config.FLASK_SECRETS['SECRET_KEY'],
        DATABASE=os.path.join(app.instance_path, DATABASE_NAME)
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass
    try:
        os.makedirs(LOG_DIR)
    except FileExistsError:
        pass
    return app


def create_app(test_config=None):
    app = set_app(test_config)

    server_logger.debug(msg="Server initiated")
    with app.app_context():
        conn = get_db()

    # TODO: USE BLUEPRINTS
    @app.route('/get_all')
    def get_all():
        df = pd.read_sql_query("SELECT * FROM APP", conn)
        df['GEO_LAT'] = pd.to_numeric(df['GEO_LAT'], errors='coerce')
        df['GEO_LONG'] = pd.to_numeric(df['GEO_LONG'], errors='coerce')
        ret_dict = {}
        for disease in DISEASES:
            data = df[df.DISEASE == disease]
            geo_lat = data['GEO_LAT']
            geo_long = data['GEO_LONG']
            ret_dict[disease] = list(zip(geo_lat, geo_long))
        return jsonify(ret_dict)

    @app.route('/get_center')
    def get_center():
        ret_dict = {}
        df = pd.read_sql_query("SELECT * FROM APP", conn)
        df['GEO_LAT'] = pd.to_numeric(df['GEO_LAT'], errors='coerce')
        df['GEO_LONG'] = pd.to_numeric(df['GEO_LONG'], errors='coerce')
        for disease in DISEASES:
            ret_dict[disease] = get_center_from_data(df, disease)
        ret_dict['status'] = 200
        return jsonify(ret_dict)

    from . import db
    db.init_app(app)

    start_streaming(conn)

    server_logger.debug("Server started successfully")
    return app
