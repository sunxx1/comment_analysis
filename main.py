import get_file 
import ana_com 
import extract_fun 
import os



directory = 'StoryDiffusion'

for root, dirs, files in os.walk(directory):
    for file in files:
            # 获取文件的完整路径
        full_path = os.path.join(root, file)

        if full_path.endswith('.py'):
            print('process', full_path)
            fid = open(full_path, 'r')
            value = fid.readlines()
            code_list, comment_list = extract_fun.extract_functions_and_comments(value)
            code_comment_lists = extract_fun.process_comment_list(code_list, comment_list)
            print('Original code')
            for value_ele in value:
                print(value_ele)
            for code, comment in code_comment_lists:
                print()
                print('-----------------------------------')
                print('Original comment')
                print(comment)
                ana_com.comprehensive_ana(code, comment)
            break
    

