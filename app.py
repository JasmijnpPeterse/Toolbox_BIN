from flask import Flask,send_from_directory,redirect, url_for, render_template_string, render_template, request, session
import os

app = Flask(__name__)
app.secret_key = "BINNANPORE"

@app.route('/')
def input_output_page():
    return render_template('web.html')

@app.route('/Info_pagina.html')
def information_page():
    return render_template('Info_pagina.html')

@app.route('/tools_info.html')
def tools_info_page():
    return render_template('tools_info.html')

@app.route('/reference.html')
def reference_gen_page():
    return render_template('reference.html')

@app.route('/stylesheet.css')
def stylesheet():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'stylesheet.css')


@app.route('/aanmelden', methods=['POST'])
def aanmelden():
    email = request.form.get('email')
    if email:
        with open('email.txt', 'a') as f:
            f.write(email + '\n')
    return redirect('web.html')

@app.route('/web.html', methods=['GET', 'POST'])
def output():
    download_map = os.getcwd()
    if request.method == 'GET':
        return render_template('web.html')
    elif request.method == 'POST':
        pad_naar_download = os.path.join(download_map, "output.vcf")
        kwags = {
            'tabel_snps': request.form.get('tabel_snps') is not None,
            'plot_mutaties': request.form.get('plot_mutaties') is not None,
            'kwaliteitscore': request.form.get('kwaliteitscore') is not None,
            'vcf_doc': request.form.get('vcf_doc') is not None,
            'download_pad': pad_naar_download
        }
        return render_template('web.html', **kwags)

    return render_template('web.html',
        tabel_snps=False,
        tabel_mutaties=False,
        kwaliteitscore=False,
        vcf_doc=False
    )

if __name__ == '__main__':
    app.run(debug=True)
