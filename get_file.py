# coding = utf-8
import requests
import time

# GitHub API 基本 URL
GITHUB_API_URL = "https://api.github.com/repos"

# 设置超时和重试参数
TIMEOUT = 10  # 超时时间，单位秒
MAX_RETRIES = 5  # 最大重试次数
WAIT_TIME = 2  # 每次重试之间的等待时间，单位秒


max_py_num = 5
current_py_num = 0

def get_github_project_files(owner, repo, current_py_num, path=""):
    """获取GitHub项目中的所有文件，保存为字典形式，递归处理文件夹"""
    url = f"{GITHUB_API_URL}/{owner}/{repo}/contents/{path}"
    print(f"正在获取路径: {url}")
    
    response = make_request_with_retries(url)
    
    if response is None:
        print("获取项目内容失败。")
        return None

    files_dict = {}
    content_list = response.json()

    for content in content_list:
        # 如果是文件夹，递归处理
        if content['type'] == 'dir':
            print(f"发现文件夹: {content['name']}，进入文件夹继续遍历")
            sub_dict, current_py_num_result = get_github_project_files(owner, repo, content['path'])
            if sub_dict:
                files_dict[content['name']] = sub_dict
            current_py_num += current_py_num_result
        # 如果是.py文件，下载并保存为字符串
        elif content['type'] == 'file' and content['name'].endswith('.py'):
            print(f"发现Python文件: {content['name']}，开始下载")
            file_content = download_file(content['download_url'])
            if file_content:
                files_dict[content['name']] = file_content
                current_py_num += 1
                
        print('now we have', current_py_num)
        if current_py_num > 5:
            break
    return files_dict, current_py_num

def download_file(url):
    """下载文件并返回为字符串"""
    print(f"正在下载文件: {url}")
    response = make_request_with_retries(url)
    if response is not None:
        print("文件下载成功")
        return response.text
    else:
        print("文件下载失败")
        return None

def make_request_with_retries(url):
    """带重试机制的请求函数"""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                return response
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"请求超时，正在进行重试 {attempt + 1}/{MAX_RETRIES} ...")
        except requests.exceptions.RequestException as e:
            print(f"请求失败，错误: {e}")
        
        # 等待一段时间后重试
        time.sleep(WAIT_TIME)
    
    print(f"在 {MAX_RETRIES} 次尝试后请求失败")
    return None

if __name__ == "__main__":
    # 输入项目的拥有者和仓库名
    owner = "stanfordnlp"
    repo = "dspy"

    # 获取所有.py文件并保存为字典
    print("开始获取项目中的所有.py文件...")
    project_files = get_github_project_files(owner, repo)
    
    if project_files:
        print("成功获取所有.py文件!")
        # 可以根据需要处理project_files字典，例如保存到本地文件系统
        # 这里暂时仅打印字典结构
        print(project_files)
    else:
        print("未找到任何文件或获取失败。")

