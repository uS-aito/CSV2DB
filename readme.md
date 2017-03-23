# CSV2DB
CSVファイルをRDBMSのDBへ変換するPythonスクリプトです。変換したDBへSQLを発行し結果を取得したり、他のアプリケーションに組み込むことができます。  

---
## Description
カンマ区切りのCSVファイルをsqliteのDBへ変換することができます。変換後のDBに対しSQLを発行して結果を取得することもできます。  
sqliteのDBファイル名やテーブル名を指定することができます。

## Demo
```
>>> import databaser
>>> dber = databaser()
>>> connection = dber.makeDB("test.csv",":memory:","temp")
Table temp was created.
>>> print(dber.executeSql(connection,"select * from temp"))
[('hoge', 'foo', 'bar'), ('1', '2', '3'), ('4', '5', '6')]
```

## Requirement
* python3.x

## Document
#### csv2db.makeDB(csvfile,dbfile,tblname)
CSVファイル*csvfile*から、データベースファイル*dbfile*に対しテーブル名*tblname*のDBを作成します。内部的にpython標準ライブラリのsqlite3を使用しており、*dbfile*に特別な名前`:memory:`を使用するとメモリ上にDBを作成します。  
このメソッドはSQLiteデータベースコネクションオブジェクトを返します。このオブジェクトを利用することで、作成したDBへSQLを発行したり、結果を取得することが可能です。

#### csv2db.executeSql(connection,sql,tpl=())
コネクションオブジェクト*connection*が指すDBに対し、*sql*で与えられたsql文を実行します。実行結果の各行のタプルからなるリストを返します。
コネクションオブジェクト*connection*は`makeDB`メソッドで得られるほか、`sqlite3.connect`メソッドの戻り値を利用することもできます。  
実行結果の例を以下に示します。  
```test.csv
# test.csv
hoge,foo,bar
1,2,3
4,5,6
```
```select * from temp
>>> executeSql(connection,"select * from temp")
[('hoge', 'foo', 'bar'), ('1', '2', '3'), ('4', '5', '6')]
```
***注意***  
このメソッドは*sql*に入力されたsql文をそのまま実行します。そのようなプログラムはSQLインジェクションに非常に脆弱になります。具体的な例として、ユーザの入力をSQL文に受け取りたい場合が挙げられます。  
この問題を解決するためには、`?`をSQL文中の変数を使いたい部分に埋め込み、引数をタプルとして*tpl*に与えます。

#### csv2db.readSql(self,connection)
コネクションオブジェクト*connection*が指すDBに対し、標準入力から受け取ったSQL文を実行し、結果を表示します。  
この関数は、CSVから変換されたDBに対し、人間がSQL文を発行することで内容を解析する目的で設計されました。

## License
本ソフトウェアはMITライセンスに準拠します。  
* [MIT License](http://opensource.org/licenses/mit-license.php)
