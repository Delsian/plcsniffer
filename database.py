from mysql.connector import (connection, errorcode)
import mysql.connector

DB_HOST = "192.168.0.107"
DB_USER = "pi"
DB_PASS = "zzzzzz"
DB_NAME = "plcsniff"

class Database(object):
    __instance = None
    __con = None

    def __new__(cls):
        if Database.__instance is None:
            Database.__instance = object.__new__(cls)
        return Database.__instance

    def __init__(self):
        if not self.__con:
            self.__con = connection.MySQLConnection(
                host=DB_HOST,
                user=DB_USER,
                passwd=DB_PASS,
                database=DB_NAME
            )

    def __del__(self):
        self.__con.close()

    def commit(self):
        self.__con.commit()

    def getCursor(self):
        return self.__con.cursor(dictionary=True)
