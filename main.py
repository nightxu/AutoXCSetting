#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import getopt
import os

def __exec_cmd(cmd):
    print "exec: <" + cmd + ">\n↓↓↓";
    status = os.system(cmd)
    if (status != 0):
        print "exec fail: <" + cmd + ">"
    return status;

def __os_write_file(path,content):
    fd = open(path, 'w')
    fd.write(content)
    fd.close()  # 操作完文件后一定要记得关闭，释放内存资源

def __file_path_with_components(names):
    result = "";
    for aName in names:
        result += aName + "/";
    result = result.rstrip("/");
    return result;


# ------------ Ruby ----------
def __rb_make(dir,target,dirnames):
    rb_content = """require 'xcodeproj'

hasProjDir = -1;
hasProjName = -1;
projDir = ""
projName = ""

subdirsFlag = false
subdirs = []

puts "</rb argv******************>"
for item in ARGV

    if item == "--dir" or hasProjDir >= 0
        hasProjDir += 1;
    end
    if item == "--name" or hasProjName >= 0
        hasProjName += 1;
    end

    if hasProjDir == 1 and projDir == ""
        projDir = item;
    end

    if hasProjName == 1 and projName == ""
        projName = item;
    end

    if subdirsFlag
        subdirs.push(item);
    end
    if projDir != "" && projName != ""
        subdirsFlag = true;
    end
end


if projDir == "" || projName == "" || subdirs.size == 0
    exit;
end

puts ("subdirs  = ")
puts "["
puts subdirs;
puts "]"
puts ("dir  = " + projDir)
puts ("name = " + projName)
puts ""

puts "</rb dispose xcode project>******************"


#打开项目工程A.xcodeproj

_project_path = projDir + "/" + projName + ".xcodeproj"
project_path = File.join([projDir , (projName + ".xcodeproj")])
puts project_path;

project = Xcodeproj::Project.open(project_path)

# 1、显示所有的target
#project.targets.each do |target|
#puts target.name
#end

target = project.targets.first

# 判断是否以.开头
def _is_hidden_file(name)
   if name == "" or name[0] == "."
        return true
   end
   return false;
end

# 添加文件到target 的 group
def add__file_to_group (name,group,target)
    # 设置文件引用是否存在标识
    file_ref_mark = false
    # 获取全部的文件引用
    file_ref_list = target.source_build_phase.files_references
    # 检测需要添加的文件是否存在
    for file_ref_temp in file_ref_list
        puts file_ref_temp.path.to_s
        if file_ref_temp.path.to_s.end_with?(name) then
            file_ref_mark = true
        end
    end
    if file_ref_mark == true
        return;
    end
    file_ref = group.new_reference(name)
    ret = target.add_file_references([file_ref])
end

# 添加目录到target 的 group
def add_group (group_path,group_find_path,group,project,target)
    if File.directory?(group_path) == false             # 如果文件不是一个文件夹
        return
    end
    subdir = Dir.open(group_path)
    while subfilename = subdir.read
            next if _is_hidden_file(subfilename)              # 忽略以.开头
            subfile_path = File.join(group_path,subfilename)
            puts subfile_path
            # 遍历
            # 目录 - 递归执行 add_group
            # 文件 - 执行 add__file_to_group
            if File.directory?(subfile_path) && subfile_path.to_s.end_with?('.xcassets') == false             # 如果文件是一个文件夹
                subgroup_path = subfile_path
                subgroup_find_path = File.join(group_find_path,subfilename)
                puts ("* subgroup_path      = " + subgroup_path + " *")
                puts ("* subgroup_find_path = " + subgroup_find_path + " *")

                subgroup = project.main_group.find_subpath(subgroup_find_path, true)
                subgroup.set_source_tree('<group>')
                subgroup.set_path(subgroup_path)
                # 递归调用
                add_group(subgroup_path,subgroup_find_path,subgroup,project,target)
            else
                add__file_to_group(subfilename,group,target)
            end

    end




end

#dir_item = "Test"

for dir_item in subdirs
    group = project.main_group.find_subpath(File.join(projName,dir_item), true)
    group.set_source_tree('<group>')
    group.set_path(File.join(projDir,projName,dir_item))

    group_path = File.join(projDir,projName,dir_item)
    group_find_path = File.join(projName,dir_item)
    puts group_path
    puts group_find_path
    add_group(group_path,group_find_path,group,project,target)
end



project.save
"""
    __os_write_file("./.auto_make_xc_proj_temp.rb",rb_content);

    __rb_cmd = "ruby .auto_make_xc_proj_temp.rb --dir "+ dir + " --name " + target;
    for subdir in dirnames:
        __rb_cmd += " " + subdir
    __exec_cmd(__rb_cmd)

    os.remove("./.auto_make_xc_proj_temp.rb")

