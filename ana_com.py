# coding = utf-8
import requests
import json
import time
# 配置信息
endpoint = "https://oh-ai-openai-scu.openai.azure.com/"
api_key = "76c10d695bf349ab8026e7c940e6bd26"
deployment_id = "gpt-35-turbo"
api_version = "2023-05-15"

# 请求头
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

def ask_openai_question(question):
    # 请求体
    data = {
        "model": "gpt-35-turbo",
        "messages": [
            {"role": "system", "content": "You are a highly experienced software engineer with extensive knowledge in writing and reviewing code. You specialize in multiple programming languages, understand best practices for code quality, and are skilled at providing clear, concise, and constructive feedback on both the logic and structure of code. Your expertise spans debugging, optimizing algorithms, and ensuring that code adheres to industry standards. You are focused on maintaining high code quality, writing clean, efficient, and maintainable code, and helping others improve their code skills."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 5000
    }
    

    
    # 构造请求URL
    url = f"{endpoint}openai/deployments/{deployment_id}/chat/completions?api-version={api_version}"
    
    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    


    # 检查响应状态
    while response.status_code != 200:
        print("Hit rate limit. Waiting and retrying...")
        time.sleep(20)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
    result = response.json()
    # 从响应中提取回答
    return result['choices'][0]['message']['content'].strip()


        
    
    
def check_problem(code, comments, task_discription, examples):
    #code = '\n'.join(code_l)
    question = task_discription
    for example_ind, example in enumerate(examples):
        question = question +('\nExample %d\n' %example_ind) + example
    question = question + "\ninput:\n"+ "code: " + code
    if isinstance(comments, list):
        for comment_ind, comment in enumerate(comments):
            question = question +  ("\ncomment%d: " % comment_ind) + comment
    else:
        question = question + "\ncomment: " + comments
    
    answer = ask_openai_question(question)

# 输出回答
    print("Answer:", answer)
    return answer

def get_relative(code, comments):
    
    task_discription = "You are given two inputs: \n" + \
    "1. Code (denoted as 'A'). \n" +\
    "2. Comment (denoted as 'B').\n\n" +\
    "Your task is to: \n" +\
    "1. Determine if code A and comment B are related. Answer strictly with 'yes' or 'no'.\n" +\
    "2. Provide a reason for your answer in this format: \"Reason: because the comment mentions [specific feature] which aligns with [specific logic] in the code.\"\n" +\
    "3. Break down comment B into its individual descriptions, such as parameter explanations or logical descriptions of specific functions. \n" +\
    "For each description in comment B, list the corresponding code part from code A. \n" +\
    "If the relevant code spans multiple lines, select 1-3 lines at random."
    
    examples = [
        "Code (A):\n" +\
        "def calculate_area(radius: float) -> float:\n" +\
        "    pi = 3.14159\n" +\
        "    if radius > 0:\n" +\
        "        return pi * radius ** 2\n" +\
        "    else:\n" +\
        "        return 0\n\n" +\
        "Comment (B):\n" +\
        "Calculate the area of a circle given its radius.\n" +\
        "Args:\n" +\
        "    radius: The radius of the circle. Must be a positive number.\n" +\
        "Returns:\n" +\
        "    The area of the circle as a float. Returns 0 if the radius is non-positive.\n\n" +\
        "Output:\n" +\
        "1. Yes\n" +\
        "2. Reason: because the comment explains the function `calculate_area`, which matches the logic of calculating a circle's area and handling non-positive radius values in the code.\n" +\
        "3. Breakdown of the comment:\n" +\
        "    - \"radius: The radius of the circle. Must be a positive number.\": Corresponds to `radius: float` and `if radius > 0:`\n" +\
        "    - \"Returns: The area of the circle as a float. Returns 0 if the radius is non-positive.\": Corresponds to `return pi * radius ** 2` and `return 0`\n\n"
        , 
        "Code (A):\n" +\
        "public int addNumbers(int a, int b) {\n" +\
        "    return a + b;\n" +\
        "}\n\n" +\
        "Comment (B):\n" +\
        "This function calculates the factorial of a given number.\n" +\
        "Args:\n" +\
        "    num: The number to calculate the factorial for.\n" +\
        "Returns:\n" +\
        "    The factorial of the number as an integer.\n\n" +\
        "Output:\n" +\
        "1. No\n" +\
        "2. Reason: because the comment describes a factorial calculation function, whereas the code performs a simple addition operation. The two do not align.\n" +\
        "3. Breakdown of the comment:\n" +\
        "    - \"num: The number to calculate the factorial for.\": No corresponding parameter or logic found in the code.\n" +\
        "    - \"Returns: The factorial of the number as an integer.\": This functionality is not present in the code."
        ,     
        "Code (A):\n" +\
        "def calculate_discount(price: float, discount: float) -> float:\n" +\
        "    if discount > 0.5:\n" +\
        "        discount = 0.5\n" +\
        "    final_price = price * (1 - discount)\n" +\
        "    return final_price\n\n" +\
        "Comment (B):\n" +\
        "The function limits the discount to a maximum of 50%. If a discount greater than 50% is provided, it will be reduced to 50%.\n\n" +\
        "Output:\n" +\
        "1. Yes\n" +\
        "2. Reason: because the comment explains the logic of limiting the discount to 50%, which matches the code's logic that implements this check.\n" +\
        "3. Breakdown of the comment:\n" +\
        "    - \"limits the discount to a maximum of 50%\": Corresponds to `if discount > 0.5: discount = 0.5`\n" +\
        "    - \"If a discount greater than 50% is provided, it will be reduced to 50%\": Corresponds to `discount = 0.5`"
        ,
        "Code (A):\n" +\
        "def reverse_string(s: str) -> str:\n" +\
        "    return s[::-1]\n\n" +\
        "Comment (B):\n" +\
        "This function sorts the input string in alphabetical order.\n\n" +\
        "Output:\n" +\
        "1. No\n" +\
        "2. Reason: because the comment describes sorting the string alphabetically, while the code actually reverses the string, so they are not related.\n" +\
        "3. Breakdown of the comment:\n" +\
        "    - \"sorts the input string in alphabetical order\": No corresponding logic for sorting found in the code.\n" +\
        "    - \"input string\": Refers to `s: str`, but this does not involve sorting.\n"
    ]
    
    answer = check_problem(code, comments, task_discription, examples)
    return answer

def get_verbose(code, comments):
    
    task_discription = "You are given two inputs:\n" + \
    "1. Code (denoted as 'A').\n" + \
    "2. Comment (denoted as 'B').\n\n" + \
    "Your task is to:\n" + \
    "Task One: Evaluate whether comment B is too verbose or overly detailed in explaining the corresponding part of code A.Answer strictly with 'yes' or 'no'.\n" + \
    "Specifically, check if the comment provides excessive details that make it difficult to understand and if it fails to focus on the core message.\n" + \
    "Note: All the explains in the comments which explain the meaning of multiple function parameters shold be remained and should not be considered verbos. These explanations are useful for understanding the code, even if they are long.\n" + \
    "However, if a comment simply repeats or slightly modifies the function parameter names without adding useful information, those comments should be considered verbose and can be removed.\n" + \
    "Task Two: If the comment is indeed too verbose, provide a simplified version of the comment that retains the original meaning while being clearer and more concise. Else, outputs None"
    
    examples = [
        "Code (A):\n" + \
        "def test_fun(batch_size, lr_rate, optimizer_type_select):\n\n" + \
        "Comment (B):\n" + \
        "batch_size: the number of sample in a batch\n" + \
        "lr_rate: the initial learning rate,\n" + \
        "optimizer_type_select: optimizer type select\n\n" + \
        "Output:\n" + \
        "1. Yes\n" + \
        "2. Modified Comment: 'the number of sample in a batch, lr_rate: the initial learning rate'\n\n\n" + \
        "Note: for optimizer_type_select: optimizer type select, we consider it verbose and remove it, for batch_size: the number of sample in a batch and lr_rate: the initial learning rate, we do not consider it verbose and remain it."
        ,
        "Code (A):\n" + \
        "def add_numbers(a, b):\n" + \
        "    return a + b\n\n" + \
        "Comment (B):\n" + \
        "# This function takes two input parameters: a and b, which can be integers or floating-point numbers.\n" + \
        "# It then proceeds to add these two numbers together using Python's built-in addition operator, which works for both integers and floats.\n" + \
        "# After performing the addition, it returns the result, which will be either an integer or a float, depending on the input types.\n\n" + \
        "Output:\n" + \
        "1. Yes\n" + \
        "2. Modified Comment: # Adds two numbers and returns the result."
        ,
        "Code (A):\n" + \
        "def reverse_string(s):\n" + \
        "    return s[::-1]\n\n" + \
        "Comment (B):\n" + \
        "# Reverses the input string.\n\n" + \
        "Output:\n" + \
        "1. No\n" + \
        "2. None\n"
    ]
    
    answer = check_problem(code, comments, task_discription, examples)
    return answer   


def get_vague(code, comments):
    task_discription = "You are given two inputs:\n" + \
    "1. Code (denoted as 'A').\n" + \
    "2. Comment (denoted as 'B').\n\n" + \
    "Your task is to:\n" + \
    "1. Determine if comment B describing the functionality of code A is too vague or unclear.\n" + \
    "Specifically, check if the comment lacks sufficient information, making it hard to understand. Answer strictly with 'yes' or 'no'.\n" + \
    "2. If the comment is vague or unclear, provide a more detailed and clearer version of the comment that fully explains the code's functionality. Else, outputs None."
    
    examples = [
        "Code (A):\n" + \
        "def process_data(data):\n" + \
        "    result = []\n" + \
        "    for item in data:\n" + \
        "        if isinstance(item, int) and item > 10:\n" + \
        "            result.append(item * 2)\n" + \
        "        elif isinstance(item, str):\n" + \
        "            result.append(item.lower())\n" + \
        "        else:\n" + \
        "            result.append(item)\n" + \
        "    return result\n\n" + \
        "Comment (B):\n" + \
        "# Process the data\n\n" + \
        "Output:\n" + \
        "1. Yes\n" + \
        "2. Modified Comment: \n" + \
        "# Processes the data by doubling integers greater than 10, converting strings to lowercase, \n" + \
        "# and appending other items unchanged to the result list."
        ,
        "Code (A):\n" + \
        "def calculate_statistics(numbers):\n" + \
        "    total = sum(numbers)\n" + \
        "    count = len(numbers)\n" + \
        "    mean = total / count\n" + \
        "    variance = sum((x - mean) ** 2 for x in numbers) / count\n" + \
        "    std_dev = variance ** 0.5\n" + \
        "    return {\"mean\": mean, \"variance\": variance, \"std_dev\": std_dev}\n\n" + \
        "Comment (B):\n" + \
        "# Calculates the mean, variance, and standard deviation of a list of numbers.\n\n" + \
        "Output:\n" + \
        "1. No\n" + \
        "2. None"
        ,
        "Code (A):\n" + \
        "def process_orders(order_list):\n" + \
        "    processed_orders = []\n" + \
        "    total_revenue = 0\n" + \
        "    for order in order_list:\n" + \
        "        if order['status'] == 'completed':\n" + \
        "            processed_orders.append(order)\n" + \
        "            total_revenue += order['price'] * order['quantity']\n" + \
        "        elif order['status'] == 'pending':\n" + \
        "            order['follow_up'] = True\n" + \
        "        else:\n" + \
        "            continue\n" + \
        "    return {\n" + \
        "        'processed_orders': processed_orders,\n" + \
        "        'total_revenue': total_revenue,\n" + \
        "        'order_count': len(processed_orders)\n" + \
        "    }\n\n" + \
        "def generate_summary(orders):\n" + \
        "    summary = {\n" + \
        "        'completed_orders': 0,\n" + \
        "        'pending_orders': 0,\n" + \
        "        'canceled_orders': 0\n" + \
        "    }\n" + \
        "    for order in orders:\n" + \
        "        if order['status'] == 'completed':\n" + \
        "            summary['completed_orders'] += 1\n" + \
        "        elif order['status'] == 'pending':\n" + \
        "            summary['pending_orders'] += 1\n" + \
        "        elif order['status'] == 'canceled':\n" + \
        "            summary['canceled_orders'] += 1\n" + \
        "    return summary\n\n" + \
        "Comment (B):\n" + \
        "# Process the orders and generate summary\n\n" + \
        "Output:\n" + \
        "1. Yes\n" + \
        "2. Modified Comment: \n" + \
        "# Processes the orders by filtering completed orders and calculating total revenue.\n" + \
        "# It also flags pending orders for follow-up and skips other orders.\n" + \
        "# Additionally, a summary is generated with counts of completed, pending, and canceled orders."
        ,
        "Code (A):\n" + \
        "def manage_inventory(inventory, transactions):\n" + \
        "    for transaction in transactions:\n" + \
        "        product_id = transaction['product_id']\n" + \
        "        if product_id in inventory:\n" + \
        "            if transaction['type'] == 'purchase':\n" + \
        "                inventory[product_id]['quantity'] += transaction['quantity']\n" + \
        "                inventory[product_id]['total_value'] += transaction['quantity'] * transaction['price_per_unit']\n" + \
        "            elif transaction['type'] == 'sale' and inventory[product_id]['quantity'] >= transaction['quantity']:\n" + \
        "                inventory[product_id]['quantity'] -= transaction['quantity']\n" + \
        "                inventory[product_id]['total_value'] -= transaction['quantity'] * transaction['price_per_unit']\n" + \
        "            else:\n" + \
        "                continue\n" + \
        "        else:\n" + \
        "            if transaction['type'] == 'purchase':\n" + \
        "                inventory[product_id] = {\n" + \
        "                    'quantity': transaction['quantity'],\n" + \
        "                    'total_value': transaction['quantity'] * transaction['price_per_unit']\n" + \
        "                }\n" + \
        "    return inventory\n\n" + \
        "def generate_inventory_report(inventory):\n" + \
        "    report = []\n" + \
        "    for product_id, details in inventory.items():\n" + \
        "        report.append({\n" + \
        "            'product_id': product_id,\n" + \
        "            'quantity': details['quantity'],\n" + \
        "            'total_value': details['total_value']\n" + \
        "        })\n" + \
        "    return report\n\n" + \
        "Comment (B):\n" + \
        "# Manages inventory by processing purchase and sale transactions, and generates a report\n" + \
        "# summarizing the quantity and total value of each product in stock.\n\n" + \
        "Output:\n" + \
        "1. No\n" + \
        "2. None"
    ]
    
    answer = check_problem(code, comments, task_discription, examples)
    return answer 


def get_unprofessional(code, comments):
    task_discription = "You are given two inputs:\n" + \
    "1. Code (denoted as 'A').\n" + \
    "2. Comment (denoted as 'B').\n\n" + \
    "Your task is to:\n" + \
    "1. Determine if comment B uses inappropriate or unprofessional language, such as slang, overly casual phrases, or unprofessional terminology. Answer strictly with 'yes' or 'no'.\n" + \
    "2. If the answer is 'yes', provide a modified version of the comment (Modified Comment) that replaces the inappropriate language with professional terms. If the answer is 'no', output 'None'."

    examples = [
        "Code (A):\n" + \
        "def process_data(data):\n" + \
        "    cleaned_data = []\n" + \
        "    for item in data:\n" + \
        "        if isinstance(item, str):\n" + \
        "            cleaned_data.append(item.strip().lower())\n" + \
        "        elif isinstance(item, int):\n" + \
        "            cleaned_data.append(item)\n" + \
        "        else:\n" + \
        "            continue\n" + \
        "    return cleaned_data\n\n" + \
        "def analyze_data(cleaned_data):\n" + \
        "    result = []\n" + \
        "    for entry in cleaned_data:\n" + \
        "        if isinstance(entry, str) and len(entry) > 5:\n" + \
        "            result.append(entry)\n" + \
        "        elif isinstance(entry, int) and entry > 10:\n" + \
        "            result.append(entry * 2)\n" + \
        "    return result\n\n" + \
        "Comment (B):\n" + \
        "# We will clean the bad boys in the data and process only the cool samples.\n\n" + \
        "Output:\n" + \
        "1. Yes\n" + \
        "2. Modified Comment: \n" + \
        "# Clean the invalid or improperly formatted data entries and process the valid samples."
        ,
        "Code (A):\n" + \
        "def generate_report(sales_data):\n" + \
        "    report = {}\n" + \
        "    for month, data in sales_data.items():\n" + \
        "        total_sales = sum(data['sales'])\n" + \
        "        total_returns = sum(data['returns'])\n" + \
        "        net_sales = total_sales - total_returns\n" + \
        "        report[month] = {\n" + \
        "            'total_sales': total_sales,\n" + \
        "            'total_returns': total_returns,\n" + \
        "            'net_sales': net_sales\n" + \
        "        }\n" + \
        "    return report\n\n" + \
        "def summarize_report(report):\n" + \
        "    summary = {'total_sales': 0, 'total_returns': 0, 'net_sales': 0}\n" + \
        "    for month, data in report.items():\n" + \
        "        summary['total_sales'] += data['total_sales']\n" + \
        "        summary['total_returns'] += data['total_returns']\n" + \
        "        summary['net_sales'] += data['net_sales']\n" + \
        "    return summary\n\n" + \
        "Comment (B):\n" + \
        "# Generates a detailed monthly report of sales and returns, and provides a summary of total sales.\n\n" + \
        "Output:\n" + \
        "1. No\n" + \
        "2. None."
    ]
    
    answer = check_problem(code, comments, task_discription, examples)
    return answer 


def get_redundant(code, comments):
    
    if not isinstance(comments, list):
        comments = [comments]
    
    task_discription = "You are given two inputs:\n" + \
    "1. Code (denoted as 'A').\n" + \
    "2. Multiple comments (denoted as 'B').\n\n" + \
    "Your task is to:\n" + \
    "1. Determine if there are multiple comments in B that redundantly describe the same aspect of code A.\n" + \
    "If there are redundant comments, keep the information in the earlier comment and remove the redundant part in the later comment.\n" + \
    "Answer strictly with 'yes' or 'no'.\n" + \
    "2. If the answer is 'yes', provide the modified comments (Modified Comment) with redundant descriptions removed from the later comments.\n" + \
    "If the answer is 'no', output 'None'."
    examples = [
        "Code (A):\n" + \
        "def process_image(image):\n" + \
        "    # Step 1: Load the image from disk\n" + \
        "    img = load_image(image)\n" + \
        "    # Step 2: Convert image to grayscale\n" + \
        "    gray_img = convert_to_grayscale(img)\n" + \
        "    # Step 3: Normalize the grayscale image\n" + \
        "    normalized_img = normalize_image(gray_img)\n" + \
        "    # Step 4: Apply Gaussian blur\n" + \
        "    blurred_img = apply_gaussian_blur(normalized_img)\n" + \
        "    return blurred_img\n\n" + \
        "Comments (B):\n" + \
        "Comment1: # Step 1: Load the image from disk\n" + \
        "Comment2: # Step 2: Convert image to grayscale\n" + \
        "Comment3: # Step 3: Normalize the grayscale image\n" + \
        "Comment4: # Step 4: Apply Gaussian blur\n\n" + \
        "Output:\n" + \
        "1. No\n" + \
        "2. None."
        ,
        "Code (A):\n" + \
        "def process_image(image):\n" + \
        "    # Step 1: Normalize the image and convert to HSV\n" + \
        "    normalized_img = normalize_image(image)\n" + \
        "    hsv_img = convert_to_hsv(normalized_img)\n" + \
        "    # Step 2: Convert to HSV and perform data augmentation\n" + \
        "    augmented_img = augment_data(hsv_img)\n" + \
        "    # Step 3: Perform edge detection\n" + \
        "    edge_img = detect_edges(augmented_img)\n" + \
        "    # Step 4: Save the processed image\n" + \
        "    save_image(edge_img)\n" + \
        "    return edge_img\n\n" + \
        "Comment (B):\n" + \
        "# Comment1: Step 1: Normalize the image and convert to HSV\n" + \
        "# Comment2: Step 2: Convert to HSV and perform data augmentation\n" + \
        "# Comment3: Step 3: Perform edge detection\n" + \
        "# Comment4: Step 4: Save the processed image\n\n" + \
        "Output:\n" + \
        "1. Yes\n" + \
        "2. Modified Comment: \n" + \
        "# Comment1: Step 1: Normalize the image and convert to HSV\n" + \
        "# Comment2: Step 2: Perform data augmentation\n" + \
        "# Comment3: Step 3: Perform edge detection\n" + \
        "# Comment4: Step 4: Save the processed image."
    ]
    
    answer = check_problem(code, comments, task_discription, examples)
    return answer 



def comprehensive_ana(code, comment):

    verbose_result = get_verbose(code, comment)
    is_verbose_str = verbose_result.split('1.')[1].split('\n')[0]
    is_verbose = ('Yes' in is_verbose_str) or ('YES' in is_verbose_str)
    
    
    relateive_result = get_relative(code, comment)
    is_relative_str = relateive_result.split('1.')[1].split('\n')[0]
    is_relative = ('Yes' in is_relative_str) or ('YES' in is_relative_str)
    
    unprofessional_result = get_unprofessional(code, comment)
    is_unprofessional_str = unprofessional_result.split('1.')[1].split('\n')[0]
    is_unprofessional = ('Yes' in is_unprofessional_str) or ('YES' in is_unprofessional_str)
    
    vague_result = get_vague(code, comment)
    is_vague_str = vague_result.split('1.')[1].split('\n')[0]
    is_vague = ('Yes' in is_vague_str) or ('YES' in is_vague_str)
    
    prompt = "You are given three inputs:\n" + \
        "1. Code (denoted as 'A').\n" + \
        "2. Comment (denoted as 'B').\n" + \
        "3. Four conclusions about comment B:\n" + \
        "    - C1: Does comment B relate to code A? (Yes or No)\n" + \
        "    - C2: Is comment B too verbose or overly detailed? (Yes or No)\n" + \
        "    - C3: Is comment B vague or unclear? (Yes or No)\n" + \
        "    - C4: Does comment B use unprofessional or inappropriate language? (Yes or No)\n\n" + \
        "Your task is to:\n" + \
        "1. Evaluate comment B based on the four conclusions (C1 to C4).\n" + \
        "2. If the comment should be changed, provide the final modified comment that resolves any issues found in the conclusions With The Start Words: 'FINAL COMMENT:', making sure the final comment is:\n" + \
        "    - Related to the code (if C1 is Yes)\n" + \
        "    - Concise (if C2 is Yes, remove any verbose parts)\n" + \
        "    - Clear and specific (if C3 is Yes, improve clarity)\n" + \
        "    - Professional and appropriate (if C4 is Yes, replace unprofessional language)\n" + \
        "3. If no changes are needed, return the original comment With The Start Words: 'FINAL COMMENT:'.\n\n" + \
        "INPUT:\n" + \
        "Code: \n" + code + "\nComment:\n " + comment + \
        "\nIs it Relative:\n" + relateive_result + \
        "\nIs it Verbose:\n" + verbose_result + \
        "\nIs it Vague:\n" + vague_result + \
        "\nIs it Unprofessional:\n" + unprofessional_result
        
    answer = ask_openai_question(prompt)

    
    print("Final Answer:", answer)
    if 'FINAL COMMENT' in answer:
        final_comment = answer.split('FINAL COMMENT')[1]
    else:
        final_comment = 'Error: '+ answer
    
    print('Is the Comment Relative: ' + is_relative_str)
    print('Is the Comment Verbose: ' + is_verbose_str)
    print('Is the Comment Vague: ' + is_vague_str)
    print('Is the Comment Unprofessional: ' + is_unprofessional_str)
    if is_relative and (not is_verbose) and (not is_vague)  and (not is_unprofessional):
        print('No need to modified')
    else:
        print('Modified Comment', final_comment)
    
    
    return answer
        
    



'''
code = """
def create_faiss_index(
    emb_dim: int,
    n_objects: int,
    n_probe: int = 10,
    max_gpu_devices: int = 0,
    encode_residuals: bool = True,
    in_list_dist_type: str = 'L2',
    centroid_dist_type: str = 'L2',
) -> Index:
    if n_objects < 20_000:
        index = _get_brute_index(emb_dim=emb_dim, dist_type=in_list_dist_type)
    else:
        index = _get_ivf_index(
            emb_dim=emb_dim,
            n_objects=n_objects,
            in_list_dist_type=in_list_dist_type,
            centroid_dist_type=centroid_dist_type,
            encode_residuals=encode_residuals,
        )

    index.nprobe = n_probe

    num_devices, is_gpu = determine_devices(max_gpu_devices)
    if is_gpu:
        cloner_options = faiss.GpuMultipleClonerOptions()
        cloner_options.shard = True
        index = faiss.index_cpu_to_gpus_list(index, cloner_options, list(range(num_devices)))

    return index
"""

comments1 = """
Create IVF index (with IP or L2 dist), without adding data and training
Args:
    emb_dim: emb dim
    n_objects: size of a trainset for index. Used to determine optimal type
        of index and its settings (will use bruteforce if `n_objects` is less than 20_000).
    n_probe: number of closest IVF-clusters to check for neighbours.
        Doesn't affect bruteforce-based search.
    max_gpu_devices: max gpu devices
    encode_residuals: whether or not compute the fucking happy thing. The residual vector is 
        the difference between a vector and the reconstruction that can be
        kick out from its representation in the index.
    in_list_dist_type: type of distance to calculate similarities within one IVF.
        Can be `IP` (for inner product) or `L2` distance. Case insensitive.
    centroid_dist_type: type of distance to calculate similarities between a query 
        and cluster centroids. Can be `IP` (for inner product) or `L2` distance.
        Case insensitive.
Returns: untrained FAISS-index,
"""

comments2 = """
Create IVF index (with IP or L2 dist), without adding data and training
Returns: untrained FAISS-index,
"""

comprehensive_ana(code, comments1)
'''