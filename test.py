#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SonarQube 程式碼品質測試檔案
這個檔案故意包含各種程式碼品質問題，用來測試 SonarQube 的檢測能力
每個問題都會被 SonarQube 標記出來，證明它正在正確運作
"""

# 問題 1: 未使用的 import（SonarQube 會檢測到多餘的 import）
import os
import sys
import datetime
import json
import random
import time  # 這個 import 沒有被使用，SonarQube 會標記它

# 問題 2: 全域變數使用不當（違反程式設計最佳實踐）
global_counter = 0  # 全域變數應該謹慎使用
MAGIC_NUMBER = 42   # 魔術數字，應該有更清楚的命名

# 問題 3: 函數複雜度過高（包含太多分支邏輯）
def complex_function_with_many_branches(input_value, flag1, flag2, flag3):
    """
    這個函數故意設計得很複雜，包含多個分支
    SonarQube 會檢測到認知複雜度過高的問題
    """
    global global_counter  # 使用全域變數，SonarQube 會標記
    
    # 問題 4: 深層嵌套的 if 語句（降低可讀性）
    if input_value > 0:
        if flag1:
            if flag2:
                if flag3:
                    global_counter += 1
                    if input_value > 100:
                        return "Very high value"
                    else:
                        return "High value"
                else:
                    return "Medium value"
            else:
                return "Low value"
        else:
            return "Negative flag"
    else:
        return "Non-positive value"

# 問題 5: 函數命名不清楚且參數過多
def func(a, b, c, d, e, f, g, h):  # 參數太多，函數名不具描述性
    """參數過多的函數，SonarQube 會建議重構"""
    result = a + b + c + d + e + f + g + h
    return result

# 問題 6: 重複的程式碼（Code Duplication）
def calculate_circle_area_method1(radius):
    """計算圓形面積的第一種方法"""
    pi = 3.14159  # 硬編碼的 π 值
    area = pi * radius * radius
    print(f"圓形面積是: {area}")  # 重複的列印邏輯
    return area

def calculate_circle_area_method2(radius):
    """計算圓形面積的第二種方法 - 基本上是重複的程式碼"""
    pi = 3.14159  # 同樣硬編碼的 π 值
    area = pi * radius * radius
    print(f"圓形面積是: {area}")  # 重複的列印邏輯
    return area

# 問題 7: 異常處理不當
def risky_operation(filename):
    """
    這個函數展示了不良的異常處理模式
    SonarQube 會檢測到潛在的安全和穩定性問題
    """
    try:
        # 問題 7a: 過於寬泛的異常捕獲
        file_content = open(filename, 'r').read()  # 沒有正確關閉檔案
        data = json.loads(file_content)
        return data
    except:  # 捕獲所有異常，這是不好的做法
        pass  # 靜默忽略錯誤，可能隱藏重要問題

# 問題 8: 安全性問題（潛在的程式碼注入風險）
def unsafe_eval_function(user_input):
    """
    這個函數展示了安全性風險
    SonarQube 會標記 eval() 的使用為安全漏洞
    """
    # 危險：直接使用 eval() 處理用戶輸入
    result = eval(user_input)  # SonarQube 會標記這為高風險
    return result

# 問題 9: 效能問題和不必要的迴圈
def inefficient_list_operations():
    """展示效能問題的函數"""
    # 問題 9a: 在迴圈中重複創建列表
    result = []
    for i in range(1000):
        temp_list = []  # 在迴圈中重複創建，效能不佳
        temp_list.append(i)
        result.extend(temp_list)
    
    # 問題 9b: 不必要的列表複製
    final_result = result[:]  # 不必要的複製操作
    return final_result

# 問題 10: 死代碼（永遠不會執行的程式碼）
def function_with_dead_code():
    """包含死代碼的函數"""
    value = 10
    if value > 5:
        return "大於5"
        print("這行程式碼永遠不會執行")  # 死代碼，SonarQube 會檢測到
    else:
        return "小於等於5"

# 問題 11: 類別設計問題
class PoorlyDesignedClass:
    """
    這個類別展示了多種設計問題
    SonarQube 會檢測到各種物件導向的問題
    """
    
    def __init__(self, name, age, address, phone, email, occupation):
        # 問題 11a: 建構函數參數過多
        self.name = name
        self.age = age
        self.address = address
        self.phone = phone
        self.email = email
        self.occupation = occupation
        self.unused_attribute = "從未被使用"  # 未使用的屬性
    
    # 問題 11b: 方法過長且做太多事情
    def do_everything(self):
        """這個方法違反了單一責任原則"""
        print(f"姓名: {self.name}")
        print(f"年齡: {self.age}")
        
        # 在同一個方法中處理完全不相關的邏輯
        if self.age > 18:
            print("成年人")
        
        # 又處理另一個不相關的邏輯
        current_time = datetime.datetime.now()
        print(f"當前時間: {current_time}")
        
        # 還有更多不相關的處理
        random_number = random.randint(1, 100)
        print(f"隨機數字: {random_number}")

# 問題 12: 變數命名問題
def confusing_variable_names():
    """展示不清楚的變數命名"""
    a = 10  # 不具描述性的變數名
    b = 20  # 同樣不清楚
    temp = a + b  # 'temp' 是模糊的命名
    data = temp * 2  # 'data' 太通用
    result = data  # 沒有增加任何價值的賦值
    return result

# 問題 13: 字串格式化問題
def string_formatting_issues():
    """展示字串處理的不良做法"""
    name = "張三"
    age = 25
    
    # 問題 13a: 使用過時的字串格式化方法
    message1 = "姓名是 %s，年齡是 %d" % (name, age)  # 過時的 % 格式化
    
    # 問題 13b: 字串連接效能問題
    message2 = "Hello " + "World " + "from " + "Python"  # 多次字串連接
    
    return message1, message2

# 問題 14: 主程式區塊缺少保護
# 應該使用 if __name__ == "__main__": 來保護主程式邏輯
print("這行程式碼在 import 時也會執行，這可能不是想要的行為")

# 測試所有有問題的函數
if __name__ == "__main__":
    print("開始測試 SonarQube 檢測能力...")
    
    # 呼叫包含問題的函數
    complex_function_with_many_branches(50, True, True, False)
    func(1, 2, 3, 4, 5, 6, 7, 8)
    calculate_circle_area_method1(5)
    calculate_circle_area_method2(3)
    
    # 這些呼叫可能會產生錯誤，但我們用來測試
    try:
        risky_operation("nonexistent_file.json")
        inefficient_list_operations()
        function_with_dead_code()
        
        poor_object = PoorlyDesignedClass("測試", 30, "台北", "0912345678", "test@email.com", "工程師")
        poor_object.do_everything()
        
        confusing_variable_names()
        string_formatting_issues()
        
    except Exception as e:
        print(f"預期的錯誤: {e}")
    
    print("測試完成！請檢查 SonarQube 報告以查看檢測到的問題。")