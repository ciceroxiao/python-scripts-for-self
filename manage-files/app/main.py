# coding:utf-8

import glob
import os
import shutil

from .errors import PathInvalidError


class Action:
    """操作某个路径中的内容。

    :param path: 指定的路径名称。"""
    def __init__(self, path: str):
        self.path = path

    def find_files(self, include_folders: bool = True, include_file_in_subfolders: bool = False) -> list:
        """获取当前路径（包括子文件夹）中的内容。

        :param include_folders: 返回的结果中是否包含文件夹。
        :param include_file_in_subfolders: 是否递归查找子文件夹中的文件。
        :return: 以列表形式返回文件夹中的内容。
        :raise: 如果传入的文件夹不是有效文件夹，则返回 PathInvalidError。"""
        if not os.path.isdir(self.path):
            raise PathInvalidError(f"对不起，您输入的路径 {self.path} 不是有效路径。")

        scope_of_find = "*" if not include_file_in_subfolders else "**/*"
        result = glob.glob(os.path.join(self.path, scope_of_find), recursive=include_file_in_subfolders)

        if not include_folders:
            result = [_ for _ in result if not os.path.isdir(_)]

        return result

    def search_file(self, filename: str) -> list:
        """在当前路径中搜索指定文件。

        :param filename: 搜索的文件名称。
        :return: 以列表的形式返回搜索结果。
        :raise: 如果输入的路径不是有效路径，将返回 PathInvalidError。
        """
        all_files = self.find_files(include_folders=True, include_file_in_subfolders=True)
        search_result = [_ for _ in all_files if filename in _]

        return search_result

    def search_file_with_content(self, keyword_: str) -> list:
        """在当前路径中查找含有指定关键词的相关文件。

        :param keyword_: 搜索的关键词。
        :return: 以列表形式返回搜索结果。
        :raise: 如果输入的路径不是有效路径，将返回 PathInvalidError。"""
        all_files = self.find_files(include_file_in_subfolders=True, include_folders=False)

        search_result = []
        for file in all_files:
            try:
                with open(file, "r") as f:
                    if keyword_ in f.read():
                        search_result.append(file)
            except UnicodeError:
                continue

        return search_result

    def delete_duplicate_files(self):
        """查找当前路径中的重复文件。"""
        # 基本思路是，逐个查找每个路径下的文件，并记录查找到的文件名称和大小。在后续查找过程中，如果某个文件名称已被记录，然后就对比这两个文件的大小。
        # 如果这两个文件的大小相同，那就再对比这两个文件的内容。
        # 1. 不要直接存储文件内容，因为某些文件的内容可能非常大，因而应该将文件内容转化成 hash 值（hashlib 模块）或其他数据格式。
        # 2. 某些文件可能无法直接读取内容，比如 zip 或 rar 文件，这类文件需要特殊的打开方式，因此需要做条件判断。
        # 如果这两个文件的内容相同，那就判断这两个文件是重复文件。
        # 建议将此函数分割为多个小函数：is_duplicate_files()、search_duplicate_files、delete_duplicate_files()。
        # 且，在删除前，最好询问用户是否确认删除。用户也可以传入某个参数，以避免后续的询问。
        pass

    def rename_files(self, old_: str, new_: str) -> None:
        """批量修改当前路径下的文件名称。

        :param old_: 更改前的内容。
        :param new_: 更改后的内容。
        :raise: 如果输入的路径不是有效路径，将返回 PathInvalidError。"""
        all_files = self.find_files(include_folders=True, include_file_in_subfolders=False)

        for file_old in all_files:
            file_name = os.path.split(file_old)[-1]
            file_name_new = file_name.replace(old_, new_)
            file_new = os.path.join(os.path.split(file_old)[0], file_name_new)

            shutil.move(file_old, file_new)

    def move_files(self) -> None:
        """将当前路径下的所有文件移动到当前路径下。"""
        all_files = self.find_files(include_folders=False, include_file_in_subfolders=True)
        for file in all_files:
            file_name = os.path.split(file)[-1]
            file_new_path = os.path.join(self.path, file_name)
            shutil.move(file, file_new_path)

    def delete_folders(self) -> None:
        """删除当前路径下的文件夹。"""
        folders = [_ for _ in self.find_files() if os.path.isdir(_)]
        print(*folders, sep="\n")
        if folders:
            is_continue = input("Do you want to delete these folders? y(yes) / n(no)\n").strip().lower()
        else:
            is_continue = False
        if is_continue in ("y", "yes"):
            for folder in folders:
                shutil.rmtree(folder)
