#!/usr/bin/env python3
"""
Debug script to check tools page rendering
"""

from app import app
from models import Tool, ToolCategory

def debug_tools_page():
    with app.app_context():
        # Check database
        tools = Tool.query.filter_by(is_active=True).all()
        categories = ToolCategory.query.filter_by(is_active=True).all()
        
        print(f"Database has {len(tools)} active tools")
        print(f"Database has {len(categories)} active categories")
        
        # Test route
        with app.test_client() as client:
            response = client.get('/tools/')
            print(f"Response status: {response.status_code}")
            print(f"Response length: {len(response.data)}")
            
            # Check for specific content
            content = response.data.decode('utf-8')
            
            # Count tool cards
            tool_card_count = content.count('class="tool-card')
            print(f"Tool cards in HTML: {tool_card_count}")
            
            # Check for loading messages
            if "Loading tools" in content:
                print("Found 'Loading tools' message")
            else:
                print("No 'Loading tools' message found")
                
            # Check for no tools message
            if "No tools found" in content:
                print("Found 'No tools found' message")
            else:
                print("No 'No tools found' message")
            
            # Check specific tools
            if "pdf-merge" in content:
                print("Found PDF merge tool")
            
            if "tool-card" in content:
                print("Found tool-card class")
            
            # Check for errors
            if "error" in content.lower() or "exception" in content.lower():
                print("Found error/exception in response")

if __name__ == "__main__":
    debug_tools_page()