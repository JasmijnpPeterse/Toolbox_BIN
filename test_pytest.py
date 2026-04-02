import inspect, pytest, os, tempfile, backend, pycodestyle
import app as flask_app
import matplotlib.pyplot as plt
from unittest.mock import patch
from backend import lezen_vcf, Tool, Plot


@pytest.fixture()
def client():
    flask_app.app.config['TESTING'] = True
    return flask_app.app.test_client()

@pytest.fixture()
def fake_vcf(tmp_path):
    vcf_inhoud = (
        "##fileformat=VCFv4.1\n"
        "NC_001\t1000\t.\tA\tT\t99\t.\t.\n"  # goede mutatie
        "NC_001\t2000\t.\tC\t.\t45\t.\t.\n"  # ALT is "." --> skip
    )

    vcf_bestand = tmp_path / "output.vcf"
    vcf_bestand.write_text(vcf_inhoud)
    os.chdir(tmp_path)
    return tmp_path

def test_server(client):
    """
    Checkt of de server werkt.
    """
    response = client.get("/")
    assert response.status_code == 200

def test_fastq_bestand(client):
    """
    Check of de server een 404 geeft bij een niet-fastq bestand.
    """
    fastq_bestand = client.get("/upload/verkeerd_bestand.txt")
    assert fastq_bestand.status_code == 404

def test_leeg_bestand(client):
    """
    Check of de server een 404 geeft bij een niet ingevoerde bestand of leeg bestand.
    """
    leeg_bestand = client.get("/leeg/")
    assert leeg_bestand.status_code == 404

def test_resultaat(client, fake_vcf):
    """
    Check of de website de gewenste resultaat teruggeeft.
    """
    with patch("app.run_pipeline"):
        result = client.post("/web.html",
                           data={"tabel_snps": "tabel_snps"})
    assert result.status_code == 200

def test_ontbrekende_info(tmp_path, fake_vcf):
    """
    Check of de website nog steeds resultaat geeft bij ontbrekende score (de "." in VCF).
    """
    mutaties, snps_tabel_info, chromosoom = lezen_vcf()

    assert "1000" in snps_tabel_info
    assert "2000" not in snps_tabel_info

def test_diagram_resultaat():
    """
    Check of de plot de juiste resultaat geeft
    """
    mutaties = {
        "1000": 1,
        "2000": 3
    }
    plt.bar(mutaties.keys(), mutaties.values())

    plot = Plot(mutaties)
    resultaat = plot.maken_plot(mutaties)

    assert isinstance(resultaat, str)
    assert len(resultaat) > 0

def test_class():
    """
    Check of de class Tool goed werkt.
    """
    tool = Tool("minimap2", threads = 8, N = 5)
    assert tool.tool == "minimap2"
    assert tool.configs["threads"] == 8
    assert tool.configs["N"] == 5

def test_tools(tmp_path, fake_vcf):
    """
    Check of de tools goed werkt.
    """
    oude_map = os.getcwd()

    try:
        vcf_bestand = tmp_path / "output.vcf"

        with open(vcf_bestand, "w") as vcf:
            vcf.write("##header\n")

        os.chdir(tmp_path)

        mutaties, snps_tabel_info, chroms = lezen_vcf()
        assert isinstance(mutaties, dict)
        assert isinstance(snps_tabel_info, dict)
        assert isinstance(chroms, dict)

    finally:
        os.chdir(oude_map)

def test_functies():
    """
    Check of er geen lege functies zijn.
    """
    for naam, obj in inspect.getmembers(backend, inspect.isfunction):
        source = inspect.getsource(obj)
        assert "pass" not in source, f"{naam}() bevat 'pass'"

def test_pep8_valide():
    """
    Check of alles PEP8 valide is.
    """
    style = pycodestyle.StyleGuide(quiet=True)
    resultaat = style.check_files(["app.py", "backend.py"])

    assert resultaat.total_errors == 0, f"{resultaat.total_errors} PEP8 fouten gevonden"

