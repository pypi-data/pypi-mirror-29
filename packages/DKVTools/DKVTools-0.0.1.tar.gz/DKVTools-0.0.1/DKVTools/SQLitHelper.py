# -*- coding:utf-8 -*- 
# Date: 2017-07-06 10:05:49
# Author: dekiven

# 参考：
# Python: Enum枚举的实现：http://www.cnblogs.com/codingmylife/archive/2013/05/31/3110656.html
# type函数创建新的类型（传入3个参数）： http://www.cnblogs.com/sesshoumaru/p/6129966.html
# SQLite - Python： http://www.runoob.com/sqlite/sqlite-python.html

import os
import sqlite3

curDir = os.getcwd()

def EnumDef(*sequential, **named):
	'''
	创建枚举类型，可以通过该类型的reverse_mapping属性从值反向获取enum名
	详见参考：
		Python: Enum枚举的实现：http://www.cnblogs.com/codingmylife/archive/2013/05/31/3110656.html
	# 测试代码
	EnumTest = EnumDef('Zero', One = 1, Two = 2)
	print(EnumTest.Zero)
	print(EnumTest.One)
	print(EnumTest.reverse_mapping[2])
	'''
	enums = dict(zip(sequential, range(len(sequential))), **named)
	reverse = dict((value, key) for key, value in enums.iteritems())
	enums['reverse_mapping'] = reverse
	return type('Enum', (), enums)



class TableKeyAtt(object):
	'''
		数据库字段属性
		一般数据采用的固定的静态数据类型，而SQLite采用的是动态数据类型，会根据存入值自动判断。SQLite具有以下五种数据类型：

		1.NULL：空值。
		2.INTEGER：带符号的整型，具体取决有存入数字的范围大小。
		3.REAL：浮点数字，存储为8-byte IEEE浮点数。
		4.TEXT：字符串文本。
		5.BLOB：二进制对象。

		但实际上，sqlite3也接受如下的数据类型：
		smallint 16 位元的整数。
		interger 32 位元的整数。
		decimal(p,s) p 精确值和 s 大小的十进位整数，精确值p是指全部有几个数(digits)大小值，s是指小数点後有几位数。如果没有特别指定，则系统会设为 p=5; s=0 。
		float  32位元的实数。
		double  64位元的实数。
		char(n)  n 长度的字串，n不能超过 254。
		varchar(n) 长度不固定且其最大长度为 n 的字串，n不能超过 4000。
		graphic(n) 和 char(n) 一样，不过其单位是两个字元 double-bytes， n不能超过127。这个形态是为了支援两个字元长度的字体，例如中文字。
		vargraphic(n) 可变长度且其最大长度为 n 的双字元字串，n不能超过 2000
		date  包含了 年份、月份、日期。
		time  包含了 小时、分钟、秒。
		timestamp 包含了 年、月、日、时、分、秒、千分之一秒。
		datetime 包含日期时间格式，必须写成'2010-08-05'不能写为'2010-8-5'，否则在读取时会产生错误！

		sqlite中char、varchar、text和nchar、nvarchar、ntext的区别
		1、CHAR。CHAR存储定长数据很方便，CHAR字段上的索引效率级高，比如定义char(10)，那么不论你存储的数据是否达到了10个字节，都要占去10个字节的空间,不足的自动用空格填充。
		2、VARCHAR。存储变长数据，但存储效率没有CHAR高。如果一个字段可能的值是不固定长度的，我们只知道它不可能超过10个字符，把它定义为 VARCHAR(10)是最合算的。VARCHAR类型的实际长度是它的值的实际长度+1。为什么“+1”呢？这一个字节用于保存实际使用了多大的长度。从空间上考虑，用varchar合适；从效率上考虑，用char合适，关键是根据实际情况找到权衡点。
		3、TEXT。text存储可变长度的非Unicode数据，最大长度为2^31-1(2,147,483,647)个字符。
		4、NCHAR、NVARCHAR、NTEXT。这三种从名字上看比前面三种多了个“N”。它表示存储的是Unicode数据类型的字符。我们知道字符中，英文字符只需要一个字节存储就足够了，但汉字众多，需要两个字节存储，英文与汉字同时存在时容易造成混乱，Unicode字符集就是为了解决字符集这种不兼容的问题而产生的，它所有的字符都用两个字节表示，即英文字符也是用两个字节表示。nchar、nvarchar的长度是在1到4000之间。和char、varchar比较起来，nchar、nvarchar则最多存储4000个字符，不论是英文还是汉字；而char、varchar最多能存储8000个英文，4000个汉字。可以看出使用nchar、nvarchar数据类型时不用担心输入的字符是英文还是汉字，较为方便，但在存储英文时数量上有些损失。
		所以一般来说，如果含有中文字符，用nchar/nvarchar，如果纯英文和数字，用char/varchar
	'''
	def __init__(self, keyName, typeStr, typeLen = 1, isDefautNull = True, isPrimaryKey = False):
		self.keyName = keyName
		self.typeStr = typeStr
		self.typeLen = typeLen
		self.isDefautNull = isDefautNull
		self.isPrimaryKey = isPrimaryKey

	def getSqlStr(self):
		keyName = self.keyName
		typeStr = self.typeStr
		typeLen = (self.typeLen > 1) and '(%d)'%(typeLen) or ''
		isDefautNull = self.isDefautNull and 'DEFAULT NULL' or 'NOT NULL'
		isPrimaryKey = self.isPrimaryKey and 'PRIMARY KEY' or ''

		return '%s %s%s %s %s' % (keyName, typeStr, typeLen, isPrimaryKey, isDefautNull)

	def getIsPrimaryKey():
		return self.isPrimaryKey

