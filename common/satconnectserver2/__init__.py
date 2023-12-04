"""
Update : 2022-27-09
SatConnectServer Versi 2 untuk exec
Return dictionary
Version : 1.0.0
Requirements :
 Standard Lib : satlog
 Library : psycopg2
"""

import psycopg2
import os
from common.satconnectserver2.satlog import Logger

Log = Logger()

class Database() :
    """
    Class Database digunakan untuk obj koneksi ke database postgres
    Cara penggunaan : conn = Database("param_database")
    Fungsi : select, selectData, Execute, ExecuteData, Close, dll (untuk mengetahui bisa jalankan fungsi print(dir(Database))
    Syarat : Harus memiliki file Connection2.cfg didalam folder /config dan standard library satlog
    Cara pembuatan Connection String pada file Connection2.cfg, jalankan perintah ''python CreateConnection2.py'' pada terminal, ikuti semua langkah-langkahnya dan copy paste configuration ke file COnnection2.cfg
    @param param_database : Merupakan parameter alias database dari file Connection2.cfg yang ada di client
    @return: status = nilai boolean (True = berhasil, False = gagal)
            data = Hasil select statement
            msg = message informasi
            notice = return message dari procedure database
            rowcount = jumlah baris
            errorcode = code error dari postgres
            errormsg = msg error yang dapat ditampilkan ke user/client
    @rtype: dict
    """

    def __init__(self, paramDatabase, autocommit = False):
        self.__paramDatabase = paramDatabase
        self.status = {"status":False,"msg":"","errorcode":""}
        self.__ConnectDatabase(autocommit)

    def __ConnectDatabase(self, autocommit):
        try :
            dictParser = DictParserCFG()._main(self.__paramDatabase)
            if dictParser[0] :
                valParser = dictParser[1].get(self.__paramDatabase.upper(),None)
                try:
                    username = valParser.get("username")
                    database_name = valParser.get("databaseName")
                    password = valParser.get("password")
                    host = valParser.get("host", "127.0.0.1")
                    port = valParser.get("port")
                    _param_string = "host='{host}' port='{port}' dbname='{dbname}' user='{user}' password='{password}'".format(
                                    host=host,
                                    port=port,
                                    dbname=database_name,
                                    user=username,
                                    password=password
                                )
                    
                    Log.error("========" + _param_string)
                    try:
                        self._conn = psycopg2.connect(_param_string)
                        self._conn.autocommit = autocommit
                        self._curs = self._conn.cursor()
                        self.status = {"status":True, "msg":"Koneksi Database Postgres Berhasil","errorcode":"00"}
                    except psycopg2.Error as e:
                        Log.error(message=e)
                        self.status = {"status": False, "msg": "Koneksi Database Error, Terdapat kesalahan Koneksi","errorcode":"01"}
                except Exception as e:
                    Log.error(message=e)
                    self.status = {"status": False, "msg": "Error Konfigurasi Database","errorcode":"02"}
            else :
                Log.error(message = "File Not Found")
                self.status = {"status": False, "msg": "File Not Found","errorcode":"03"}
        except Exception as e:
            Log.error(message=e)
            self.status = {"status": False, "msg": "Error database init konfigurasi","errorcode":"04"}

    def select(self, select_string):
        """
            Fungsi ini digunakan untuk select query yang tidak membutuhkan parameter
            @param select_string: Merupakan statement query yang dipakai
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"] :
            try:
                self._curs.execute(select_string)
                result["data"] = self._curs.fetchall()
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "select statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, select_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status
        
    #
    
    #

    def selectData(self, select_string, param, rownum="ALL"): 
        """ 
            Fungsi ini digunakan untuk select query yang membutuhkan parameter
            @param select_string: Merupakan statement query yang dipakai
            @param param: Merupakan inputan parameter yang dibutuhkan
            @param rownum: jumlah baris yang akan dipilih
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        #belom edit
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"]:
            try:
                self._curs.execute(select_string, param)
                if rownum == "ALL":
                    data = self._curs.fetchall()
                else:
                    data = self._curs.fetchmany(int(rownum))
                result["data"] = data
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "select statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, select_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status

    #


    #


    def selectHeader(self, select_string):
        """
            Fungsi ini digunakan untuk select query yang tidak membutuhkan parameter dan membutuhkan header
            @param select_string: Merupakan statement query yang dipakai
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        data = []
        if self.status["status"]:
            try:
                self._curs.execute(select_string)
                header = []
                for col in self._curs.description:
                    header.append(col[0])
                dataTemp = self._curs.fetchall()
                data.append(header)
                data.append(dataTemp)
                result["data"] = data
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "select statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, select_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status

    def selectDataHeader(self, select_string, param):
        """
            Fungsi ini digunakan untuk select query yang membutuhkan parameter dan membutuhkan header
            @param select_string: Merupakan statement query yang dipakai
            @param param: Merupakan inputan parameter yang dibutuhkan
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        data = []
        if self.status["status"]:
            try:
                self._curs.execute(select_string, param)
                header = []
                for col in self._curs.description:
                    header.append(col[0])
                dataTemp = self._curs.fetchall()
                data.append(header)
                data.append(dataTemp)
                result["data"] = data
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "select statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, select_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status

    def execute(self, exec_string):
        """
            Fungsi ini digunakan untuk memproses query (insert) yang tidak membutuhkan parameter
            @param exec_string: Merupakan statement query yang dipakai
            @type exec_string: str
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"]:
            try:
                self._curs.execute(exec_string)
                self._curs.execute("commit")
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "execute statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, exec_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status

    def executeData(self, exec_string, param):
        """
            Fungsi ini digunakan untuk memproses query (insert) yang membutuhkan parameter
            @param exec_string: Merupakan statement query yang dipakai
            @type exec_string: str
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"]:
            try:
                self._curs.execute(exec_string, param)
                self._curs.execute("commit")
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "execute statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, exec_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status

    def executeDataNoCommit(self, exec_string, param):
        """
            Fungsi ini digunakan untuk memproses query (insert) yang membutuhkan parameter dan non commit
            @param exec_string: Merupakan statement query yang dipakai
            @type exec_string: str
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"]:
            try:
                self._curs.execute(exec_string, param)
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "execute statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, exec_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else:
            return self.status

    def executeMany(self, exec_string, param):
        """
            Fungsi ini digunakan untuk memproses query (insert) yang membutuhkan parameter dan commit
            @param exec_string: Merupakan statement query yang dipakai
            @param param: Merupakan inputan parameter yang dibutuhkan
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"]:
            try:
                self._curs.executemany(exec_string, param)
                self._curs.execute("commit")
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "executemany statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, exec_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status

    def executePro(self, exec_string, param):
        """
            Fungsi yang digunakan untuk execute procedure yang membutuhkan parameter
            @param exec_string: Merupakan statement query yang dipakai
            @param param: Merupakan inputan parameter yang dibutuhkan
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"]:
            try:
                self._curs.callproc(exec_string, param)
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "executePro statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, exec_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status

    def executeValue(self, exec_string, param):
        """
            Function ini digunakan untuk execute value
            @params execString: (str) merupakan query yang dipakai
            @params param: (list) berupa list of list dari value yang akan digunakan
            @return: status = nilai boolean (True = berhasil, False = gagal)
                        data = Hasil select statement
                        msg = message informasi
                        notice = return message dari procedure database
                        rowcount = jumlah baris
                        errorcode = code error dari postgres
                        errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        from psycopg2.extras import execute_values
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"]:
            try:
                execute_values(self._curs, exec_string, param)
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "execute_values statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, exec_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status

    def executeFunc(self, exec_string, param):
        """
            Fungsi ini digunakan untuk memproses query (insert) yang membutuhkan parameter dan commit
            @param exec_string: Merupakan statement query yang dipakai
            @param param: Merupakan inputan parameter yang dibutuhkan
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"]:
            try:
                myVar = self._curs.var(self.psycopg2.STRING)
                vResult = self._curs.callfunc(exec_string, myVar, param)
                result["data"] = vResult
                result["notices"] = self._conn.notices
                result["rowcount"] = self._curs.rowcount
                result["status"] = True
                result["msg"] = "executeFunc statement berhasil"
                result["errorcode"] = "0"
            except Exception as e :
                self._curs.execute("rollback")
                message = e.pgcode
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, exec_string, e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result
        else :
            return self.status

    def close(self):
        """
            Fungsi ini digunakan menutup koneksi
            @return: status = nilai boolean (True = berhasil, False = gagal)
                    data = Hasil select statement
                    msg = message informasi
                    notice = return message dari procedure database
                    rowcount = jumlah baris
                    errorcode = code error dari postgres
                    errormsg = msg error yang dapat ditampilkan ke user/client
            @rtype: dict
        """
        result = {"status":False,"data":"","msg":"","notices":"","rowcount":"","errorcode":"","errormsg":""}
        if self.status["status"]:
            try:
                self._conn.close()
                result["status"] = True
                result["msg"] = "Berhasil Menutup Koneksi"
                result["errorcode"] = "0"
            except Exception as e :
                nilai = "Log Error PGCode : %s - query: %s - PGError : %s " % (e.pgcode, "Delete Connection", e.pgerror)
                msgerror = e.pgerror
                Log.error(message=nilai)
                result["errorcode"] = e.pgcode
                result["msg"] = msgerror
                result["errormsg"] = msgerror.split("\n")[0]
            return result

    def __delete__(self):
        self.close()

class DictParserCFG() :
    def __init__(self):
        self.__dict = {}

    def _main(self,param):
        try :
            with open(f"{os.getcwd()}/common/config/Connection2.cfg", "r") as stream:
                line = stream.read()
            listLine = line.split("\n")
            for val in listLine :
                valDB = decoder(val.split(" "))
                if valDB[0].upper() == param.upper() :
                    dictValDB = self.__split(valDB)
                    self.__dict[valDB.pop(0).upper()] = dictValDB
                    return True,self.__dict
            return False, self.__dict
        except :
            return False,self.__dict

    def __split(self,param):
        databaseAlias, databaseName, host, username, password, port, schema = param
        if os.environ.get("GAE_ENV") == "standard" or os.environ.get("CLOUD_APPS") == "CLOUD_RUN" :
            if ":" in host :
                host = "/cloudsql/{instance}".format(instance=host)
        return {
            "databaseName": databaseName.lower(),
            "host": host,
            "username": username.lower(),
            "password": password,
            "port": port,
            "schema": schema.lower()
        }

def decoder(data):
    """
    Fungsi ini untuk decode ordinal menjadi char
    @param data: list of encoded string
    @type data: list[str]
    @return: decoded list of string
    @rtype: list[str]
    """
    result = []
    for datum in data:
        temp = ""
        for x in datum.strip().split("+"):
            temp = temp + chr(int(x))
        result.append(temp)
    return result