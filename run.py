import os
import re

# Define your project's templates directory
templates_dir = 'C:\\Users\\zwiad\\Desktop\\Folders\\CodersLab\\finalProject\\quikcart\\templates' 

# Regex to match local static files specifically for CSS, JS, and images, 
# and avoid direct .html references that should not be converted.
pattern = re.compile(r'(href|src)="(?!http://|https://|#|javascript:;|login.html#|index.html|index2.html|index3.html|index4.html|#0)([^"]+\.(css|js|png|jpg|jpeg|gif))"')

# Replacement function
def replace_with_static(match):
    attr = match.group(1)  # href or src
    file_path = match.group(2)  # the actual file path
    return f'{attr}="{{% static \'{file_path}\' %}}"'

# Process files
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):  # Adjust for other file types if needed
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Ensure {% load static %} is present
            if "{% load static %}" not in content:
                content = "{% load static %}\n" + content
            
            # Replace the content
            updated_content = pattern.sub(replace_with_static, content)
            
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

print("All files have been processed.")
