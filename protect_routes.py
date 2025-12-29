# Add @login_required to all routes except /login and /logout
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all @app.route decorators (but not /login or /logout)
# Pattern: @app.route('...') followed by optional decorators and then def function_name()
lines = content.split('\n')
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this is an @app.route line
    if line.strip().startswith('@app.route('):
        # Check if it's login or logout route
        if "'/login'" in line or "'/logout'" in line:
            new_lines.append(line)
            i += 1
            continue
        
        # Check if next line already has @login_required
        if i + 1 < len(lines) and '@login_required' in lines[i + 1]:
            new_lines.append(line)
            i += 1
            continue
        
        # Add the route line
        new_lines.append(line)
        # Add @login_required decorator
        new_lines.append('@login_required')
        i += 1
    else:
        new_lines.append(line)
        i += 1

new_content = '\n'.join(new_lines)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Added @login_required to all routes!")
