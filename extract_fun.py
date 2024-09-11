import re
import copy

def get_indent_level(line):
    """计算行的缩进级别"""  
    # 匹配字符串中是否只包含空格、\t、\n、\r,如果是，返回None，否则返回缩进值
    if re.fullmatch(r'[\s\t\n\r]*', line) is not None:
        return None
    else:
        return len(line) - len(line.lstrip())

def extract_functions_and_comments(code_str):
    lines = code_str
    code_list = []  # 保存函数和类的列表
    comment_list = []  # 保存注释的列表

    # 正则匹配函数和类的定义
    func_pattern = re.compile(r'^\s*(def|class)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(?.*?\)?:')

    # 初始化变量
    current_hierarchy = []  # 用于追踪当前的层级（类、函数的索引）
    func_stack = []  # 保存函数和它的缩进级别 (index, indent_level)
    func_counter = 0  # 函数计数器
    inside_func = False
    func_start_line = [0]
    current_func = []
    current_indent = 0
    indent_gap = 4
    first_indent = True
    
    current_func.append([])


        
        
    
    # 生成函数层级
    current_hierarchy =  [0]
    func_stack.append((func_counter, -4))  # 将当前函数加入栈
    
    
    
    
    for i, line in enumerate(lines):
        stripped_line = line.strip()

        is_comment = True
        
        # 处理单行注释
        if stripped_line.startswith('#'):
            comment_lines = [stripped_line]
            comment_start = i + 1
            comment_end = i + 1
            # 检查连续的单行注释
            while i + 1 < len(lines) and lines[i + 1].strip().startswith('#'):
                i += 1
                comment_lines.append(lines[i].strip())
                comment_end = i + 1
            comment_str = '\n'.join(comment_lines)
            comment_list.append((comment_str, (comment_start, comment_end), tuple(current_hierarchy)))

        # 处理多行注释
        elif stripped_line.startswith('"""') or stripped_line.startswith("'''"):
            comment_lines = [stripped_line]
            comment_start = i + 1
            comment_end = i + 1
            closing_pattern = '"""' if stripped_line.startswith('"""') else "'''"
            while not lines[i].strip().endswith(closing_pattern):
                i += 1
                comment_lines.append(lines[i].strip())
                comment_end = i + 1
            comment_str = '\n'.join(comment_lines)
            comment_list.append((comment_str, (comment_start, comment_end), tuple(current_hierarchy)))
        else:
            is_comment = False

        if is_comment:
            continue
        # 检查是否为函数或类定义
        if func_pattern.match(line):
            func_counter += 1  # 新函数发现，函数计数器加1
            indent_level = get_indent_level(line)

            if indent_level > 0:
                if first_indent:
                    assert indent_level in [2,4], 'wrong indent level %d' %indent_level
                    indent_gap = indent_level
                    first_indent = False 
            
            # 新函数并非开启一个新层级
            
            if func_stack and func_stack[-1][1] >= indent_level:
                while func_stack and func_stack[-1][1] >= indent_level:
                    func_stack.pop()
                    code_list.append(('\n'.join(current_func[-1]), (func_start_line[-1], i), copy.deepcopy(current_hierarchy)))
                    current_func.pop()
                    func_start_line.pop()
                    current_hierarchy.pop()
            elif func_stack:
                assert indent_level - func_stack[-1][1] == indent_gap, 'indent of line %d is wrong' % i
            elif not first_indent:
                #print(func_stack)
                assert indent_level == indent_gap, 'indent of line %d: %s is wrong' % (i, line)
            
            current_func.append([])
            func_start_line.append(i+1)

                
                
            
            # 生成函数层级
            current_hierarchy = [item[0] for item in func_stack] + [func_counter]
            func_stack.append((func_counter, indent_level))  # 将当前函数加入栈
            print(current_hierarchy)
            
            # 如果已经在一个函数中，保存当前函数
            
            
            # 记录新函数的开始
            inside_func = True

            for current_func_ele in current_func:
                current_func_ele.append(line)
        
        elif inside_func:
            indent_level = get_indent_level(line)
            
            if indent_level is not None and func_stack and func_stack[-1][1] >= indent_level:
                print('act', func_stack, indent_level)
                while func_stack and func_stack[-1][1] >= indent_level:
                    func_stack.pop()
                    code_list.append(('\n'.join(current_func[-1]), (func_start_line[-1], i), copy.deepcopy(current_hierarchy)))
                    current_func.pop()
                    func_start_line.pop()
                    current_hierarchy.pop()
                    
            for current_func_ele in current_func:
                current_func_ele.append(line)
        


    # 如果在循环结束时还有一个函数未保存
    if current_func:
        while current_func:
            code_list.append(('\n'.join(current_func[-1]), (func_start_line[-1], len(lines)), copy.deepcopy(current_hierarchy)))
            current_func.pop()
            func_start_line.pop()
            current_hierarchy.pop()


    
    return code_list, comment_list





