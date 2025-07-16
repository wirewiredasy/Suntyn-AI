#!/usr/bin/env python3
"""
Quick script to check tools in database and fix loading issues
"""
from app import app, db
from models import Tool, ToolCategory

def check_tools_database():
    with app.app_context():
        # Count total tools
        total_tools = Tool.query.filter_by(is_active=True).count()
        print(f"✅ Total active tools: {total_tools}")
        
        # Count tools by category
        categories = ToolCategory.query.all()
        for category in categories:
            tool_count = Tool.query.filter_by(category_id=category.id, is_active=True).count()
            print(f"   {category.display_name}: {tool_count} tools")
        
        # Show first 5 tools for verification
        tools = Tool.query.filter_by(is_active=True).limit(5).all()
        print(f"\n📋 Sample tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.display_name}")
            
        return total_tools

if __name__ == "__main__":
    count = check_tools_database()
    if count == 0:
        print("⚠️ No tools found - need to populate database")
    else:
        print(f"✅ Database has {count} tools")