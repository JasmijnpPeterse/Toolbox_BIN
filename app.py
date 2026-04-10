"""
Bio-informatica nanopore sequencing analyse

Autors: Lucas Bos, Jasmijn Peterse, Vani Rembet
Version: 1.0
Date: 30/03 - 10/04
"""
import os
from flask import Flask,send_from_directory,redirect, render_template, request
from werkzeug.middleware.profiler import ProfilerMiddleware
from backend import run as run_pipeline
from backend import lezen_vcf, Plot

app = Flask(__name__)
app.secret_key = "BINNANPORE"
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=('app.py', 'backend.py'))

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # maakt..

FASTQ_BESTAND = os.path.join(BASE_DIR, "Data", "ERR2165898.fastq") #vindt waar het document staat
REFERENCE = os.path.join(BASE_DIR, "Data", "reference", "GCF_000006945.2_ASM694v2_genomic.fna") #vindt waar het document staat

@app.route('/')
def input_output_page():
    """
    Functie voor directie naar analyse pagina

    :return: (Response) HTML response met web.html
    """
    return render_template("web.html")

@app.route("/Info_pagina.html")
def information_page():
    """
    Functie voor directie naar informatie pagina

    return: (Response) HTML response met Info_pagina.html
    """
    return render_template("Info_pagina.html")

@app.route("/tools_info.html")
def tools_info_page():
    """
    Functie voor directie naar tools informatie pagina

    return: (Response) HTML response met tools_info.html
    """
    return render_template("tools_info.html")

@app.route("/reference.html")
def reference_gen_page():
    """
    Functie voor directie naar reference genoom pagina

    return: (Response) HTML response met reference.html
    """
    return render_template("reference.html")

@app.route("/stylesheet.css")
def stylesheet():
    """
    Functie voor directie naar stylesheet

    return: (Response) CSS bestand stylesheet.css
    """
    return send_from_directory(os.path.join(app.root_path, "static"), "stylesheet.css")


@app.route("/aanmelden", methods=["POST"])
def aanmelden():
    """
    Functie voor email opgeven

    return: (str) redirect naar web.html
    """
    email = request.form.get("email")
    if email:
        with open("email.txt", "a", encoding="utf-8") as f:
            f.write(email + '\n')
    return redirect("web.html")

@app.route("/web.html", methods=["GET", "POST"])
def output():
    """
    Functie voor het runnen van backend

    :param: (str) informatie vanuit form in web.html

    :return: web.html met argumeten False als er niets mee wordt gedaan.
    """
    if request.method == "GET":
        return render_template("web.html")
    if request.method == "POST":
        chromosoom = request.form.get("chromosoom", "").strip()
        startpunt  = request.form.get("startpunt", "").strip()
        eindpunt   = request.form.get("eindpunt", "").strip()

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
            return render_template("web.html", region_error=region_error)

        kwargs = {
            "fastq_bestand": FASTQ_BESTAND,
            "reference": REFERENCE,
            "threads": 8,
            "N": 5,
            "region": region,
            "tabel_snps": request.form.get("tabel_snps") is not None,
            "plot_mutaties": request.form.get("plot_mutaties") is not None,
            "chroms": request.form.get("plot_chroms") is not None
        }

        run_pipeline(kwargs)
        region_error_mutation = None
        region_error_snp = None
        mutaties, snps_tabel_info, chroms = lezen_vcf()
        mutaties_png = None
        chroms_png = None
        region_error_chroms = None

        if kwargs["plot_mutaties"]:
            if not mutaties:
                region_error_mutation = "Geen mutaties gevonden om te plotten."
            else:
                plot_data = Plot(mutaties)
                mutaties_png = plot_data.maken()
        if kwargs["chroms"]:
            if not chroms:
                region_error_chroms = "Geen mutaties op een chromosoom gevonden"
            else:
                plot_data = Plot(chroms)
                chroms_png = plot_data.opslaan_plot(chroms)
        if kwargs["tabel_snps"]:
            if not snps_tabel_info:
                region_error_snp="Geen snp's gevonden om in tabel te zetten"
        return render_template(
            "web.html",
            **kwargs,
            mutatie_fig= mutaties_png,
            chroms_fig=chroms_png,
            snps_tabel_info=snps_tabel_info,
            region_error_mutation=region_error_mutation,
            region_error_snp=region_error_snp,
            region_error_chroms=region_error_chroms
        )


    return render_template("web.html",
        tabel_snps=False,
        tabel_mutaties=False,
        kwaliteitscore=False,
        vcf_doc=False
    )

if __name__ == "__main__":
    app.run(debug=True, port=5002)
