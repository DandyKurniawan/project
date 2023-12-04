from flask import  request, session, redirect, jsonify, Flask, Blueprint
from . import transaction

get_member_by_number = Blueprint("get_member_by_number",__name__, template_folder="templates", static_folder="/static")

@get_member_by_number.route("/customer/get_member_by_number",methods=["POST"])
def select_by_id():
    
    phone_number = request.json

    result =  transaction.get_email(phone_number)
    return result
    
        
   