class SQLitHelper(object):
	'''
		SQLitHelper
	'''
	def __init__(self, dbPath):
		super(SQLitHelper, self).__init__()
		self.conn = self.getConn(dbPath)
		self.cursor = self.getCursor()
		self.printDebug = False

	def getConn(self, path):
		if not os.path.isabs(path) :
			path = os.path.join(curDir, path)

		conn = sqlite3.connect(path)
		if (os.path.exists(path) and os.path.isfile(path)):
			return conn
		else :
			conn = None
			conn = sqlite3.connect(':memery:')

	def getCursor(self, conn = None):		
		conn = conn or self.conn
		if conn is not None :
			return conn.cursor()
		else :
			# 如果传入的conn为空则返回在内存数据库中链接对象的游标
			self.conn = self.getConn('')
			return self.conn.cursor()

	def closeAll(self, conn = None, cursor = None):
		'''
		关闭数据库游标和数据库链接
		'''
		conn = conn or self.conn
		cursor = cursor or self.cursor

		try:
			if cursor is not None :
				cursor.close()
		finally:
			if conn is not None :
				conn.close()

	def createTable(self, tableName, keys, conn = None):
		'''
		创建数据表
		'''
		conn = conn or self.conn
		if isinstance(tableName, str) and tableName != '' :
			sql = 'CREATE TABLE %s \n(' % (tableName)
			count = 0
			if (isinstance(keys, list) or isinstance(keys, tuple)) :
				for key in keys :
					if isinstance(key, TableKeyAtt):
						sql = sql + key.getSqlStr() + ',\n'
						count += 1
				if count > 0 :
					sql = sql[:-2] + ');'
				else :
					sql = None
			elif isinstance(keys, str) and keys != '' :
				sql = keys
			else :
				sql = None

			if sql is not None :
				self.execute(sql, conn = conn)

	def dropTable(self, tableName, commit = True, conn = None):
		'''
		删除数据表
		'''
		if isinstance(tableName, str) and tableName != '' :
			sql = 'DROP TABLE IF EXISTS %s' % (tableName)
			self.execute(sql, conn = conn, commit = commit)

	def insert(self, tableName, data, commit = True, conn = None):
		'''
		添加数据
		'''
		if isinstance(data, list) or isinstance(data, tuple) and isinstance(tableName, str) and tableName != '':
			dataLen = len(data)
			sql = 'INSERT INTO %s values (%s);' % (tableName, ('?,'*dataLen)[:-1])
			self.execute(sql, data, conn, commit)

	def select(self, tableName, keyNames, where = None, conn = None ):
		'''
		查询数据
		'''
		if isinstance(keyNames, list) or isinstance(keyNames, tuple) and isinstance(tableName, str) and tableName != '':
			sql = None
			if len(keyNames) > 0 :
				sql = 'SELECT %s from %s;' % ((', '.join(keyNames)), tableName)
			else :
				sql = 'SELECT %s from %s;' % ('*', tableName)

			if sql is not None :
				return self.execute(sql, conn = conn, commit = False)

		return None

	def update(self, tableName, dataDic, where = None, commit = True, conn = None):
		'''
		更新数据
		'''
		if isinstance(dataDic, dict) and isinstance(tableName, str) and tableName != '':
			data = []
			setStr = ''
			for k, v in dataDic.items():
				if isinstance(v, str):
					v = '"' + v + '"'
				setStr = setStr + '{} = {}, '.format(k, v)
			if len(setStr) > 2 :
				setStr = setStr[:-2]
			else :
				setStr = ''

			whereStr = ''
			if isinstance(where, str) and where != '' :
				whereStr = 'where ' + where

			sql = 'UPDATE %s set %s %s' % (tableName, setStr, whereStr)

			self.execute(sql, conn = conn, commit = commit)

	def delete(self, tableName, where = None, commit = True, conn = None):
		'''
		删除数据
		'''
		if isinstance(tableName, str) and tableName != '':
			whereStr = ''
			if isinstance(where, str) and where != '':
				whereStr ='where ' + where

			sql = 'DELETE FROM %s %s' % (tableName, whereStr)

			self.execute(sql, conn = conn, commit = commit)

	def commit(self, conn = None):
		'''
		提交
		'''
		conn = conn or self.conn

		conn.commit()

	def rollback(self, conn = None):
		'''
		回滚自上一次调用 commit() 以来对数据库所做的更改。
		'''
		conn = conn or self.conn

		conn.rollback()

	def execute(self, sql, data = None, conn = None, commit = True):
		'''
		运行sql语句
		'''
		conn = conn or self.conn
		if isinstance(sql, str) and sql != '' :
			cursor = None
			if self.printDebug:
				print('execute, sql:\n\t"%s", \ndata:\n\t%s, \ncommit:\n\t%s'%(sql, str(data), str(commit)))
			try:
				if data is not None :
					cursor = conn.execute(sql, data)
				else :
					cursor = conn.execute(sql)

			except Exception as e:
				print(e)
			finally:
				if commit :
					conn.commit()
				return cursor 
		return None

	def setPrintLog(self, value):
		self.printDebug = value

