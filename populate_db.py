
import os
from app import app, db
from models import ToolCategory, Tool
from config import Config

def populate_database():
    """Populate database with all tools and categories"""
    
    with app.app_context():
        try:
            # Clear existing data
            Tool.query.delete()
            ToolCategory.query.delete()
            db.session.commit()
            
            # Create categories and tools
            for category_name, category_data in Config.TOOL_CATEGORIES.items():
                # Create category
                category = ToolCategory(
                    name=category_name,
                    display_name=category_data['name'],
                    icon=category_data['icon'],
                    description=category_data['description'],
                    color=category_data['color'],
                    tool_count=len(category_data['tools']),
                    is_active=True,
                    sort_order=list(Config.TOOL_CATEGORIES.keys()).index(category_name) + 1
                )
                db.session.add(category)
                db.session.flush()  # Get category ID
                
                # Create tools for this category
                for tool_name in category_data['tools']:
                    tool = Tool(
                        name=tool_name,
                        display_name=tool_name.replace('-', ' ').title(),
                        description=f"Professional {tool_name.replace('-', ' ')} tool",
                        category_id=category.id,
                        icon=category_data['icon'],
                        is_active=True,
                        is_premium=False,
                        file_types=['*'],
                        max_file_size_mb=16,
                        features=["High Quality", "Fast Processing", "No Registration Required"]
                    )
                    db.session.add(tool)
            
            db.session.commit()
            
            # Count results
            category_count = ToolCategory.query.count()
            tool_count = Tool.query.count()
            
            print(f"✅ Successfully populated database:")
            print(f"   - {category_count} categories")
            print(f"   - {tool_count} tools")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Database population error: {str(e)}")
            return False

if __name__ == "__main__":
    # Set your PostgreSQL connection string
    os.environ["DATABASE_URL"] = "postgresql://tooloraai_db_061z_user:TV1IVOa6Ty1ZSZzN0ChMEWw6pXG7bcSS@dpg-d1rmmqadbo4c738bfiu0-a/tooloraai_db_061z"
    
    print("🚀 Populating PostgreSQL database...")
    if populate_database():
        print("✅ Database population completed successfully!")
    else:
        print("❌ Database population failed!")
