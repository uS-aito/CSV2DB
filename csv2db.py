#coding:utf-8
# Copyright (c) 2016 uS-aito
# Released under the MIT license
# http://opensource.org/licenses/mit-license.php

import sys
import sqlite3
import argparse

class csv2db(object):
    """
    1.コマンドライン引数を解析する
    2.ファイルを開く
    3.一行読み込んでテーブルを作成
        3.1.データベースファイル作成
        3.2.カラム名読み込み
        3.3.テーブル作成
    4.順繰りに追加していく
        4.1.一行読み込み
        4.2.一行追加
    5.sql文を読み込んで実行
    """    
    def _openCsv(self,filename):
        return open(file=filename,mode="r")

    def _connectDB(self,dbname):
        return sqlite3.connect(database=dbname)

    def _readColumnName(self,file):
        """
        1.現在のオフセットを取得
        2.オフセットを0にして一行読み込み,ColumnNameを取得
        3.元のオフセットをセット
            3.1.ただし、元のオフセットが0の場合はやらない
        """
        current_offset = file.tell()
        file.seek(0)
        first_columun = file.readline()
        if (current_offset != 0):
            file.seek(current_offset)
        return first_columun[:-1].split(",")

    def _createTable(self,connection,tblname,columnnames):
        def createSql(tblname,columnnames):
            sql = "create table "+tblname+" ("
            for name in columnnames:
                sql = sql + name + ","
            sql = sql[:-1] + ")"
            return sql
        c = connection.cursor()
        sql = createSql(tblname,columnnames)
        c.execute(sql)
        connection.commit()

    def _readValuesList(self,file):
        values_list = file.readlines()
        return values_list
    
    def _addValues(self,connection,tblname,valuesList):
        def createSql(tblname,values):
            sql = "insert into "+tblname+" values ("
            for var in range(len(values)):
                sql = sql + "?,"
            sql = sql[:-1] + ")"
            return sql
        c = connection.cursor()
        for values in valuesList:
            values = values.replace("\r","").replace("\n","")
            values = values.split(",")
            sql = createSql(tblname,values)
            c.execute(sql,tuple(values))
        connection.commit()

    def readSql(self,connection):
        def printSqlResult(result,cursor):
            def createNameString(name_tupple):
                names = ""
                for name in name_tupple:
                    names = names + name[0] + ", "
                return names[:-2]
            def createValueString(value_tupple):
                values = ""
                for value in value_tupple:
                    values = values + value + ", "
                return values[:-2]
            """
            1.descriptionの各要素の先頭を表示
            2.rowを表示
            """
            desc = cursor.description
            print(createNameString(desc))
            for value_tupple in result:
                print(createValueString(value_tupple))

        """
        1.sqlを読む
        2.実行する
        3.結果を出力する
        """
        input_sql = input("> ")
        c = connection.cursor()
        try:
            result = c.execute(input_sql)
        except:
            print("Invalid SQL")
            return None
        else:
            printSqlResult(result,c)

    def makeDB(self,csvfile,dbfile,tblname):
        with self._openCsv(csvfile) as f:
            connection = self._connectDB(dbfile)
            column_name = self._readColumnName(f)
            self._createTable(connection,tblname,column_name)
            values_list = self._readValuesList(f)
            self._addValues(connection,tblname,values_list)
        print("Table " + tblname + " was created.")
        return connection

    def executeSql(self,connection,sql,tpl=()):
        c = connection.cursor()
        try:
            result = c.execute(sql,tpl)
        except:
            print("Invalid SQL")
            return None
        else:
            data = []
            names = []
            for name in c.description:
                names.append(name[0])
            data.append(tuple(names))
            for value_tupple in result:
                data.append(value_tupple)
        return data

def main():
    TABLENAME = "temp"

    p = argparse.ArgumentParser()
    p.add_argument("-c", "--csv-file-path", help="Path to CSV file")
    p.add_argument("-t", "--table-name", help="Table Name")
    p.add_argument("-d","--database-file-name", help="Database file name")
    args = p.parse_args()
    print(args)
    csvFileName = args.csv_file_path
    tableName = args.table_name
    databaseFileName = args.database_file_name

    c2d = csv2db()
    connection = c2d.makeDB(csvFileName,databaseFileName,tableName)
    while True:
        c2d.readSql(connection)

if __name__ == '__main__':
    main()
