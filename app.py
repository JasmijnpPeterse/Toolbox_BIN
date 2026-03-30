from flask import Flask,send_from_directory,redirect, render_template, request
import os
from backend import run as run_pipeline
from backend import lezen_vcf

app = Flask(__name__)
app.secret_key = "BINNANPORE"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FASTQ_BESTAND = os.path.join(BASE_DIR, "data", "ERR2165898.fastq")
REFERENCE     = os.path.join(BASE_DIR, "data", "reference", "GCF_000006945.2_ASM694v2_genomic.fna")

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
    if request.method == 'GET':
        return render_template('web.html')
    elif request.method == 'POST':
        chromosoom = request.form.get('chromosoom', '').strip()
        startpunt  = request.form.get('startpunt', '').strip()
        eindpunt   = request.form.get('eindpunt', '').strip()

        region = None
        region_error = None

        if chromosoom:
            if startpunt and eindpunt:
                try:
                    if int(startpunt) >= int(eindpunt):
                        region_error = "Startpositie moet kleiner zijn dan eindpositie."
                    else:
                        region = f"{chromosoom}:{startpunt}-{eindpunt}"
                except ValueError:
                    region_error = "Start- en eindpositie moeten gehele getallen zijn."
            elif startpunt or eindpunt:
                region_error = "Vul zowel de start- als eindpositie in, of laat beide leeg."
            else:
                region = chromosoom

        if region_error:
            return render_template('web.html', region_error=region_error)

        kwags = {
            'fastq_bestand': FASTQ_BESTAND,
            'reference': REFERENCE,
            'threads': 8,
            'N': 5,
            'region': region,
            'tabel_snps': request.form.get('tabel_snps') is not None,
            'plot_mutaties': request.form.get('plot_mutaties') is not None,
            'kwaliteitscore': request.form.get('kwaliteitscore') is not None,
            'vcf_doc': request.form.get('vcf_doc') is not None
        }

        run_pipeline(kwags)

        return render_template('web.html', **kwags)

    return render_template('web.html',
        tabel_snps=False,
        tabel_mutaties=False,
        kwaliteitscore=False,
        vcf_doc=False
    )

if __name__ == '__main__':
    app.run(debug=True)