def process_comment_list(code_list, comment_list):
    code_comment_lists = []
    for comment, line_index, fun_index in comment_list:
        code = code_list[fun_index[-1]][0]
        code_comment_lists.append([code, comment])
    return code_comment_lists









'''
# 测试代码
code_str = '''
'''
# Copyright 2023 llmware

# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You
# may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.

"""The setup module implements the init process.

The module implements the Setup class, which has two static methods - load_sample_files and load_sample_voice_files.

These methods create the necessary directory if they do not exist and downloads the sample files from an llmware-
 maintained AWS S3 instance.

"""


import shutil
import os
from llmware.resources import CloudBucketManager
from llmware.configs import LLMWareConfig

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=LLMWareConfig().get_logging_level_by_module(__name__))


class Setup:

    """Implements the download of sample files from an AWS S3 bucket.

    ``Setup`` implements the download of sample files from an AWS S3 bucket. Currently, there are samples
    from eight domains:

    - AgreementsLarge (~80 sample contracts)
    - Agreements (~15 sample employment agreements)
    - UN-Resolutions-500 (500 United Nations Resolutions over ~2 years)
    - Invoices (~40 invoice sample documents)
    - FinDocs (~15 financial annual reports, earnings and 10Ks)
    - AWS-Transcribe (~5 AWS-transcribe JSON files)
    - SmallLibrary (~10 mixed document types for quick testing)
    - Images (~3 images for OCR processing)

    The sample files are updated continously. By calling ``Setup().load_sample_files(over_write=True)``
    you will get the newest version of the sample files.

    The sample files were prepared by LLMWare from public domain materials, or invented bespoke.
    If you have any concerns about Personally Identifiable Information (PII), or the suitability of any material
    we included, please contact us, e.g. either by raising an issue on GitHub or sending an E-Mail.
    We reserve the right to withdraw documents at any time.

    Examples
    ----------
    >>> import os
    >>> from llmware.setup import Setup
    >>> sample_files_path = Setup().load_sample_files()
    >>> sample_files_path
    '/home/user/llmware_data/sample_files'
    >>> os.listdir(sample_files_path)
    ['AWS-Transcribe', '.DS_Store', 'SmallLibrary', 'UN-Resolutions-500', 'Invoices', 'Images', 'AgreementsLarge', 'Agreements', 'FinDocs']

    If you have called the function before but want to get the newest updates to the sample files, or you simply
    want to get the newest sample files, you simply set ``over_write=True``.
    >>> sample_files_path = Setup().load_sample_files(over_write=True)
    """
    @staticmethod
    def load_sample_files(over_write=False):

        """ Downloads sample document files from non-restricted AWS S3 bucket. """

        if not os.path.exists(LLMWareConfig.get_llmware_path()):
            LLMWareConfig.setup_llmware_workspace()

        # not configurable - will pull into /sample_files under llmware_path
        sample_files_path = os.path.join(LLMWareConfig.get_llmware_path(), "sample_files")

        if not os.path.exists(sample_files_path):
            os.makedirs(sample_files_path,exist_ok=True)
        else:
            if not over_write:
                logger.info(f"Setup - sample_files path already exists - \{sample_files_path\}")
                return sample_files_path

        # pull from sample files bucket
        logger.info(f"Setup - sample_files - downloading requested sample files from AWS S3 bucket - may take a minute.")

        bucket_name = LLMWareConfig().get_config("llmware_sample_files_bucket")
        remote_zip = bucket_name + ".zip"
        local_zip = os.path.join(sample_files_path, bucket_name + ".zip")
            
        CloudBucketManager().pull_file_from_public_s3(remote_zip, local_zip, bucket_name)
        shutil.unpack_archive(local_zip, sample_files_path, "zip")
        os.remove(local_zip)

        return sample_files_path

    @staticmethod
    def load_voice_sample_files(over_write=False, small_only=True):

        """ Downloads sample wav files from non-restricted AWS S3 bucket. """

        if not os.path.exists(LLMWareConfig.get_llmware_path()):
            LLMWareConfig.setup_llmware_workspace()

        # not configurable - will pull into /sample_files under llmware_path
        if not small_only:
            sample_files_path = os.path.join(LLMWareConfig.get_llmware_path(), "voice_sample_files")
        else:
            sample_files_path = os.path.join(LLMWareConfig.get_llmware_path(), "voice_sample_files_small")

        if not os.path.exists(sample_files_path):
            os.makedirs(sample_files_path, exist_ok=True)
        else:
            if not over_write:
                logger.info(f"Setup - voice_sample_files path already exists - \{sample_files_path\}")
                return sample_files_path

        # pull from sample files bucket
        bucket_name = LLMWareConfig().get_config("llmware_sample_files_bucket")

        if small_only:
            folder_name = "voice_small"
        else:
            folder_name = "voice_all"

        logger.info("Setup - sample_voice_files - downloading requested sample files from AW3 S3 bucket - "
                    "may take a minute.")

        remote_zip = folder_name + ".zip"
        local_zip = os.path.join(sample_files_path, bucket_name + ".zip")

        CloudBucketManager().pull_file_from_public_s3(remote_zip, local_zip, bucket_name)
        shutil.unpack_archive(local_zip, sample_files_path, "zip")
        os.remove(local_zip)

        return sample_files_path

    @staticmethod
    def load_selected_sample_files(sample_folder="microsoft_ir", over_write=False):

        """ Downloads sample wav files from non-restricted AWS S3 bucket. """
        
        def little_util(sampl1, sampl2):
            # compare larger
            if sample1 > 1:
                return sampl2
            else:
                return sampl1

        if not os.path.exists(LLMWareConfig.get_llmware_path()):
            LLMWareConfig.setup_llmware_workspace()

        # not configurable - will pull into /sample_files under llmware_path
        sample_files_path = os.path.join(LLMWareConfig.get_llmware_path(), sample_folder)

        if not os.path.exists(sample_files_path):
            os.makedirs(sample_files_path, exist_ok=True)
        else:
            if not over_write:
                logger.info(f"Setup - sample_files selected path already exists - \{sample_files_path\}")
                return sample_files_path

        # pull from sample files bucket
        bucket_name = LLMWareConfig().get_config("llmware_sample_files_bucket")

        folder_name = sample_folder

        logger.info("Setup - selected sample files - downloading requested sample files from AW3 S3 bucket - "
                    "may take a minute.")

        remote_zip = folder_name + ".zip"
        local_zip = os.path.join(sample_files_path, bucket_name + ".zip")

        CloudBucketManager().pull_file_from_public_s3(remote_zip, local_zip, bucket_name)
        shutil.unpack_archive(local_zip, sample_files_path, "zip")
        os.remove(local_zip)

        return sample_files_path
'''
'''
A, B = extract_functions_and_comments(code_str)
print("Functions (A):")
for aa in A:
    print(aa[0])
    print(aa[1:])
    print('---------------------------------------------------------')
    print()
print("Comments (B):")
for bb in B:
    print(bb)
'''