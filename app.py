from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
@app.route('/web.html')
def web():
    return render_template('web.html')

@app.route('/lucas.html')
def lucas():
    return render_template('lucas.html')

@app.route('/background_info.html')
def background_info():
    return render_template('background_info.html')

@app.route('/stylesheet.css')
def stylesheet():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'stylesheet.css')


@app.route('/aanmelden', methods=['POST'])
def aanmelden():
    email = request.form.get('email')
    if email:
        with open('emails.txt', 'a') as f:
            f.write(email + '\n')
    return redirect(url_for('lucas'))


if __name__ == '__main__':
    app.run(debug=True)