# Update base.html to add dashboard title next to hamburger

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the top navbar section
old_navbar = '''  <!-- Top Navigation Bar -->
  <nav class="top-navbar">
    <button class="hamburger" id="hamburgerBtn">
      <i class="bi bi-list"></i>
    </button>
    
    <div class="top-nav-links" id="topNavLinks">'''

new_navbar = '''  <!-- Top Navigation Bar -->
  <nav class="top-navbar">
    <div style="display: flex; align-items: center; gap: 15px;">
      <button class="hamburger" id="hamburgerBtn">
        <i class="bi bi-list"></i>
      </button>
      <span style="color: white; font-weight: 600; font-size: 1.1rem;">
        {% block dashboard_title %}Dashboard{% endblock %}
      </span>
    </div>
    
    <div class="top-nav-links" id="topNavLinks">'''

content = content.replace(old_navbar, new_navbar)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated base.html with dashboard title!")
