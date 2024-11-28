import os
import re

files = os.listdir("./templates")

with open("app.py", 'r') as app:
    content = app.read()

with open("app.py", 'a') as app:
    if not f'@app.route("/")' in content:

        app.writelines([f'@app.route("/")\n',
                        f'def index():\n',
                        f"\treturn render_template('index.html')\n\n"])

    for name_uncored in files:
        name = name_uncored.split('.')[0]
        if (not (f'@app.route("/{name}') in content) and (name != "index"):
            app.writelines([f'@app.route("/{name}")\n' if name != "index" else '@app.route("/")\n'
                            , f'def {name}_page():\n'
                            , f"\treturn render_template('{name_uncored}')\n\n"])


files = ['./templates/aaa.html'] 

for file_name in files:
    
    
    with open(file_name, 'r') as file:
        content = file.read()
    

    new_content = re.sub(".html", "", content)

    with open(file_name, 'w') as file:
        file.write(new_content)