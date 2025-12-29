"""
Finance Tracker - Add Password Management Features
Migration script to add email and security questions to User model
Version: 2.1
"""

from app import app, db, User
from werkzeug.security import generate_password_hash
from sqlalchemy import text

def migrate():
    print("=" * 50)
    print("Finance Tracker - Password Management Migration")
    print("Version 2.1")
    print("=" * 50)
    print()
    
    with app.app_context():
        try:
            # Add new columns to User table
            print("[1/3] Adding new columns to User table...")
            
            with db.engine.connect() as conn:
                # Add email column (optional)
                try:
                    conn.execute(text('ALTER TABLE user ADD COLUMN email VARCHAR(120)'))
                    conn.commit()
                    print("  [OK] Added email column")
                except Exception as e:
                    if "duplicate column name" in str(e).lower():
                        print("  [INFO] Email column already exists")
                    else:
                        raise
                
                # Add security question columns
                security_columns = [
                    ('security_question_1', 'VARCHAR(200)'),
                    ('security_answer_1', 'VARCHAR(200)'),
                    ('security_question_2', 'VARCHAR(200)'),
                    ('security_answer_2', 'VARCHAR(200)'),
                    ('security_question_3', 'VARCHAR(200)'),
                    ('security_answer_3', 'VARCHAR(200)')
                ]
                
                for col_name, col_type in security_columns:
                    try:
                        conn.execute(text(f'ALTER TABLE user ADD COLUMN {col_name} {col_type}'))
                        conn.commit()
                        print(f"  [OK] Added {col_name} column")
                    except Exception as e:
                        if "duplicate column name" in str(e).lower():
                            print(f"  [INFO] {col_name} column already exists")
                        else:
                            raise
            
            print()
            print("[2/3] Verifying columns...")
            
            # Verify columns exist
            users = User.query.all()
            print(f"  [OK] Found {len(users)} existing users")
            
            # Check if any user has security questions
            users_with_questions = User.query.filter(User.security_question_1.isnot(None)).count()
            print(f"  [INFO] {users_with_questions} users have security questions set")
            
            print()
            print("[3/3] Migration Summary...")
            print(f"  - Email field: Added (optional)")
            print(f"  - Security questions: 3 questions + 3 answers")
            print(f"  - Existing users: {len(users)}")
            print(f"  - Users with security questions: {users_with_questions}")
            
            print()
            print("=" * 50)
            print("[SUCCESS] Migration completed successfully!")
            print("=" * 50)
            print()
            print("Next steps:")
            print("1. Existing users will be prompted to set security questions on next login")
            print("2. New users will set security questions during registration")
            print("3. Email field is ready for future email-based recovery (v3.0)")
            print()
            
        except Exception as e:
            print(f"[ERROR] Migration failed: {e}")
            raise

if __name__ == '__main__':
    migrate()
