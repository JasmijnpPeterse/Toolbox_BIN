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
    return render_template('Toolbox_BIN/background_info.html')

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

if __name__ == '__main__':
    app.run()