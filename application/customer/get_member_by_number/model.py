def get_email_model (conn,param) :
    sql = """SELECT name, email, ponta_number FROM alfamidi.customer WHERE phone_number = %(cusphone)s"""
    return conn.selectData(sql, param)

#untuk mendapatkan nama, email, ponta number berdasarkan nomor telephone (^)