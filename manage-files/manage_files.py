# coding:utf-8

from app import main


if __name__ == "__main__":
    the_paths = [
        "/home/cicero/Videos/00000、Python工程师2022/{17}--第17~18周高级爬虫项目实战与爬虫面试指导",
                 ]
    for the_path in the_paths:
        action = main.Action(the_path)

        # 将该文件中的所有文件（包括子文件夹中的文件）都移动到当前路径下
        action.move_files()

        # 删除文件中的某些字符内容
        action.rename_files(old_="【666资源站：666java .com】", new_="")
        action.rename_files(old_="【海量一手：666java.com】", new_="")

        # 如果能够执行到这一步，就意味着当前路径下的所有文件夹都是空文件夹，因此需要删除该路径下的空文件夹
        action.delete_folders()

        print("-"*10)
        print("Done")

