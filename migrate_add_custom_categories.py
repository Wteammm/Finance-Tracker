"""
Migration script to add CustomCategory table and initialize default categories for existing users
"""
from app import app, db, CustomCategory, User
from datetime import datetime

# Default categories
DEFAULT_INCOME_CATEGORIES = [
    "工资 (Salary)",
    "奖金 (Bonus)",
    "投资 (Investment)",
    "存钱 (Savings)",
    "退款 (Refund)"
]

DEFAULT_EXPENSE_CATEGORIES = [
    "PTPTN",
    "保险 (Insurance)",
    "水电费 (Utilities)",
    "电话费 (Phone)",
    "打油 (Petrol)",
    "公交 (Public Transport)",
    "Toll",
    "泊车 (Parking)",
    "餐饮 (Dining)",
    "零食 (Snacks)",
    "面包 (Bread)",
    "水果 (Fruit)",
    "蔬菜 (Vegetables)",
    "奶茶/饮料 (Drinks)",
    "炸物 (Fried Food)",
    "汉堡包 (Burger)",
    "请别人吃 (Treat Others)",
    "服装 (Clothing)",
    "鞋子 (Shoes)",
    "护肤品 (Skincare)",
    "护发 (Haircare)",
    "美容 (Beauty)",
    "梳洗卫生 (Toiletries)",
    "首饰 (Jewelry)",
    "香水 (Perfume)",
    "图书 (Books)",
    "教育 (Education)",
    "办公 (Office)",
    "家具 (Furniture)",
    "家电 (Appliances)",
    "购物 (Shopping)",
    "购物（食物） (Groceries)",
    "宠物 (Pets)",
    "家人红包 (Family Angpao)",
    "婴幼儿 (Baby)",
    "保健 (Supplements)",
    "健康 (Health)",
    "牙齿保护 (Dental)",
    "牙医 (Dentist)",
    "娱乐 (Entertainment)",
    "请别人的娱乐 (Treat Ent.)",
    "唱K (Karaoke)",
    "运动 (Sports)",
    "旅行 (Travel)",
    "彩票 (Lottery)",
    "数码 (Digital)",
    "礼物 (Gifts)"
]

def init_user_categories(user_id):
    """Initialize default categories for a user"""
    # Add income categories
    for cat_name in DEFAULT_INCOME_CATEGORIES:
        category = CustomCategory(
            user_id=user_id,
            name=cat_name,
            category_type='Income',
            is_active=True,
            is_custom=False
        )
        db.session.add(category)
    
    # Add expense categories
    for cat_name in DEFAULT_EXPENSE_CATEGORIES:
        category = CustomCategory(
            user_id=user_id,
            name=cat_name,
            category_type='Expense',
            is_active=True,
            is_custom=False
        )
        db.session.add(category)
    
    db.session.commit()
    print(f"Initialized {len(DEFAULT_INCOME_CATEGORIES) + len(DEFAULT_EXPENSE_CATEGORIES)} categories for user {user_id}")

def run_migration():
    with app.app_context():
        # Create the table
        db.create_all()
        print("[OK] CustomCategory table created")
        
        # Initialize categories for all existing users
        users = User.query.all()
        for user in users:
            # Check if user already has categories
            existing = CustomCategory.query.filter_by(user_id=user.id).first()
            if not existing:
                init_user_categories(user.id)
                print(f"[OK] Initialized categories for user: {user.username}")
            else:
                print(f"[SKIP] User {user.username} already has categories")
        
        print("\n[OK] Migration completed successfully!")

if __name__ == '__main__':
    run_migration()
