# Sublime Keil Compiler
**Compile the Keil project in Sublime Text. Let the ugly keil editor go away.**

**在Sublime Text 3 及 Keil uVision 4下测试通过，其余版本未测试。**
Tested with Sublime Text 3 & Keil uVision 4. Didn't test the other version.


Keil的自带编辑器很难用，所以我利用Sublime Text作为Keil uVision的外部编辑器来学习MCS51单片机，但每次编辑完成后都需要关闭sublime回到Keil中进行编译，不是很方便，要是sublime能直接编译C51文件就好了。网上有一些用sublime调用C51的编译器、连接器等进行编译的方法，但设置麻烦，而且相对的不太容易传递编译参数。幸运的是我在github上发现了[stu0219/sublime-Keil-Compiler](https://github.com/stu0219/sublime-Keil-Compiler)，直接在sublime中以命令行的方式调用Keil uVision进行编译。但由于我学习C51单片机时，经常需要在Keil的Project中切换.c文件，每次都要到Keil中设置，所以我fork了这个项目，添加了编译前更改Keil Project文件的功能。这样，我只需要在Sublime中新建一个c文件，保存到项目文件夹，然后直接编译就行了，全部在Sublime中进行，方便太多了~~

The Keil own editor is difficult to use, so I use Sublime Text as the Keil uVision external editor for learning 8051 MCU. But when finishing editting each time, I must return to the Keil to compile it, that is really not convenient. Some blog on the Internet says calling the call C51 compiler, linker exe in Sublime when compiling, but the configuration is too difficult for me , a sublime & 8051 & python & program newbie, and I found it hardly to transform compiling arguments. Fortunately I found [stu0219/sublime-Keil-Compiler](https://github.com/stu0219/sublime-Keil-Compiler) on GitHub, calling the Keil directly by command line when compiling. But I often need to switch the c file of the Project of Keil when learning 8051 MCU, and I need to return the Keil again. so I forked this project, added the function changing Keil Project file befor the compiling. Now, I can create a new c file in Sublime, save it to the project folder and directly compile it, all work is in the Sublime , so convenient ~ ~

##安装
1. 安装Keil软件，然后在系统的环境变量`Path`中添加你的Keil路径，如`C:\Keil\UV4`。
2. 复制所有文件到`Data\Packages\`文件夹下，当然你可以自己建一个子文件夹来保存。关于Data文件夹的位置，请参见[The *Data* Directory](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory)。
3. 打开Keil软件新建一个项目，保存。
4. 打开Sublime Text，将Keil项目所在文件夹添加到项目，并保存项目，以便生成一个`.sublime-project`文件。

5. 新建一个`.c`文件，并保存到项目文件夹中，按`Alt+C`或菜单`Tools->Keil Compiler`编译，编译完成后自动打开`log.txt`文件。查看项目文件夹，`.hex`文件是不是已经生成了呢~


##Install
1. Install Keil uVision, then add the install path to the environment variables `Path`, ex: `C:\Keil\UV4`.
2. Copy all files to the `Data\Packages\`, of course, you can create a sub-folder. The location of `Data` folder is [here](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory).
3. Open Keil uVision to create a project, then save it.
4. Open Sublime Text, add the Keil Project folder to the sublime project, and save the project for creating a `.sublime-project` file.
5. Create a new `.c` file, input some code, save it to the sublime project folder. Compile it by `Alt+C` or `Tools->Keil Compiler`. The `log.txt` will be open when completed. Now, see your project folder, the `.hex` file is already here. Download it to your MCU. Enjoy it~

----
*pls forgive my poor english.*
