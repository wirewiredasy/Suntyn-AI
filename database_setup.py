
import os
from app import app, db
import models

def setup_database():
    """Setup PostgreSQL database with all tables"""
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Test database connection
            result = db.session.execute(db.text("SELECT 1"))
            print("✅ Database connection test successful!")
            
            # Check if tables exist
            tables = db.session.execute(db.text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)).fetchall()
            
            print(f"✅ Created {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
                
        except Exception as e:
            print(f"❌ Database setup error: {str(e)}")
            return False
            
    return True

if __name__ == "__main__":
    # Set your PostgreSQL connection string here
    os.environ["DATABASE_URL"] = "postgresql://tooloraai_db_061z_user:TV1IVOa6Ty1ZSZzN0ChMEWw6pXG7bcSS@dpg-d1rmmqadbo4c738bfiu0-a/tooloraai_db_061z"
    
    print("🚀 Setting up PostgreSQL database...")
    if setup_database():
        print("✅ Database setup completed successfully!")
    else:
        print("❌ Database setup failed!")
