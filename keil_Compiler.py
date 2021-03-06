import os, shutil, re
import sublime, sublime_plugin
import subprocess, sys
import xml.dom.minidom as minidom

class KeilCompileCommand(sublime_plugin.TextCommand):
	def run(self,edit,modify):

		k=self.view.window().extract_variables()
		global projPath
		projPath = k["project_path"]
		os.chdir(projPath)
		path=os.listdir(os.getcwd())

		for i in path:
			if(i.find(".uvproj")>0):
				keilProj=os.path.join(projPath,i)

		# settings = sublime.load_settings('keil_Compiler.sublime-settings')
		# value = settings.get('modify_uvproj')
		value = bool(modify)

		if value:
			print("修改uvproj.")
			fileList = self.getOpenFiles()
			if not self.modify_uvproj(keilProj, fileList):
				print ("任务终止。")
				return
		else:
			print("不修改uvproj.")

		Command="UV4 -b {0} -o log.txt".format(keilProj)

		subprocess.call(Command,stdout=subprocess.PIPE,shell =False )
		self.view.window().open_file(projPath+"/log.txt")

		print ("完成。")

	def modify_uvproj(self, uvproj, fileList):

		if len(fileList) == 0:
			print("已打开的文件中没有匹配的文件类型。")
			return False

		# uvproj = "D:\lesson7.uvproj"
		# print("UV4 proj: %s"%uvproj)
		dom = minidom.parse(uvproj)

		#更改hex生成选项
		hexFile=dom.getElementsByTagName("CreateHexFile")
		if hexFile[0].childNodes[0].nodeValue == '0':
			hexFile[0].childNodes[0].nodeValue = '1'

		print("CreateHexFile: %s"%hexFile[0].childNodes[0].nodeValue)

		#删除原来的File节点
		oldFiles = dom.getElementsByTagName("FileName")
		for f in oldFiles:
			print("删除旧文件信息: %s"%f.childNodes[0].nodeValue)
			f.parentNode.parentNode.removeChild(f.parentNode);


		root = dom.getElementsByTagName("Files")
		if not root:
			root = dom.getElementsByTagName("Group")
			newfiles = dom.createElement("Files")
			for gp in root:
				gp.appendChild(newfiles)
		root = dom.getElementsByTagName("Files")
		for f in fileList:
			print('添加文件节点信息: %s'%f)
			newfile = dom.createElement("File")

			fileNameNode = dom.createElement("FileName")
			fileName = dom.createTextNode(os.path.basename(f)) #(f.lstrip("./"))
			fileNameNode.appendChild(fileName)

			fileTypeNode = dom.createElement("FileType")
			t=f[f.rfind('.'):].upper()
			if t==".C":
				ftype = "1"
			elif t==".A51":
				ftype="2"

			fileType = dom.createTextNode( ftype)
			fileTypeNode.appendChild(fileType)

			filePathNode = dom.createElement("FilePath")
			filePath = dom.createTextNode(f)	# filePath = dom.createTextNode("./"+f)
			filePathNode.appendChild(filePath)

			newfile.appendChild(fileNameNode)
			newfile.appendChild(fileTypeNode)
			newfile.appendChild(filePathNode)

			root[0].appendChild(newfile)

		domcopy = self.beautifulFormat(dom.cloneNode(True))

		uvBak = uvproj + ".uvbak"
		shutil.copy(uvproj, uvBak)

		fileHandle = open(uvproj,'w',encoding='utf-8')

		try:

			domcopy.writexml(fileHandle, addindent='  ', newl='\n', encoding = 'utf-8')
			fileHandle.close()
			print('修改.uvproj项目文件成功。')

			# 调试用
			# i=1
			# print("打印File信息：")
			# for node in root[0].childNodes:
			# 	if node.nodeType == node.ELEMENT_NODE:
			# 		print("File Name %d is %s"%(i,node.getElementsByTagName("FileName")[0].childNodes[0].nodeValue))
			# 		print("File Type %d is %s"%(i,node.getElementsByTagName("FileType")[0].childNodes[0].nodeValue))
			# 		print("File Path %d is %s\n"%(i,node.getElementsByTagName("FilePath")[0].childNodes[0].nodeValue))
			# 		i+=1
		except:
			fileHandle.close()
			os.remove(uvproj)
			os.rename(uvBak, uvproj)
		finally:
			fileHandle.close()
			os.remove(uvBak)

		return True
	def getOpenFiles(self):
		files=[]
		settings = sublime.load_settings('keil_Compiler.sublime-settings')
		value = settings.get('fileFilter')

		for v in sublime.active_window().views():
			if v and v.file_name():
				fileName=v.file_name()
				# print("Opened File: %s  %s"%(fileName,os.path.splitext(fileName)[1]))
				if value:
					if fileName.endswith(".dump"):
						fileName = fileName[:-5]
					if (fileName[fileName.rfind('.'):].upper() in value):#if the extension in 'fileFilter' setting
						#files.append(os.path.basename(fileName))	#only add the basename
						self.view.run_command("save")	#保存符合的文件

						f=fileName.replace(projPath,'.').strip() #构造子目录的相对路径
						f=fileName.replace(os.path.dirname(projPath),'..').strip() #构造父目录下文件夹的相对路径

						# pattern = r"[a-zA-Z]:"
						# if re.search(pattern,f):
						# 	print(f)
						# 	f=f[2:]
						# 	print(f)
						files.append(f)	#can deal with file in other folders
						# files.append(fileName)
		return files

	def beautifulFormat(self, xmlDomObject):
		# '''美化xml格式
		strXml=""
		for line in xmlDomObject.toprettyxml(indent=' '*2).split('\n'):
			strXml += line.strip()

		return minidom.parseString(strXml)
