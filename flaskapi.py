from mysql.connector import errorcode
import mysql.connector
import configparser
import logging
import os
from flask import Flask,jsonify,request,make_response



dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(f'{dir_path}/flaskapi.cfg')
logging.basicConfig(filename=config['DEFAULT']['log_file'], level=config['DEFAULT']['log_level'])

app=Flask(__name__)

def connect():
    return mysql.connector.connect(
        user=config['DEFAULT']['mysql_user'],
        password=config['DEFAULT']['mysql_password'],
        host=config['DEFAULT']['mysql_host'],
        database=config['DEFAULT']['mysql_database'],
        auth_plugin='mysql_native_password')  




@app.route("/Select", methods=['GET'])
def select():
    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        query = f"SELECT * FROM {config ['DEFAULT']['mysql_database']}.{config ['DEFAULT']['mysql_table']};"
        cursor.execute(query)
        response=jsonify(cursor.fetchall())
        mysqldb.commit()
        mysqldb.close()

    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return make_response("AUTH ERROR! PLEASE CHECK LOG FILE.")
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return make_response("DB NOT EXIST! PLEASE CHECK LOG FILE.")
            
        else:
            logging.error(str(e))
            return make_response ("SOME ERROR OCCURED! PLEASE CHECK LOG FILE.")
            
    return("response")






@app.route("/Insert",methods=['POST','PUT'])
def insert():
    json_object=request.get_json()
    name=json_object["name"]
    surname=json_object["surname"]
    email =json_object["email"]
    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        query = f"""INSERT INTO 
        {config ['DEFAULT']['mysql_database']}.{config ['DEFAULT']['mysql_table']}(name, surname, email) VALUES
        ('{name}', '{surname}', '{email}');"""
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return make_response("AUTH ERROR! PLEASE CHECK LOG FILE.")
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return make_response("DB NOT EXIST! PLEASE CHECK LOG FILE.")
            
        else:
            logging.error(str(e))
            return make_response ("SOME ERROR OCCURED! PLEASE CHECK LOG FILE.")
            
    return("SUCCESS")

@app.route("/Delete",methods=['DELETE'])

def delete(ID):
    json_object = request.get_json()
    number=json_object["number"]

    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        query = f""" DELETE FROM {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']} WHERE ID = {number}; """
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return make_response("AUTH ERROR! PLEASE CHECK LOG FILE.")
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return make_response("DB NOT EXIST! PLEASE CHECK LOG FILE.")
            
        else:
            logging.error(str(e))
            return make_response("SOME ERROR OCCURED! PLEASE CHECK LOG FILE.")
            
            
    return("SUCCESS")






if __name__ == "__main__":
    app.run(host=config['DEFAULT']['host'], port=config['DEFAULT']['port'])

    