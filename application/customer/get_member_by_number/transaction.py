from . import model
from common.satconnectserver2 import Database
from common.satconnectserver2.satlog import Logger
from flask import jsonify

Log = Logger()

def get_email (phone_number):
    try:
        # Connect to Database 
        conn = Database('database')
        # Phone_number = request.args.get('phone_number')
        
        values = {'cusphone' : phone_number["phone_number"]}
        result = model.get_email_model(conn,values)
        print(result)
        conn.close()
        

        Log.info(message=result)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)})