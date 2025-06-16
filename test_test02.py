"""
單元測試檔案：test_personal_expense_tracker.py

這個檔案包含了對 personal_expense_tracker.py 的完整測試覆蓋。
每個測試方法都專注於驗證一個特定的功能或情境。

測試的命名遵循：test_方法名稱_預期行為 的模式
這種命名讓其他開發者能夠快速理解每個測試的目的
"""

import unittest
import datetime
import tempfile
import os
from pathlib import Path

# 導入我們要測試的類別和函數
# 這裡假設你的原始檔案名為 personal_expense_tracker.py
from personal_expense_tracker import Expense, ExpenseTracker


class TestExpense(unittest.TestCase):
    """
    測試 Expense 資料類別的功能
    
    這個測試類別專注於驗證 Expense 物件的基本行為，
    包括物件創建、資料轉換和驗證邏輯等。
    """
    
    def setUp(self):
        """
        在每個測試方法執行前都會執行的設定方法
        
        setUp 方法讓我們可以為每個測試準備乾淨的測試環境，
        確保測試之間不會互相影響，這是測試獨立性的重要原則。
        """
        self.test_date = datetime.date(2024, 6, 15)
        self.test_expense = Expense(
            amount=100.0,
            category="食物",
            description="午餐",
            date=self.test_date
        )
    
    def test_expense_creation_with_valid_data(self):
        """
        測試使用有效資料創建 Expense 物件
        
        這個測試驗證我們最基本的功能：能否正確創建一個支出記錄。
        我們檢查所有屬性是否按預期設定，包括自動生成的ID。
        """
        # 驗證基本屬性是否正確設定
        self.assertEqual(self.test_expense.amount, 100.0)
        self.assertEqual(self.test_expense.category, "食物")
        self.assertEqual(self.test_expense.description, "午餐")
        self.assertEqual(self.test_expense.date, self.test_date)
        
        # 驗證ID是否自動生成（不應該為None）
        self.assertIsNotNone(self.test_expense.id)
        self.assertIsInstance(self.test_expense.id, str)
    
    def test_expense_to_dict_conversion(self):
        """
        測試 Expense 物件轉換為字典的功能
        
        這個測試確保我們的資料序列化功能正常工作，
        這對於儲存和載入資料至關重要。
        """
        expense_dict = self.test_expense.to_dict()
        
        # 驗證字典包含所有必要的鍵
        expected_keys = {'amount', 'category', 'description', 'date', 'id'}
        self.assertEqual(set(expense_dict.keys()), expected_keys)
        
        # 驗證日期是否正確轉換為字串格式
        self.assertEqual(expense_dict['date'], '2024-06-15')
        self.assertEqual(expense_dict['amount'], 100.0)
    
    def test_expense_from_dict_creation(self):
        """
        測試從字典創建 Expense 物件的功能
        
        這個測試驗證反序列化過程，確保我們能從儲存的資料
        正確重建 Expense 物件。
        """
        expense_dict = {
            'amount': 150.0,
            'category': '交通',
            'description': '捷運費',
            'date': '2024-06-16',
            'id': 'test_id_123'
        }
        
        recreated_expense = Expense.from_dict(expense_dict)
        
        # 驗證重建的物件屬性正確
        self.assertEqual(recreated_expense.amount, 150.0)
        self.assertEqual(recreated_expense.category, '交通')
        self.assertEqual(recreated_expense.description, '捷運費')
        self.assertEqual(recreated_expense.date, datetime.date(2024, 6, 16))
        self.assertEqual(recreated_expense.id, 'test_id_123')


