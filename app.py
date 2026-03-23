from flask import Flask,send_from_directory,redirect, url_for, render_template_string, render_template, request, session
import os

app = Flask(__name__)

@app.route('/')
def input_output_page():
    return render_template('web.html')

@app.route('/lucas.html')
def information_page():
    return render_template('lucas.html')

@app.route('/background_info.html')
def tools_info_page():
    return render_template('background_info.html')

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
        with open('emails.txt', 'a') as f:
            f.write(email + '\n')
    return redirect(url_for('lucas'))

@app.route('/web.html', methods=['GET', 'POST'])
def output():
    if request.method == 'GET':
        return render_template('web.html')
    elif request.method == 'POST':
        kwags = {
            'tabel_snps': request.form.get('tabel_snps') is not None,
            'tabel_mutaties': request.form.get('tabel_mutaties') is not None,
            'kwaliteitscore': request.form.get('kwaliteitscore') is not None,
            'vcf_doc': request.form.get('vcf_doc') is not None
        }
        return render_template('web.html', **kwags)

    return render_template('web.html',
        tabel_snps=False,
        tabel_mutaties=False,
        kwaliteitscore=False,
        vcf_doc=False
    )

@app.route("/", methods=["GET", "POST"])
def index():
    # Haal data op
    uitslag = session.get("uitslag")
    show_results = session.get("show_results", False)

    if request.method == "POST":
        # Nieuwe input file
        file = request.files.get('data')
        if file and file.filename != "":
            filename = file.filename
            file.save(os.path.join(upload_folder, filename))

            # Sla het resultaat altijd op (tijdelijk resultaat)
            session["uitslag"] = {
                "filename": filename,
                "status": "Analyse voltooid!"
            }
            session["show_results"] = True

            # Update de upload map
            uitslag = session["uitslag"]
            show_results = True

        else:
            session["uitslag"] = {"status": "FOUT: Geen bestand geselecteerd"}
            session["show_results"] = False


    return render_template('web.html', uitslag=uitslag, show_results=show_results)

if __name__ == '__main__':
    app.run(debug=True)
