from flask import  request, session, redirect, jsonify, Flask, Blueprint
from datetime import datetime, date
from flask_session import Session
from common.satconnectserver2 import Database
from common.satconnectserver2.satlog import Logger
from application.customer.get_member_by_number.views import get_member_by_number
from application.promo.prom_dua_nol_satu.views import prom_dua_nol_satu

Log = Logger()
app = Flask(import_name=__name__)

app.register_blueprint(get_member_by_number)
app.register_blueprint(prom_dua_nol_satu)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)