class TestExpenseTracker(unittest.TestCase):
    """
    測試 ExpenseTracker 類別的功能
    
    這個測試類別涵蓋了支出追蹤器的所有主要功能，
    包括添加支出、刪除支出、統計分析等。
    """
    
    def setUp(self):
        """
        為每個測試準備獨立的測試環境
        
        我們使用臨時檔案來避免測試對真實資料的影響，
        這是測試隔離性的重要實踐。
        """
        # 創建臨時檔案作為測試資料庫
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        
        # 使用臨時檔案創建追蹤器實例
        self.tracker = ExpenseTracker(self.temp_file.name)
        
        # 準備測試日期
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
    
    def tearDown(self):
        """
        在每個測試結束後清理資源
        
        這個方法確保我們不會留下測試產生的臨時檔案，
        保持測試環境的乾淨。
        """
        # 刪除臨時測試檔案
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_valid_expense(self):
        """
        測試添加有效支出記錄的功能
        
        這是我們最核心的功能測試，驗證正常情況下
        添加支出是否能正確工作。
        """
        # 執行添加操作
        result = self.tracker.add_expense(50.0, "食物", "早餐", self.today)
        
        # 驗證添加操作成功
        self.assertTrue(result)
        
        # 驗證支出記錄確實被添加到追蹤器中
        self.assertEqual(len(self.tracker.expenses), 1)
        
        # 驗證添加的支出記錄內容正確
        expense = self.tracker.expenses[0]
        self.assertEqual(expense.amount, 50.0)
        self.assertEqual(expense.category, "食物")
        self.assertEqual(expense.description, "早餐")
        self.assertEqual(expense.date, self.today)
    
    def test_add_expense_with_invalid_amount(self):
        """
        測試添加無效金額的錯誤處理
        
        這個測試驗證我們的輸入驗證邏輯，確保程式能夠
        正確拒絕不合理的輸入並提供明確的錯誤訊息。
        """
        # 測試負數金額
        with self.assertRaises(ValueError) as context:
            self.tracker.add_expense(-10.0, "食物", "測試", self.today)
        
        self.assertIn("支出金額必須大於零", str(context.exception))
        
        # 測試零金額
        with self.assertRaises(ValueError):
            self.tracker.add_expense(0.0, "食物", "測試", self.today)
        
        # 驗證無效操作後，追蹤器中沒有添加任何記錄
        self.assertEqual(len(self.tracker.expenses), 0)
    
    def test_add_expense_with_empty_description(self):
        """
        測試添加空白描述的錯誤處理
        
        這個測試確保我們不接受無意義的空白描述，
        維護資料品質的完整性。
        """
        with self.assertRaises(ValueError) as context:
            self.tracker.add_expense(50.0, "食物", "", self.today)
        
        self.assertIn("支出描述不能為空", str(context.exception))
        
        # 測試只包含空格的描述
        with self.assertRaises(ValueError):
            self.tracker.add_expense(50.0, "食物", "   ", self.today)
    
    def test_remove_existing_expense(self):
        """
        測試移除存在的支出記錄
        
        這個測試驗證我們能夠正確識別並移除指定的支出記錄。
        """
        # 先添加一筆支出
        self.tracker.add_expense(100.0, "購物", "書籍", self.today)
        expense_id = self.tracker.expenses[0].id
        
        # 移除這筆支出
        result = self.tracker.remove_expense(expense_id)
        
        # 驗證移除操作成功
        self.assertTrue(result)
        
        # 驗證支出記錄確實被移除
        self.assertEqual(len(self.tracker.expenses), 0)
    
    def test_remove_nonexistent_expense(self):
        """
        測試移除不存在的支出記錄
        
        這個測試確保當我們嘗試移除不存在的記錄時，
        程式能夠優雅地處理這種情況。
        """
        result = self.tracker.remove_expense("nonexistent_id")
        
        # 驗證移除操作返回False，表示沒有找到對應記錄
        self.assertFalse(result)
    
    def test_get_expenses_by_category(self):
        """
        測試按分類獲取支出記錄的功能
        
        這個測試驗證我們的查詢和過濾功能是否正確工作。
        """
        # 添加不同分類的支出記錄
        self.tracker.add_expense(30.0, "食物", "午餐", self.today)
        self.tracker.add_expense(120.0, "交通", "計程車", self.today)
        self.tracker.add_expense(45.0, "食物", "晚餐", self.yesterday)
        
        # 獲取食物分類的支出
        food_expenses = self.tracker.get_expenses_by_category("食物")
        
        # 驗證結果正確
        self.assertEqual(len(food_expenses), 2)
        for expense in food_expenses:
            self.assertEqual(expense.category, "食物")
        
        # 驗證總金額計算正確
        total_food_amount = sum(exp.amount for exp in food_expenses)
        self.assertEqual(total_food_amount, 75.0)
    
    def test_get_expenses_by_date_range(self):
        """
        測試按日期範圍獲取支出記錄的功能
        
        這個測試驗證日期範圍查詢的邏輯，包括邊界條件的處理。
        """
        # 添加不同日期的支出記錄
        past_date = self.today - datetime.timedelta(days=5)
        future_date = self.today + datetime.timedelta(days=2)
        
        self.tracker.add_expense(100.0, "食物", "過去", past_date)
        self.tracker.add_expense(200.0, "食物", "今天", self.today)
        self.tracker.add_expense(150.0, "食物", "未來", future_date)
        
        # 查詢今天到未來的支出
        recent_expenses = self.tracker.get_expenses_by_date_range(
            self.today, future_date
        )
        
        # 驗證結果包含正確的記錄
        self.assertEqual(len(recent_expenses), 2)
        descriptions = [exp.description for exp in recent_expenses]
        self.assertIn("今天", descriptions)
        self.assertIn("未來", descriptions)
        self.assertNotIn("過去", descriptions)
    
    def test_calculate_total_by_category(self):
        """
        測試分類統計計算的準確性
        
        這個測試驗證我們的統計分析功能，確保計算結果正確。
        """
        # 添加多筆不同分類的支出
        self.tracker.add_expense(50.0, "食物", "早餐", self.today)
        self.tracker.add_expense(120.0, "食物", "午餐", self.today)
        self.tracker.add_expense(80.0, "交通", "捷運", self.today)
        self.tracker.add_expense(200.0, "娛樂", "電影", self.today)
        self.tracker.add_expense(60.0, "交通", "公車", self.yesterday)
        
        # 計算分類統計
        category_totals = self.tracker.calculate_total_by_category()
        
        # 驗證統計結果正確
        expected_totals = {
            "食物": 170.0,
            "交通": 140.0,
            "娛樂": 200.0
        }
        
        self.assertEqual(category_totals, expected_totals)
    
    def test_calculate_monthly_summary(self):
        """
        測試月度摘要計算的完整性
        
        這個測試驗證月度統計功能，包括總額、筆數、平均值等指標。
        """
        # 使用特定日期進行測試，避免跨月問題
        test_date = datetime.date(2024, 6, 15)
        
        # 添加本月的支出記錄
        self.tracker.add_expense(100.0, "食物", "餐廳", test_date)
        self.tracker.add_expense(200.0, "購物", "衣服", test_date)
        self.tracker.add_expense(80.0, "食物", "超市", test_date)
        
        # 添加其他月份的支出（不應包含在摘要中）
        other_month_date = datetime.date(2024, 5, 15)
        self.tracker.add_expense(50.0, "食物", "其他月", other_month_date)
        
        # 計算6月的摘要
        summary = self.tracker.calculate_monthly_summary(2024, 6)
        
        # 驗證摘要數據正確
        self.assertEqual(summary['total_amount'], 380.0)
        self.assertEqual(summary['expense_count'], 3)
        self.assertEqual(summary['average_amount'], 126.67)
        
        # 驗證分類統計正確
        expected_categories = {
            "食物": 180.0,
            "購物": 200.0
        }
        self.assertEqual(summary['categories'], expected_categories)
    
    def test_calculate_monthly_summary_empty_month(self):
        """
        測試空月份的摘要計算
        
        這個測試確保當某個月沒有支出記錄時，
        摘要功能能夠返回合理的預設值。
        """
        # 不添加任何支出記錄
        summary = self.tracker.calculate_monthly_summary(2024, 12)
        
        # 驗證空月份的摘要結構正確
        expected_summary = {
            "total_amount": 0.0,
            "expense_count": 0,
            "average_amount": 0.0,
            "categories": {}
        }
        
        self.assertEqual(summary, expected_summary)
    
    def test_data_persistence(self):
        """
        測試資料持久化功能
        
        這個測試驗證資料能夠正確儲存到檔案並在重新載入時恢復。
        """
        # 添加支出記錄
        self.tracker.add_expense(100.0, "測試", "持久化測試", self.today)
        original_expense_id = self.tracker.expenses[0].id
        
        # 創建新的追蹤器實例，使用相同的檔案
        new_tracker = ExpenseTracker(self.temp_file.name)
        
        # 驗證資料被正確載入
        self.assertEqual(len(new_tracker.expenses), 1)
        loaded_expense = new_tracker.expenses[0]
        
        self.assertEqual(loaded_expense.amount, 100.0)
        self.assertEqual(loaded_expense.category, "測試")
        self.assertEqual(loaded_expense.description, "持久化測試")
        self.assertEqual(loaded_expense.date, self.today)
        self.assertEqual(loaded_expense.id, original_expense_id)


