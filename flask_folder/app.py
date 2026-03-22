from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = "(secret key)"

# Zorg dat de map voor uploads bestaat
upload_folder = 'Uploads'
os.makedirs(upload_folder, exist_ok=True)

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

            # Parameters form
            opties = {
                "snps": request.form.get("tabel_snps"),
                "mutaties": request.form.get("mutations"),
                "scores": request.form.get("qualityscore"),
                "vcf": request.form.get("vcf_file")
            }

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

    uitslag = session.get("uitslag")
    show_results = session.get("show_results", False)

    return render_template('web.html', uitslag=uitslag, show_results=show_results)

@app.route("/about")
def about():
    return render_template("lucas.html")

@app.route("/tools")
def tools():
    return render_template("background_info.html")

@app.route("/makers")
def makers():
    return render_template("lucas.html")

@app.route("/onderzoek")
def onderzoek():
    return render_template("lucas.html")

@app.route("/reference")
def reference():
    return render_template("reference.html")

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)