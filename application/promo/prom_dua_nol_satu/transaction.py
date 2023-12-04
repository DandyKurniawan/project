from . import model
from common.satconnectserver2 import Database
from common.satconnectserver2.satlog import Logger
from flask import jsonify, request
from .model import promo_modul_model

Log = Logger()
 
def promo_modul(self):
    try:
        conn = Database('database')

        promo = request.json.get('promo')
        result = promo_modul_model(conn,promo)
        print(result) 
        conn.close()
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

