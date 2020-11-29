import os
import shutil

pic_dir_path = r'E:\c1\c2\a1'
dir_list = os.listdir(pic_dir_path)

name = 1
for dir_path in dir_list:
    dir_abs_path = pic_dir_path + '\\' + dir_path
    print("第一层，条码层：", dir_abs_path)
    for dir_dir_path in os.listdir(dir_abs_path):
        dir_org_path = dir_abs_path + '\\' + dir_dir_path
        print("第二层，商户层：", dir_org_path)
        for dir_pic_path in os.listdir(dir_org_path):
            dir_pic_abs_path = dir_org_path + '\\' + dir_pic_path
            name += 1
            new_name = dir_org_path + '\\' + str(name) + '.' + dir_pic_abs_path.split(".")[1]
            os.rename(dir_pic_abs_path, new_name)
            print(new_name, '到了', dir_abs_path)
            shutil.move(new_name, dir_abs_path)
        print("删除文件夹完成！", dir_org_path)
        shutil.rmtree(dir_org_path)
