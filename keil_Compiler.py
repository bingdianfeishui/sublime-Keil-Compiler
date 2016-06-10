import os
import sublime, sublime_plugin
import subprocess, sys
import xml.etree.cElementTree as ET 

class KeilCompileCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		self.view.run_command("save")
		k=self.view.window().extract_variables()
		os.chdir(k["project_path"])							
		path=os.listdir(os.getcwd())
						
		for i in path:
		    if(i.find(".uvproj")>0):
        		Project=i

        
		settings = sublime.load_settings('keil_Compiler.sublime-settings')
		value = settings.get('modify_uvproj')
		if value:
			cur_file = os.path.basename(self.view.file_name())
			self.modify_uvproj(Project, cur_file)
			# print("hahahhahah")

		Command="UV4 -b {0} -o log.txt".format(Project)
		
		subprocess.call(Command,stdout=subprocess.PIPE,shell =False )

		self.view.window().open_file(k["project_path"]+"/log.txt")
		#filea = open("log.txt","r")
		#print (filea.read())
		print ("saved")

	# def modify_uvproj2(self, uvproj, cur_file):

	# 	tree = ET.parse(uvproj)     #打开xml文档    

	# 	file_node = tree.getroot().find("Targets/Target/Groups/Group/Files/File")
	# 	# print(file_node.tag, "     ",file_node.text)
	# 	print("修改前：",  file_node.find("FileName").text )
	# 	file_node.find("FileName").text = cur_file
	# 	print("修改后：",  file_node.find("FileName").text )

	# 	print("修改前：",  file_node.find("FilePath").text )
	# 	file_node.find("FilePath").text = ".\\" + cur_file
	# 	print("修改后：",  file_node.find("FilePath").text )

	# 	tree.write(uvproj)	#保存

	def modify_uvproj(self, uvproj, cur_file):
		source_str1 = "<FileName>"
		source_str2 = "<FilePath>"
		source_str3 = "<CreateHexFile>0</CreateHexFile>"
		source_str4 = "<OutputName>"
		lines=open(uvproj,'r').readlines()
		lines_len=len(lines)-1
		for i in range(lines_len):
			if source_str1 in lines[i]:
				print("old: "+lines[i])
				lines[i]= "\t\t\t  <FileName>"+cur_file+"</FileName>\n"
				print("new: "+lines[i])
				continue
			if source_str2 in lines[i]:
				print("old: "+lines[i])
				lines[i]= "\t\t\t  <FilePath>"+cur_file+"</FilePath>\n"
				print("new: "+lines[i])
				continue
			if source_str3 in lines[i]:
				lines[i]= lines[i].replace(source_str3, "<CreateHexFile>1</CreateHexFile>")
				continue
			if source_str4 in lines[i]:
				lines[i]= "\t\t\t\t\t<OutputName>"+os.path.splitext(uvproj)[0]+"</OutputName>\n"
				continue
		open(uvproj,'w').writelines(lines)
