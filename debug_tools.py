#!/usr/bin/env python3
"""
Debug script to check why tools are not appearing on the tools page
"""

from app import app, db
from models import Tool, ToolCategory
from routes.tools import tools_bp
from flask import render_template_string

def debug_tools_rendering():
    with app.app_context():
        # Test database query directly
        tools = Tool.query.filter_by(is_active=True).all()
        print(f"Database has {len(tools)} active tools")
        
        if tools:
            print("Sample tools:")
            for tool in tools[:3]:
                print(f"  - {tool.name}: {tool.display_name}")
                print(f"    Category: {tool.category.name if tool.category else 'None'}")
                print(f"    Icon: {tool.icon}")
        
        # Test template rendering with minimal template
        test_template = """
        <div>Tools count: {{ tools|length }}</div>
        {% for tool in tools %}
        <div>Tool: {{ tool.name }} - {{ tool.display_name }}</div>
        {% endfor %}
        """
        
        try:
            rendered = render_template_string(test_template, tools=tools)
            print(f"\nTemplate test result:")
            print(rendered[:500])
        except Exception as e:
            print(f"Template error: {e}")

if __name__ == "__main__":
    debug_tools_rendering()