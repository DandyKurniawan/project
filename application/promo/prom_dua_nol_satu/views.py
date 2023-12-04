from flask import  request, session, redirect, jsonify, Flask, Blueprint
from . import transaction


prom_dua_nol_satu = Blueprint("prom_dua_nol_satu",__name__, template_folder="templates", static_folder="/static")

@prom_dua_nol_satu.route("/promo/prom_dua_nol_satu",methods=["POST"])
def promo_modul_dua_nol_satu():
    
    faktur = request.json

    result =  transaction.promo_modul(faktur)
    return result