def run_tests_with_coverage():
    """
    執行測試並顯示覆蓋率資訊的輔助函數
    
    這個函數提供了一個簡單的方式來執行所有測試，
    並且可以與覆蓋率工具整合。
    """
    # 創建測試套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 載入所有測試
    suite.addTests(loader.loadTestsFromTestCase(TestExpense))
    suite.addTests(loader.loadTestsFromTestCase(TestExpenseTracker))
    
    # 執行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 顯示測試結果摘要
    print(f"\n=== 測試結果摘要 ===")
    print(f"執行的測試數量: {result.testsRun}")
    print(f"失敗的測試: {len(result.failures)}")
    print(f"錯誤的測試: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 所有測試都通過了！")
    else:
        print("❌ 有測試失敗，請檢查錯誤訊息")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    """
    當直接執行這個測試檔案時的入口點
    
    這允許我們直接執行: python test_personal_expense_tracker.py
    來運行所有測試。
    """
    print("開始執行 ExpenseTracker 的單元測試...")
    success = run_tests_with_coverage()
    
    if success:
        print("\n✅ 測試覆蓋率應該已經大幅提升！")
        print("現在可以重新推送程式碼到 GitHub，SonarCloud 應該會顯示通過的結果。")
    else:
        print("\n❌ 測試未完全通過，請檢查並修正問題後再次嘗試。")