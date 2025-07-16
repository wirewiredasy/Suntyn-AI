
import os
from app import app, db
import models

def setup_neon_database():
    """Setup Neon PostgreSQL database with all tables"""
    
    # Set Neon database URL
    neon_url = os.environ.get("NEON_DATABASE_URL", "")
    if not neon_url:
        print("❌ NEON_DATABASE_URL not found in environment variables")
        return False
    
    # Temporarily override DATABASE_URL to use Neon
    original_url = os.environ.get("DATABASE_URL", "")
    os.environ["DATABASE_URL"] = neon_url
    
    with app.app_context():
        try:
            # Update app config to use Neon database
            app.config["SQLALCHEMY_DATABASE_URI"] = neon_url
            
            # Create all tables
            db.create_all()
            print("✅ Neon database tables created successfully!")
            
            # Test database connection
            result = db.session.execute(db.text("SELECT 1"))
            print("✅ Neon database connection test successful!")
            
            # Check if tables exist
            tables = db.session.execute(db.text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)).fetchall()
            
            print(f"✅ Created {len(tables)} tables in Neon:")
            for table in tables:
                print(f"   - {table[0]}")
                
        except Exception as e:
            print(f"❌ Neon database setup error: {str(e)}")
            return False
        finally:
            # Restore original DATABASE_URL
            if original_url:
                os.environ["DATABASE_URL"] = original_url
            
    return True

if __name__ == "__main__":
    print("🚀 Setting up Neon PostgreSQL database...")
    if setup_neon_database():
        print("✅ Neon database setup completed successfully!")
    else:
        print("❌ Neon database setup failed!")
