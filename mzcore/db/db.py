#!/usr/bin/env python
# coding: utf-8
import sys

reload(sys)

sys.setdefaultencoding('utf-8')
from mzcore.config import Log
from mysql_db import MysqlDB
from sqlite_db import SqliteDB
class DB(object):
    """
    修改服务器上的配置文件/etc/my.cnf，在对应位置添加以下设置:
    [client]
    default-character-set = utf8mb4

    [mysql]
    default-character-set = utf8mb4

    [mysqld]
    character-set-client-handshake = FALSE
    character-set-server = utf8mb4
    collation-server = utf8mb4_unicode_ci
    init_connect='SET NAMES utf8mb4'
    """

    def __init__(self, conf):
        self.conf = conf
        if conf['type'].upper() == "MYSQL":
        	self.db=MysqlDB(conf)
        elif conf['type'].upper() == "SQLITE":
        	self.db=SqliteDB(conf)
        else:
        	return False
        # config = {
        #     'host': conf['host'],
        #     'port': conf['port'],
        #     'user': conf['user'],
        #     'passwd': conf['passwd'],
        #     'charset':'utf8mb4', # 支持1-4个字节字符
        #     'cursorclass': pymysql.cursors.DictCursor
        # }
        # self.conn = pymysql.connect(**config)
        # self.conn.autocommit(1)
        # # for thread-save
        # self.lock = threading.Lock()

        # self.create_db(conf['database'])
        # self.conn.select_db(conf['database'])

        # # cache table cols
        # self.table_cols = {}
        # for t in self.show_tables():
        #     self.table_cols[t] = self.get_table_column_name(t)

    def show_database(self):
        c = self.conn.cursor()
        sql = 'SHOW DATABASES'
        Log.debug('DB -> %s' % sql)
        c.execute(sql)
        return [r['Database'] for r in c.fetchall()]

    def show_tables(self):
        c = self.conn.cursor()
        sql = 'SHOW TABLES'
        Log.debug('DB -> %s' % sql)
        c.execute(sql)
        return [r['Tables_in_'+self.conf['database']] for r in c.fetchall()]

    def create_db(self, db_name):
        """
        @brief      Creates a database
        @param      db_name  String
        """
        if self.conf['database'] not in self.show_database():
            sql = 'CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci' % db_name
            Log.debug('DB -> %s' % sql)
            self.execute(sql)

    def create_table(self, table, cols):
        """
        @brief      Creates a table in database
        @param      table  String
        @param      cols   String, the cols in table
        """
        if table not in self.table_cols:
            sql = 'CREATE TABLE IF NOT EXISTS %s(id int primary key auto_increment, %s) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci' % (table, cols)
            Log.debug('DB -> %s' % sql)
            self.execute(sql)
            self.table_cols[table] = ['id'] + [c.strip().split(' ')[0] for c in cols.split(',')]

    def delete_table(self, table):
        """
        @brief      Delete a table in database
        @param      table  String
        """
        if table in self.table_cols:
            sql = "DROP TABLE IF EXISTS %s" % table
            Log.debug('DB -> %s' % sql)
            self.execute(sql)
            self.table_cols.pop(table)

    def table(self,value):
        self.db.table(value)
        return self
    def field(self,value="*"):
        self.db.field(value)
        return self
    def where(self,value="1=1"):
        self.db.where(value)
        return self
    def order(self,value=None):
        self.db.order(value)
        return self
    def groupby(self,value=None):
        self.db.groupby(value)
        return self
    def limit(self,value=None):
        self.db.limit(value)
        return self
    def page(self,value):
        self.db.page(value)
        return self
    def union(self,union_type="all",table_name=""):
        self.db.union(union_type,table_name)
        return self
    def sql_join(self,join_type="INNER",table_name="",table_alias=None,join_on=False):
        self.db.sql_join(join_type,table_name,table_alias,join_on)
        return self   
    def add(self,value):
        self.db.add(value)
    def save(self,value):
        self.db.save(value)

    def insert(self, table, value):
        """
        @brief      Insert a row in table
        @param      table  String
        @param      value  Tuple
        """
        # col_name = self.table_cols[table][1:]
        col_name=value.keys()
        # print array_join(value.values(), ',')
        # # print col_name
        # # print value.values()
        # return
        sql = "INSERT INTO %s(%s) VALUES (%s)" % (table, str(','.join(col_name)), array_join(value.values(), ','))
        Log.debug('DB -> %s' % sql)
        # print sql
        self.execute(sql)
    def update(self,table,value,where):
        col_name=value.keys()
        setfield=[]
        for key,valu in value.items():
            if valu is None:
                valu=''
            afield="%s = %s" %(key,("'"+valu+"'" if isinstance(valu,basestring)  else valu))
            setfield.append(afield)
        sql="update %s set %s " %(table,str(','.join(setfield)))
        if isinstance(where,dict):
            swhere=[]
            for wkey,wvalue in where.items():
                awhree="%s = %s" %(wkey,("'"+wvalue+"'" if isinstance(wvalue,basestring) else wvalue))
                swhere.append(awhree)
            sql=sql+" where %s" %(str(' and '.join(swhere)))
        elif isinstance(where,str):
            sql=sql+where
        else:
            return 0
        # print sql
        Log.debug('DB -> %s' % sql)
        self.execute(sql)

    def insertmany(self, table, values):
        """
        @brief      Insert many rows in table
        @param      table  String
        @param      values  Array of tuple
        """
        col_name = self.table_cols[table][1:]
        sql = 'INSERT INTO %s(%s) VALUES (%s)' % (table, ','.join(col_name), ','.join(['%s'] * len(values[0])))
        Log.debug('DB -> %s' % sql)
        self.execute(sql, values)

    def select(self):
        """
        @brief      select all result from table
        @param      table  String
        @param      field  String
        @param      condition  String
        @return     result  Tuple
        """
        return self.db.select()

    def get_table_column_name(self):
        """
        @brief      select all result from table
        @param      table  String
        @return     result  Array
        """
        return self.db.get_table_column_name();
    def execute(self, sql, values=None):
        """
        @brief      execute sql commands, return result if it has
        @param      sql  String
        @param      value  Tuple
        @return     result  Array
        """
        # c = self.conn.cursor()
        # self.lock.acquire()
        # hasReturn = sql.lstrip().upper().startswith("SELECT")

        # result = []
        # try:
        #     if values:
        #         c.executemany(sql, values)
        #     else:
        #         c.execute(sql)

        #     if hasReturn:
        #         result = c.fetchall()

        # except Exception, e:
        #     Log.error(traceback.format_exc())
        #     self.conn.rollback()
        # finally:
        #     self.lock.release()

        # if hasReturn:
        #     return result
        return self.db.execute(sql,values)

    def delete(self, table, where):
        """
        @brief      execute sql commands, return result if it has
        @param      table  String
        @param      field  String
        @param      condition  String
        """
        sql = "DELETE FROM %s" % (table)
        if isinstance(where,dict):
            swhere=[]
            for wkey,wvalue in where.items():
                awhree="%s = %s" %(wkey,("'"+wvalue+"'" if isinstance(wvalue,basestring) else wvalue))
                swhere.append(awhree)
            sql=sql+" where %s" %(str(' and '.join(swhere)))
        elif isinstance(where,basestring):
            sql=sql+where
        else:
            return 0
        Log.debug('DB -> %s' % sql)
        self.execute(sql)

    def close(self):
        """
        @brief      close connection to database
        """
        Log.debug('DB -> close')
        # 关闭数据库连接
        self.conn.close()

        