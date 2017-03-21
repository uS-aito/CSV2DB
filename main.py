#coding:utf-8
import sys
import sqlite3

class databaser(object):
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
    def parseArgs(self):
        return sys.argv[-1]
    
    def openCsv(self,filename):
        return open(file=filename,mode="r")

    def createDB(self,dbname):
        return sqlite3.connect(database=dbname)

    def readColumnName(self,file):
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

    def createTable(self,connection,tblname,columnnames):
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

    def readValuesList(self,file):
        values_list = file.readlines()
        return values_list
    
    def addValues(self,connection,tblname,valuesList):
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

def main():
    TABLENAME = "temp"

    dber = databaser()
    filename = dber.parseArgs()
    with dber.openCsv(filename) as f:
        connection = dber.createDB(":memory:")
        column_name = dber.readColumnName(f)
        dber.createTable(connection,TABLENAME,column_name)
        values_list = dber.readValuesList(f)
        dber.addValues(connection,TABLENAME,values_list)
    print("Table " + TABLENAME + " was created.")

    while True:
        dber.readSql(connection)

if __name__ == '__main__':
    main()
