from flask import Flask,send_from_directory,redirect, render_template, request
import os
from backend import run as run_pipeline
from backend import lezen_vcf, Plot
from werkzeug.middleware.profiler import ProfilerMiddleware

app = Flask(__name__)
app.secret_key = "BINNANPORE"
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=('app.py', 'backend.py'))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FASTQ_BESTAND = os.path.join(BASE_DIR, "Data", "ERR2165898.fastq")
REFERENCE = os.path.join(BASE_DIR, "Data", "reference", "GCF_000006945.2_ASM694v2_genomic.fna")

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

        if startpunt and eindpunt:
            try:
                if int(startpunt) >= int(eindpunt):
                    region_error = "Startpositie moet kleiner zijn dan eindpositie."
                else:
                    if chromosoom:
                        region = f"{chromosoom}:{startpunt}-{eindpunt}"
                    else:
                        region = f"{startpunt}-{eindpunt}"
            except ValueError:
                region_error = "Start- en eindpositie moeten gehele getallen zijn."
        elif startpunt or eindpunt:
            region_error = "Vul zowel de start- als eindpositie in, of laat beide leeg."
        else:
            region = chromosoom

        if region_error:
            return render_template('web.html', region_error=region_error)

        kwargs = {
            'fastq_bestand': FASTQ_BESTAND,
            'reference': REFERENCE,
            'threads': 8,
            'N': 5,
            'region': region,
            'tabel_snps': request.form.get('tabel_snps') is not None,
            'plot_mutaties': request.form.get('plot_mutaties') is not None,
            'chroms': request.form.get('plot_chroms') is not None
        }

        run_pipeline(kwargs)
        region_error_mutation = None
        region_error_snp = None
        mutaties, snps_tabel_info, chroms = lezen_vcf()
        mutaties_png = None
        chroms_png = None
        region_error_chroms = None

        if kwargs['plot_mutaties']:
            if not mutaties:
                region_error_mutation = "Geen mutaties gevonden om te plotten."
            else:
                plot_data = Plot(mutaties)
                mutaties_png = plot_data.maken_plot(mutaties)
        if kwargs['chroms']:
            if not chroms:
                region_error_chroms = "Geen mutaties op een chromosoom gevonden"
            else:
                plot_data = Plot(chroms)
                chroms_png = plot_data.maken_plot(chroms)
        if kwargs['tabel_snps']:
            if not snps_tabel_info:
                region_error_snp="Geen snp's gevonden om in tabel te zetten"
        return render_template(
            'web.html',
            **kwargs,
            mutatie_fig= mutaties_png,
            chroms_fig=chroms_png,
            snps_tabel_info=snps_tabel_info,
            region_error_mutation=region_error_mutation,
            region_error_snp=region_error_snp,
            region_error_chroms=region_error_chroms
        )


    return render_template('web.html',
        tabel_snps=False,
        tabel_mutaties=False,
        kwaliteitscore=False,
        vcf_doc=False
    )

if __name__ == '__main__':
    app.run(debug=True, port=5002)
