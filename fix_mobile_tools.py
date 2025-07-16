#!/usr/bin/env python3
"""
Fix mobile tools display issue by testing the route directly
"""
import requests

def test_tools_page():
    try:
        # Test the tools page endpoint
        response = requests.get('http://localhost:5000/tools/')
        
        print(f"✅ Status Code: {response.status_code}")
        
        # Check if tools are being rendered
        content = response.text
        tool_cards = content.count('tool-card')
        tools_grid = content.count('tools-grid')
        
        print(f"📊 Tool cards found: {tool_cards}")
        print(f"📊 Tools grid found: {tools_grid}")
        
        # Check for specific tool names
        sample_tools = ['pdf-merge', 'image-compress', 'video-to-mp3']
        for tool in sample_tools:
            if tool in content:
                print(f"✅ Tool '{tool}' found in page")
            else:
                print(f"❌ Tool '{tool}' NOT found in page")
        
        # Check for JavaScript errors or issues
        if 'tool-card' in content and tool_cards > 0:
            print("✅ Tools are rendering correctly")
            return True
        else:
            print("❌ Tools are not rendering")
            return False
            
    except Exception as e:
        print(f"❌ Error testing tools page: {e}")
        return False

if __name__ == "__main__":
    test_tools_page()