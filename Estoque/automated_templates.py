import os

files = os.listdir("./templates")


with open("app.py", 'a') as app:
    for name_uncored in files:
        name = name_uncored.split('.')[0]
        app.writelines([f'@app.route("/{name}")\n' if name != "index" else '@app.route("/")\n'
                        , f'def {name}_page():\n'
                        , f"\treturn render_template('{name_uncored}')\n\n"])

