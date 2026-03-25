from flask import Flask,send_from_directory,redirect, url_for, render_template_string, render_template, request, session
import os

app = Flask(__name__)
app.secret_key = "BINNANPORE"

@app.route('/')
def input_output_page():
    return render_template('web.html')

@app.route('/lucas.html')
def information_page():
    return render_template('Info_pagina.html')

@app.route('/background_info.html')
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
        email_file = os.path.join(upload_folder, 'emails.txt')
        with open(email_file, 'a') as f:
            f.write(email + '\n')
    return redirect('web.html')

upload_folder = ('Data')
os.makedirs(upload_folder, exist_ok=True)

@app.route('/web.html', methods=['GET', 'POST'])
def output():
    uitslag = session.get("uitslag")
    show_results = session.get("show_results", False)

    if request.method == 'GET':
        return render_template('web.html')
    elif request.method == 'POST':
        kwags = {
            'tabel_snps': request.form.get('tabel_snps') is not None,
            'tabel_mutaties': request.form.get('tabel_mutaties') is not None,
            'kwaliteitscore': request.form.get('kwaliteitscore') is not None,
            'vcf_doc': request.form.get('vcf_doc') is not None
        }

        # Nieuwe input file
        file = request.files.get('data')

        if file and file.filename != "":
            filename = file.filename
            file.save(os.path.join(upload_folder, filename))

            uitslag = {"status": f"Bestand '{filename}' succesvol geüpload"}
            show_results = True
        else:
            uitslag = {"status": "FOUT: Geen bestand geselecteerd"}
            show_results = True  # ook tonen zodat je de fout ziet

        return render_template('web.html', **kwags, uitslag=uitslag, show_results=show_results)


    return render_template('web.html',
        tabel_snps=False,
        tabel_mutaties=False,
        kwaliteitscore=False,
        vcf_doc=False
    )

if __name__ == '__main__':
    app.run(debug=True)
