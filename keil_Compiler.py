import os, shutil
import sublime, sublime_plugin
import subprocess, sys
import xml.dom.minidom as minidom

class KeilCompileCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		self.view.run_command("save")
		k=self.view.window().extract_variables()
		curPath = k["project_path"]
		os.chdir(curPath)							
		path=os.listdir(os.getcwd())
						
		for i in path:
			if(i.find(".uvproj")>0):
				keilProj=os.path.join(curPath,i)

		settings = sublime.load_settings('keil_Compiler.sublime-settings')
		value = settings.get('modify_uvproj')

		if value:
			fileList = self.getOpenFiles()
			if not self.modify_uvproj(keilProj, fileList):
				print ("任务终止。")
				return


		Command="UV4 -b {0} -o log.txt".format(keilProj)
		
		subprocess.call(Command,stdout=subprocess.PIPE,shell =False )
		self.view.window().open_file(k["project_path"]+"/log.txt")
		
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
		if oldFiles:
			for f in oldFiles:
				print("删除旧文件信息: %s"%f.childNodes[0].nodeValue)
				f.parentNode.parentNode.removeChild(f.parentNode); 

		root = dom.getElementsByTagName("Files")
		if not root:
			group = dom.getElementsByTagName("Group")
			files = dom.createElement("Files")
			for gp in group:
				gp.appendChild(files)
			root = dom.getElementsByTagName("Files")

		for f in fileList:
			print('添加文件节点信息: %s'%f)
			newfile = dom.createElement("File")

			fileNameNode = dom.createElement("FileName")
			fileName = dom.createTextNode(f)
			fileNameNode.appendChild(fileName)

			fileTypeNode = dom.createElement("FileType")
			fileType = dom.createTextNode("1")
			fileTypeNode.appendChild(fileType)

			filePathNode = dom.createElement("FilePath")
			filePath = dom.createTextNode("./"+f)
			filePathNode.appendChild(filePath)
			
			newfile.appendChild(fileNameNode)
			newfile.appendChild(fileTypeNode)
			newfile.appendChild(filePathNode)

			root[0].appendChild(newfile)

		domcopy = self.beautifulFormat(dom.cloneNode(True))

		uvBak = uvproj + ".uvbak"
		shutil.copy(uvproj, uvBak)

		fileHandle = open(uvproj,'w') 

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
			print('修改.uvproj文件失败，文件已恢复到更改前的状态。')
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
				if value and (os.path.splitext(fileName)[1] in value):	
					files.append(os.path.basename(fileName))
		return files

	def beautifulFormat(self, xmlDomObject):
		# '''美化xml格式
		strXml=""
		for line in xmlDomObject.toprettyxml(indent=' '*2).split('\n'):
			strXml += line.strip()

		return minidom.parseString(strXml)