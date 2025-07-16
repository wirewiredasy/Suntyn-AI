#!/usr/bin/env python3
"""
Fix Template Syntax for All Tools
Fix the incorrect template syntax in all generated templates
"""

import os
import re
from config import Config

def fix_template_syntax(template_path):
    """Fix template syntax in a single template file"""
    if not os.path.exists(template_path):
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix double curly braces in template tags
    content = re.sub(r'\{\{%%\s*([^%]+)\s*%%\}\}', r'{% \1 %}', content)
    content = re.sub(r'\{\{%% ([^%]+) %%\}\}', r'{% \1 %}', content)
    
    # Fix URL generation
    content = re.sub(r'\{\{\{\{\s*([^}]+)\s*\}\}\}\}', r'{{ \1 }}', content)
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def fix_all_templates():
    """Fix syntax in all tool templates"""
    templates_dir = 'templates/tools'
    fixed_count = 0
    
    print("🔧 Fixing Template Syntax Issues")
    print("=" * 40)
    
    for category_id, category_data in Config.TOOL_CATEGORIES.items():
        print(f"\n📁 {category_data['name']} ({len(category_data['tools'])} tools)")
        
        for tool_name in category_data['tools']:
            template_path = f"{templates_dir}/{tool_name}.html"
            
            if fix_template_syntax(template_path):
                print(f"  ✅ Fixed {tool_name}.html")
                fixed_count += 1
            else:
                print(f"  ❌ Template not found: {tool_name}.html")
    
    print(f"\n🎉 Fixed {fixed_count} templates")
    return fixed_count

if __name__ == "__main__":
    fix_all_templates()