def __make_project_folder_structure(name,path):
    p_extension = "Extension-扩展"
    p_extension_category = "Category";
    p_extension_category_Foundation = "Foundation";
    p_extension_category_UIKit = "UIKit";

    p_extension_Const = "Const"
    p_extension_Macro = "Macro";
    p_extension_Networking = "Networking";
    p_extension_Tools = "Tools";

    p_main = "Main-主要"
    p_main_Base = "Base"
    p_main_Components = "Components"

    p_resources = "Resources-资源";
    p_resources_Global = "Global";
    p_resources_Images = "Images"

    p_sdk = "SDK-集成"
    p_vendor = "Vender-第三方"

    p_list = [__file_path_with_components([p_extension,p_extension_category,p_extension_category_Foundation]),
              __file_path_with_components([p_extension,p_extension_category,p_extension_category_UIKit]),
              __file_path_with_components([p_extension,p_extension_Const]),
              __file_path_with_components([p_extension,p_extension_Macro]),
              __file_path_with_components([p_extension,p_extension_Networking]),
              __file_path_with_components([p_extension,p_extension_Tools]),

              __file_path_with_components([p_main,p_main_Base]),
              __file_path_with_components([p_main,p_main_Components]),

              __file_path_with_components([p_resources, p_resources_Global]),
              __file_path_with_components([p_resources, p_resources_Images]),
              p_sdk,
              p_vendor
              ];
    for component in p_list:
        absolute_path = __file_path_with_components([path , name, component]);
        print absolute_path;
        if (os.path.exists(absolute_path)):
            continue;
        os.makedirs(absolute_path)

    __rb_make(path,name,[p_extension,p_main,p_resources,p_sdk,p_vendor])



# ------------ Pod ----------
def __alter_podfile(name,path):
    if (os.path.exists(path) == False):
        sys.exit();
    content = """# Uncomment the next line to define a global platform for your project
platform :ios, '8.0'

target '$XCPROJECT$' do
  # Uncomment the next line if you're using Swift or would like to use dynamic frameworks
  # use_frameworks!

  # Pods for $XCPROJECT$

    pod 'MLeaksFinder', '~> 1.0.0'
    pod 'AFNetworking', '~> 3.1.0'
    pod 'Masonry', '~> 1.1.0'
    pod 'IQKeyboardManager', '~> 5.0.3'
    pod 'MJExtension', '~> 3.0.13'
    pod 'UITableView+FDTemplateLayoutCell', '~> 1.6'
    pod 'SDWebImage', '~> 4.1.2'
    pod 'FLAnimatedImage', '~> 1.0.12'
    pod 'YYCategories', '~> 1.0.4'
    pod 'BlocksKit', '~> 2.2.5'
    
    # BUG 异常获取上传
    # pod 'Bugly', '~> 2.4.8'

    # 全屏滑动返回
    pod 'FDFullscreenPopGesture', '~> 1.1'
    # 网络监听
    pod 'RealReachability', '~> 1.1.9'


    # U-Share SDK UI模块（分享面板，建议添加）
    # pod 'UMengUShare/UI'

    # 集成微信(精简版0.2M)
    # pod 'UMengUShare/Social/ReducedWeChat'

    # 集成QQ(精简版0.5M)
    # pod 'UMengUShare/Social/ReducedQQ'

    # 集成新浪微博(精简版1M)
    # pod 'UMengUShare/Social/ReducedSina'

    # 集成Facebook/Messenger
    # pod 'UMengUShare/Social/Facebook'

    # 集成Twitter
    # pod 'UMengUShare/Social/Twitter'

    # 集成Line
    # pod 'UMengUShare/Social/Line'

    # 集成WhatsApp
    # pod 'UMengUShare/Social/WhatsApp'

end
"""
    content = content.replace("$XCPROJECT$",name);
    __os_write_file(path,content);


def __pod_install(name,path):

    # 切换工作目录 到 Xcode工程
    os.chdir(path)

    # pod init
    if (os.path.exists(path + "/Podfile") == False):
        status = __exec_cmd('pod init')
        if (status != 0):
            sys.exit();


    # pod install
    if (os.path.exists(path + "/" + name + ".xcworkspace") == True):
        sys.exit();#xcworkspace文件已存在,不再重新安装


    # 修改Podfile文件内容,稍后再install
    __alter_podfile(name,path + "/Podfile");


    # 安装
    status = __exec_cmd('pod install')
    if (status != 0):
        sys.exit();



    print status;





def main(argv):
    if argv.count == 0:
        sys.exit();

    try:
        opts,args = getopt.getopt(argv, "hn:p:", ["help","name=","path="]);
    except getopt.GetoptError:
        sys.exit();

    name = ''
    path = ''
    for opt,arg in opts:
        if opt in ("-h","--help"):
            print (".py -n <module name> -p <Xcode Project Path>");
            sys.exit();
        elif opt in ("-n","--name"):
            name = arg;
        elif opt in ("-p", "--path"):
            path = arg;
        else:
            sys.exit();
    if  name == "" or path == "":
        print (".py -n <module name> -p <Xcode Project Path>");
        sys.exit();

    print ("name is <" + name + ">");
    print ("path is <" + path + ">\n");


    __pod_install(name,path)
    __make_project_folder_structure(name,path);



if __name__ == '__main__':
    main(sys.argv[1:]);
