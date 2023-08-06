# -*- coding: UTF-8 -*-
# 创建时间：2018年3月9日21:29:09
# 创建人：	Dekiven_PC


import os
import sys
import platform

'''
	常用工具函数
'''

def isPython3():
	'''判断python版本是否是3.x'''
	return sys.version_info >= (3,0)

def isFunc(func):
	'''判断对象是否是函数'''
	return hasattr(func,'__call__')
	# return callable(func)

def getPlatform():
	'''获取python运行平台'''
	return platform.system()

def isWindows():
	'''判断是否是win32平台'''
	return getPlatform() == 'Windows'

def isLinux():
	'''判断是否是linux平台'''
	return getPlatform() == 'Linux'

def getDesktopPath():
	'''获取桌面的路径，只支持win32'''
	if isWindows():
		if isPython3():
			import winreg			# 内置模块，获取windows注册表
		else:
			import _winreg as winreg
		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
		return winreg.QueryValueEx(key, "Desktop")[0]
	else:
		# TODO: Linux
		return ""

def addTempPathForOs(path):
	'''添加path到系统的PATH环境变量中，暂时只支持win32'''
	if isWindows():
		os.environ['PATH']+= ';' +path

def addTempPathForPy(path):
	'''添加path到python运行环境的PATH环境变量中'''
	sys.path.append(path)

def getMainCwd():
	'''获取入口脚本的文件夹路径'''
	return os.path.split(sys.argv[0])[0]


def ZipFolder(folder, zipPath = None, suffixs = '.*', skipFiles = ()):
	'''压缩文件夹
	folder:待压缩的文件夹
	zipPath:压缩文件存储路径，默认为文件绝对夹路径加上后缀'.zip'
	suffixs:参与压缩的文件格式后缀，默认为'.*'，表示所有文件都参与压缩，多个后缀用英文逗号（','）隔开，如：'.zip,.txt'
	skipFiles:跳过压缩的文件列表（list或tuple）,在文件夹中的绝对路径
	'''
	if not isinstance(folder, str) :
		print('error:\tfolder [%s] is not a string!'%(str(folder)))
		return
	if not os.path.isabs(folder) :
		folder = os.path.join(pyDir, folder)
	folderLen = len(folder)
	fileInfos = []
	suffixs = suffixs == '.*' and suffixs or str(suffixs).lower().split(',')

	# list解析操作
	skip = [l.strip() for l in skipFiles]
	if os.path.exists(folder) and os.path.isdir(folder) :
		for _dir, folders, files in os.walk(folder) :
			for f in files :
				suffix = os.path.splitext(f)
				suffix = str(suffix[-1]).lower()
				p = os.path.join(_dir, f)
				# 获取zip文件夹内的路径，去掉前面的/
				absP = p[folderLen+1:]
				if (suffixs == '.*' or suffix in suffixs) and (not absP in skip):
					fileInfos.append((p, absP))
					skip.append(absP)
		if len(fileInfos) > 0 :
			if zipPath is None :
				zipPath = folder + '.zip'
			dirName = os.path.dirname(zipPath)
			if not os.path.exists(dirName) :
				os.makedirs(dirName)
			zipF = zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED)
			# print(password)
			# zipF.setpassword(password)
			for f, af in fileInfos :
				zipF.write(f, af)
			zipF.close()
			print('zip [%s] finished! Total files: %d'%(zipPath, len(fileInfos)))
			return fileInfos
		else :
			print('no files need to zip!')

	else :
		print('error:\tfolder [%s] do not exists!'%(folder))


def Singleton(cls, *args, **kwds):
	'''单例修饰符函数，参考见：
	python 单例：http://ghostfromheaven.iteye.com/blog/1562618
	python @修饰符：http://blog.csdn.net/lainegates/article/details/8166764
	'''
	instances = {}
	def _singleton():
		if cls not in instances:
			instances[cls] = cls(*args, **kwds)
		return instances[cls]
	return _singleton