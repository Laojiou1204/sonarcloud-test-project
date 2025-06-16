"""
個人支出追蹤器 (Personal Expense Tracker)

這個模組提供了一個簡單但完整的支出追蹤系統，展示了良好的Python程式設計實踐。
主要功能包括記錄支出、分類管理、統計分析等。
"""

import json
import datetime
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# 設定日誌記錄，這是生產環境中的最佳實踐
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Expense:
    """
    代表單一支出記錄的資料類別
    
    使用 dataclass 可以減少樣板程式碼，同時提供清晰的資料結構
    """
    amount: float
    category: str
    description: str
    date: datetime.date
    id: Optional[str] = None
    
    def __post_init__(self):
        """在物件初始化後執行的方法，用於生成唯一ID"""
        if self.id is None:
            # 使用時間戳記和描述生成簡單的ID
            timestamp = int(datetime.datetime.now().timestamp())
            self.id = f"{timestamp}_{hash(self.description) % 10000}"
    
    def to_dict(self) -> Dict:
        """將支出物件轉換為字典格式，便於序列化"""
        data = asdict(self)
        # 將日期轉換為字串格式，因為JSON不支援date物件
        data['date'] = self.date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Expense':
        """從字典創建Expense物件的類方法"""
        # 將日期字串轉回date物件
        data['date'] = datetime.date.fromisoformat(data['date'])
        return cls(**data)


class ExpenseTracker:
    """
    支出追蹤器的主要類別
    
    這個類別封裝了所有支出管理的核心功能，包括增加、刪除、
    查詢和統計分析等操作。
    """
    
    def __init__(self, data_file: str = "expenses.json"):
        """
        初始化支出追蹤器
        
        Args:
            data_file: 用於儲存支出資料的JSON檔案路徑
        """
        self.data_file = Path(data_file)
        self.expenses: List[Expense] = []
        self.categories = {
            "食物", "交通", "娛樂", "購物", "醫療", 
            "教育", "房租", "水電", "其他"
        }
        self._load_expenses()
        logger.info(f"支出追蹤器已初始化，載入了 {len(self.expenses)} 筆記錄")
    
    def add_expense(self, amount: float, category: str, description: str, 
                   date: Optional[datetime.date] = None) -> bool:
        """
        新增一筆支出記錄
        
        Args:
            amount: 支出金額，必須為正數
            category: 支出分類
            description: 支出描述
            date: 支出日期，預設為今天
            
        Returns:
            bool: 是否成功新增
            
        Raises:
            ValueError: 當金額不是正數時
        """
        try:
            # 輸入驗證是重要的防禦性程式設計實踐
            if amount <= 0:
                raise ValueError("支出金額必須大於零")
            
            if not description.strip():
                raise ValueError("支出描述不能為空")
            
            # 如果沒有提供日期，使用今天
            expense_date = date or datetime.date.today()
            
            # 自動將分類加入到已知分類中
            self.categories.add(category)
            
            # 創建新的支出記錄
            expense = Expense(
                amount=amount,
                category=category,
                description=description.strip(),
                date=expense_date
            )
            
            self.expenses.append(expense)
            self._save_expenses()
            
            logger.info(f"新增支出: ${amount} - {category} - {description}")
            return True
            
        except ValueError as e:
            logger.error(f"新增支出失敗: {e}")
            raise
        except Exception as e:
            logger.error(f"未預期的錯誤: {e}")
            return False
    
    def remove_expense(self, expense_id: str) -> bool:
        """
        移除指定ID的支出記錄
        
        Args:
            expense_id: 要移除的支出記錄ID
            
        Returns:
            bool: 是否成功移除
        """
        try:
            # 使用列表推導式來過濾掉指定ID的支出
            original_count = len(self.expenses)
            self.expenses = [exp for exp in self.expenses if exp.id != expense_id]
            
            if len(self.expenses) < original_count:
                self._save_expenses()
                logger.info(f"成功移除支出記錄 ID: {expense_id}")
                return True
            else:
                logger.warning(f"找不到ID為 {expense_id} 的支出記錄")
                return False
                
        except Exception as e:
            logger.error(f"移除支出記錄時發生錯誤: {e}")
            return False
    
    def get_expenses_by_category(self, category: str) -> List[Expense]:
        """
        取得特定分類的所有支出記錄
        
        Args:
            category: 要查詢的分類名稱
            
        Returns:
            List[Expense]: 該分類的所有支出記錄
        """
        return [exp for exp in self.expenses if exp.category == category]
    
    def get_expenses_by_date_range(self, start_date: datetime.date, 
                                  end_date: datetime.date) -> List[Expense]:
        """
        取得特定日期範圍內的支出記錄
        
        Args:
            start_date: 開始日期
            end_date: 結束日期
            
        Returns:
            List[Expense]: 日期範圍內的支出記錄
        """
        return [
            exp for exp in self.expenses 
            if start_date <= exp.date <= end_date
        ]
    
    def calculate_total_by_category(self) -> Dict[str, float]:
        """
        計算每個分類的總支出
        
        Returns:
            Dict[str, float]: 以分類為鍵，總金額為值的字典
        """
        category_totals = {}
        
        for expense in self.expenses:
            if expense.category in category_totals:
                category_totals[expense.category] += expense.amount
            else:
                category_totals[expense.category] = expense.amount
        
        return category_totals
    
    def calculate_monthly_summary(self, year: int, month: int) -> Dict[str, Union[float, int]]:
        """
        計算指定月份的支出摘要
        
        Args:
            year: 年份
            month: 月份
            
        Returns:
            Dict: 包含總額、筆數和平均金額的摘要
        """
        monthly_expenses = [
            exp for exp in self.expenses 
            if exp.date.year == year and exp.date.month == month
        ]
        
        if not monthly_expenses:
            return {
                "total_amount": 0.0,
                "expense_count": 0,
                "average_amount": 0.0,
                "categories": {}
            }
        
        total_amount = sum(exp.amount for exp in monthly_expenses)
        expense_count = len(monthly_expenses)
        average_amount = total_amount / expense_count
        
        # 計算該月份各分類的支出
        category_summary = {}
        for expense in monthly_expenses:
            if expense.category in category_summary:
                category_summary[expense.category] += expense.amount
            else:
                category_summary[expense.category] = expense.amount
        
        return {
            "total_amount": round(total_amount, 2),
            "expense_count": expense_count,
            "average_amount": round(average_amount, 2),
            "categories": category_summary
        }
    
    def _load_expenses(self) -> None:
        """
        從JSON檔案載入支出資料
        
        這是一個私有方法，用於內部資料載入
        """
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 將字典資料轉換回Expense物件
                    self.expenses = [Expense.from_dict(item) for item in data]
                    logger.info(f"成功載入 {len(self.expenses)} 筆支出記錄")
            else:
                logger.info("資料檔案不存在，從空白狀態開始")
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON檔案格式錯誤: {e}")
            self.expenses = []
        except Exception as e:
            logger.error(f"載入資料時發生錯誤: {e}")
            self.expenses = []
    
    def _save_expenses(self) -> None:
        """
        將支出資料儲存到JSON檔案
        
        這是一個私有方法，用於內部資料儲存
        """
        try:
            # 將Expense物件轉換為可序列化的字典
            data = [expense.to_dict() for expense in self.expenses]
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logger.info("支出資料已成功儲存")
            
        except Exception as e:
            logger.error(f"儲存資料時發生錯誤: {e}")


