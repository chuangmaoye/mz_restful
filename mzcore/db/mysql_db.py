#!/usr/bin/env python
# coding: utf-8
import sys

reload(sys)

sys.setdefaultencoding('utf-8')
#===================================================
from mzcore.config import Log
#---------------------------------------------------
import pymysql
import threading
import traceback
import time
#===================================================

def array_join(arr, c):
    t = ''
    for a in arr:
        # if isinstance(a,str):
        #     t+="'%s'" % (str(a))+c
        # else:
        #     t+="%s" % (str(a))+c
        t += "'%s'" % str(a) + c
    return t[:-len(c)]
def ret_run(str,func,*args):
    t=time.time()
    r=False
    try:
        r = func(*args)
        return r+1
    except:
        Log.error(str+":"+traceback.format_exc())
        return False

class MysqlDB(object):
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
        config = {
            'host': conf['host'],
            'port': conf['port'],
            'user': conf['user'],
            'passwd': conf['passwd'],
            'charset':'utf8mb4', # 支持1-4个字节字符
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.union_count=0
        self.orders={}
        self.wheres={}
        self.groups={}
        self.limits={}
        self.fields={}
        self.union_tables={}
        self.union_types={}
        self.join_types={}
        self.join_tables={}
        self.join_count=0
        self.join_tables_on={}
        self.join_tables_alias={}
        self.sql_values=[]
        self.vtable=""
        self.conn = pymysql.connect(**config)
        self.conn.autocommit(1)
        # for thread-save
        self.lock = threading.Lock()
        self.database=conf['database']
        self.create_db(conf['database'])
        self.conn.select_db(conf['database'])

        # cache table cols
        self.table_cols = {}
        for t in self.show_tables():
            self.table_cols[t] = self.get_table_column_name(t)
    #from table
    def table(self,value=None):

        if value:
            self.vtable=value
            Log.debug('DB -> %s' % value)
            return self
        else:
            return False
    def field(self,value="*"):
        fieldlist=[]
        fieldsstr=""
        if value=="*":
            for valu in self.table_cols[self.vtable]:
                opstr="CAST(%s AS CHAR) AS %s"
                if valu['dataType']=='datetime' or valu['dataType']=='date':
                    opstr=opstr % (valu['field'],valu['field'])
                    fieldlist.append(opstr)
                else:
                    fieldlist.append(valu['field'])
            fieldsstr=",".join(fieldlist)   
        else:
            fieldsstr=value

        # else:
        #     valuelist=value.split(",")
        #     print valuelist.index(u"id")
        #     for va in self.table_cols[self.vtable]:
        #         opstr="CAST(%s AS CHAR) AS %s"
        #         if ret_run("search index",valuelist.index,va['field']):
        #             if va['dataType']=='datetime' or va['dataType']=='date':
        #                 opstr=opstr % (va['field'],va['field'])
        #                 fieldlist.append(opstr)
        #             else:
        #                 fieldlist.append(va['field'])

        
        self.fields[self.union_count]=fieldsstr
        Log.debug('DB -> %s' % fieldsstr)
        return self
    def where(self,value="1=1"):
        # self.vwheres=[]
        # self.vwheres.append(value)
        self.wheres[self.union_count]=value
        Log.debug('DB -> %s' % value)
        return self
    def order(self,value=None):
        # self.vorders=[]
        if value:
            # self.vorders.append(value)
            self.orders[self.union_count]=value
            Log.debug('DB -> %s' % value)
        return self
    def groupby(self,value=None):
        if value:
            self.groups[self.union_count]=value
            Log.debug('DB -> %s' % value)
        return self
    def limit(self,value=None):
        if value:
            self.limits[self.union_count]=value
            Log.debug('DB -> %s' % value)
        return self
    def page(self,value):
        self.vlimit=value
        Log.debug('DB -> %s' % value)
        return self
    def union(self,union_type="all",table_name=""):
        if table_name:
            self.union_count+=1
            self.union_tables[self.union_count]=table_name
            self.union_types[self.union_count]=union_type
            Log.debug('DB -> union %s table %s' % (union_type,table_name))
        return self
    def sql_join(self,join_type="INNER",table_name="",table_alias=None,join_on=False):
        # log=""
        if  table_name:
            if join_type.upper()=="INNER" or join_type.upper()=="LEFT" or join_type.upper()=="RIGHT":
                self.join_types[self.union_count]={self.join_count:join_type}
            else:
                return False
            self.join_tables[self.union_count]={self.join_count:table_name}
            # log=" join %s %s " % join_type,table_name
            if  table_alias:
                self.join_tables_alias[self.union_count]={self.join_count:table_alias}
                # log=log+"as %s" % table_alias
            if join_on:
                self.join_tables_on[self.union_count]={self.join_count:join_on}
            else:
                return False
            self.join_count+=1
        return self
    def select(self):
        """
        @brief      select all result from table
        @param      table  String
        @param      field  String
        @param      condition  String
        @return     result  Tuple
        """
        sql = "SELECT %s FROM %s" % (self.fields[0],self.vtable)
        # sql = "SELECT %s FROM %s"
        # self.sql_values.extend([self.fields[0],self.vtable])
        if len(self.join_tables) > 0:
            sql=self.u_join(sql,0)
        if len(self.wheres) > 0:
            sql=self.u_where(self.wheres[0],sql)
        if len(self.orders) > 0:
            sql=self.u_order(self.orders[0],sql)
        if len(self.groups) > 0:
            sql=self.u_groupby(self.groups[0],sql)
        if len(self.limits) > 0:
            sql=self.u_limit(self.limits[0],sql)
        # if len(self.limits) > 0:
        #     sql=self.u_limit(self.limits[0],sql)
        if self.union_count > 0:
            sql+=self.union_select()
        # if field and condition:
        #     sql += " WHERE %s='%s'" % (field, condition)

        
        # print sql
        sql_values=tuple(self.sql_values)
        dbsql=sql % sql_values
        Log.debug('DB -> %s' % dbsql)
        self.u_clear()
        # print sql_values
        return self.execute(sql,sql_values)
    def union_select(self):
        sql = ""
        sqls=[]
        if self.union_count > 0:
            for key,value in self.union_tables.items():
                sql=" union %s SELECT %s FROM %s " % (self.union_types[key],self.fields[key],self.union_tables[key])
                # sql=" union %s SELECT %s FROM %s "
                # self.sql_values.extend([self.union_types[key],self.fields[key],self.union_tables[key]])
                if self.join_tables.has_key(key):
                    sql=self.u_join(sql,key)
                if self.wheres.has_key(key):
                    sql=self.u_where(self.wheres[key],sql)
                if self.orders.has_key(key):
                    sql=self.u_order(self.orders[key],sql)
                if self.groups.has_key(key):
                    sql=self.u_groupby(self.groups[key],sql)
                if self.limits.has_key(key):
                    sql=self.u_limit(self.limits[key],sql)
                sqls.append(sql)
        return "".join(sqls)             

    def u_where(self,data,sql):
        sqlwhere=""
        if isinstance(data,dict):
            swhere=[]
            for wkey,wvalue in data.items():
                # awhree="%s = %s" %(wkey,("'"+wvalue+"'" if isinstance(wvalue,basestring) else wvalue))
                awhree="%s = " % wkey
                # if isinstance(wvalue,int):
                #     awhree=awhree+" %d"
                # else:
                awhree=awhree+" %s"
                self.sql_values.append(("'"+wvalue+"'" if isinstance(wvalue,basestring) else wvalue))
                swhere.append(awhree)
            sqlwhere=(str(' and '.join(swhere)))
        elif isinstance(data,basestring):
            sqlwhere=sqlwhere+data
        else:
            return False
        sql=sql + " where %s " % sqlwhere
        return sql
    def u_order(self,data,sql):
        if data :
            sql=sql+" order by %s " % data
            # sql=sql+" order by %s "
            # self.sql_values.append(data)
        return sql
    def u_groupby(self,data,sql):
        if data :
            sql=sql+" group by %s " % data
            # sql=sql+" group by %s "
            # self.sql_values.append(data)
        return sql
    def u_limit(self,data,sql):
        if data :
            sql=sql+" limit %s " % data
            # sql=sql+" limit %s "
            # self.sql_values.append(data)
        return sql
    def u_join(self,sql,union_count):
        for vkey,wvalue in self.join_tables[union_count].items():
            tableas=wvalue
            if self.join_tables_alias[union_count][vkey]:
                tableas=" %s as %s " % (wvalue,self.join_tables_alias[union_count][vkey])
            sql=sql+" %s join %s on %s " % (self.join_types[union_count][vkey],tableas,self.join_tables_on[union_count][vkey])
            # sql=sql+" %s join %s on %s "
            # self.sql_values.extend([self.join_types[union_count][vkey],tableas,self.join_tables_on[union_count][vkey]])
        return sql

    def u_clear(self):
        self.union_count=0
        self.orders={}
        self.wheres={}
        self.groups={}
        self.limits={}
        self.fields={}
        self.union_tables={}
        self.union_types={}
        self.join_types={}
        self.join_tables={}
        self.join_count=0
        self.join_tables_on={}
        self.join_tables_alias={}
        self.sql_values=[]
    def add(self,value):
        """
        @brief      Insert a row in table
        @param      table  String
        @param      value  Tuple
        """
        # col_name = self.table_cols[table][1:]
        col_name=value.keys()
        for i in range(len(col_name)):
            col_name[i]="`%s`" % col_name[i]
        # print array_join(value.values(), ',')
        # # print col_name
        # # print value.values()
        # return
        sql = "INSERT INTO %s(%s) VALUES (%s)" % (self.vtable, str(','.join(col_name)), array_join(value.values(), ','))
        Log.debug('DB -> %s' % sql)
        # print sql
        self.execute(sql)
    def save(self,value):
        col_name=value.keys()
        setfield=[]
        for key,valu in value.items():
            if valu is None:
                valu=''
            afield="%s = %s" %(key,("'"+valu+"'" if isinstance(valu,basestring)  else valu))
            setfield.append(afield)
        sql="update %s set %s " %(self.vtable,str(','.join(setfield)))
        if len(self.wheres) > 0:
            sql=self.u_where(self.wheres[0],sql)
        # print sql
        Log.debug('DB -> %s' % sql)
        sql_values=tuple(self.sql_values)
        self.u_clear()
        self.execute(sql,sql_values)
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
    def show_table_struct(self,table):
        c = self.conn.cursor()
        sql = "desc %s" % table
        Log.debug('DB -> %s' % sql)
        c.execute(sql)
        return c.fetchall()

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

    

    def get_table_column_name(self,table=False):
        """
        @brief      select all result from table
        @param      table  String
        @return     result  Array
        """
        # c = self.conn.cursor()
        sql="SELECT  COLUMN_NAME as 'field' ,DATA_TYPE as 'dataType' ,COLUMN_TYPE as 'dataTypeLen' FROM information_schema.`COLUMNS` where TABLE_SCHEMA = '%s'and TABLE_NAME = '%s'"
        sql=sql % (self.database,(table if table  else self.vtable)) 
        return self.execute(sql)
        # names = list(map(lambda x: x[0], c.description))
        

    def execute(self, sql, values=None,sqlhole=True):
        """
        @brief      execute sql commands, return result if it has
        @param      sql  String
        @param      value  Tuple
        @return     result  Array
        """
        c = self.conn.cursor()
        self.lock.acquire()
        hasReturn = sql.lstrip().upper().startswith("SELECT")

        result = []
        print values
        try:
            if values and not sqlhole:
                c.executemany(sql, values)
            else:
                c.execute(sql,values)
            # c.execute(sql,values)
            if hasReturn:
                result = c.fetchall()

        except Exception, e:
            Log.error(traceback.format_exc())
            self.conn.rollback()
        finally:
            self.lock.release()

        if hasReturn:
            return result

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
    def __del__(self):
        Log.debug('DB -> __del__')
        self.close()

        