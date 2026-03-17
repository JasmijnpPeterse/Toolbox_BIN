from flask import Flask, render_template_string, render_template, request

app = Flask(__name__)
@app.route('/')
def open_page():
    return render_template('web.html')
@app.route('/lucas.html')
def information_page():
    return render_template('lucas.html')
@app.route('/background_info.html')
def background_info_page():
    return render_template('background_info.html')
@app.route('/web.html', methods = ['GET', 'POST'])
def output():
    if request.method == 'GET':
        return render_template('web.html')
    elif request.method == 'POST':
        return render_template_string('''
        <html>
        <head>
        <body>
        
        ''')
    return

if __name__ == '__main__':
    app.run()