def test():
	print('test beging')

	test = SQLitHelper('test.db')

	# keys = (
	# 	TableKeyAtt('id', 'INTEGER', isPrimaryKey = True),
	# 	TableKeyAtt('name', 'TEXT'),
	# 	TableKeyAtt('age', 'INTEGER'),
	# 	TableKeyAtt('score', 'REAL'),
	# )

	# test.createTable('test', keys)

	# # 添加数据
	# test.insert('test', (1, 'name1', 18, 60))
	# test.insert('test', (2, 'name2', 19, 60))
	# test.insert('test', (3, 'name3', 20, 60.2))
	# test.insert('test', (4, 'name4', 21, 60.3))

	# # 更新数据
	# test.update('test', {'age':99, 'name':'ha1hah'}, 'id = 1')

	# # 删除一条数据
	# test.delete('test', 'id = 2')

	# # 删除整个表所有数据
	# test.delete('test')

	# # 查询数据
	# cursor = test.select('test', ('id', 'age' , 'name'))
	# data = cursor.fetchone()
	# while data is not None:
	# 	print(data)
	# 	data = cursor.fetchone()

	# 删除数据表
	# test.dropTable('test')

	# test.insert('test', (1, 'name1', 18, 60))

	test.closeAll()


if __name__ == '__main__':
	test()