def main():
    """
    主程式入口點，展示如何使用ExpenseTracker
    
    這個函數提供了一個簡單的命令列介面來測試追蹤器的功能
    """
    print("=== 個人支出追蹤器 ===")
    
    # 創建追蹤器實例
    tracker = ExpenseTracker("sample_expenses.json")
    
    try:
        # 新增一些範例支出記錄
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        
        tracker.add_expense(250.0, "食物", "午餐 - 日式料理", today)
        tracker.add_expense(120.0, "交通", "捷運月票", today)
        tracker.add_expense(80.0, "娛樂", "電影票", yesterday)
        tracker.add_expense(45.0, "食物", "早餐", yesterday)
        
        print(f"\n目前總共有 {len(tracker.expenses)} 筆支出記錄")
        
        # 顯示分類別統計
        category_totals = tracker.calculate_total_by_category()
        print("\n=== 分類別支出統計 ===")
        for category, total in category_totals.items():
            print(f"{category}: ${total:.2f}")
        
        # 顯示本月摘要
        current_month = today.month
        current_year = today.year
        monthly_summary = tracker.calculate_monthly_summary(current_year, current_month)
        
        print(f"\n=== {current_year}年{current_month}月支出摘要 ===")
        print(f"總金額: ${monthly_summary['total_amount']}")
        print(f"支出筆數: {monthly_summary['expense_count']}")
        print(f"平均金額: ${monthly_summary['average_amount']}")
        
        print("\n程式執行完成！")
        
    except Exception as e:
        logger.error(f"主程式執行錯誤: {e}")
        print(f"程式執行時發生錯誤: {e}")


if __name__ == "__main__":
    # 當這個檔案被直接執行時，呼叫main函數
    main()