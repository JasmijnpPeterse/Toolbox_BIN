import unittest, inspect, os, tempfile, backend, pycodestyle
import app as flask_app
import matplotlib.pyplot as plt
from unittest.mock import patch
from backend import lezen_vcf, Tool, Plot

class TestPipeline(unittest.TestCase):
    def setUp(self):
        """
        Wordt voor elke test aangeroepen
        """
        self.client = flask_app.app.test_client()
        flask_app.app.config["TESTING"] = True
        self.tmpdir = tempfile.mkdtemp()
        self.oude_map = os.getcwd()
        os.chdir(self.tmpdir)

    def tearDown(self):
        """
        Wordt na elke test aangeroepen
        """
        os.chdir(self.oude_map)

    def maak_vcf(self, inhoud):
        """
        Maak nep-vcf bestand
        """
        vcf = os.path.join(self.tmpdir, "output.vcf")
        with open(vcf, "w") as fake_vcf:
            fake_vcf.write(inhoud)

    def test_server(self):
        """
        Checkt of de server werkt.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_lege_bestand(self):
        """
        Check of de server een 404 geeft bij een niet ingevoerde bestand of leeg bestand.
        """
        leeg_bestand = self.client.get("/leeg/")
        self.assertEqual(leeg_bestand.status_code, 404)

    def test_fastq_bestand(self):
        """
        Check of de server een 404 geeft bij een niet-fastq bestand.
        """
        fastq_bestand = self.client.get("/upload/verkeerd_bestand.txt")
        self.assertEqual(fastq_bestand.status_code, 404)

    def test_lege_vcf(self):
        """
        Check of lezen_vcf goed werkt met lege VCF.
        """
        self.maak_vcf("##header\n")
        mutaties, snps, chromosoom = lezen_vcf()
        self.assertEqual(mutaties, {})
        self.assertEqual(snps, {})
        self.assertEqual(chromosoom, {})

    def test_resultaat(self):
        """
        Check of de website de gewenste resultaat teruggeeft.
        """
        self.maak_vcf(
            "##fileformat=VCFv4.1\n"
            "NC_001\t1000\t.\tA\tT\t99\t.\t.\n"
        )
        with patch("app.run_pipeline"):
            result = self.client.post("/web.html", data={"tabel_snps": "tabel_snps"})
        self.assertEqual(result.status_code, 200)

    def test_meerdere_mutaties(self):
        """
        Check of lezen_vcf meerdere geldige mutaties pakt.
        """
        self.maak_vcf(
            "##header\n"
            "NC_001\t1000\t.\tA\tT\t99\t.\t.\n"
            "NC_001\t2000\t.\tG\tC\t45\t.\t.\n"
        )
        mutaties, snps, chromosoom = lezen_vcf()
        self.assertEqual(len(snps), 2)

    def test_ontbrekende_info(self):
        """
        Check of de website nog steeds resultaat geeft bij ontbrekende score (de "." in VCF).
        """
        self.maak_vcf(
            "##fileformat=VCFv4.1\n"
            "NC_001\t1000\t.\tA\tT\t99\t.\t.\n"
            "NC_001\t2000\t.\tC\t.\t45\t.\t.\n"
        )
        mutaties, snps_tabel_info, chromosoom = lezen_vcf()
        self.assertIn("1000", snps_tabel_info)
        self.assertNotIn("2000", snps_tabel_info)

    def test_maken_voor_plot(self):
        """
        Check of maken() een resultaat teruggeeft
        :return:
        """
        plt.figure()
        mutaties = {"1000": 1, "2000": 3}
        plot = Plot(mutaties)
        resultaat = plot.maken()

        self.assertIsInstance(resultaat, str)
        self.assertGreater(len(resultaat), 0)

    def test_opslaan_plot(self):
        """
        Check of opslaan_plot() een geldig resultaat teruggeeft.
        """
        mutaties = {"1000": 1, "2000": 3}
        plot = Plot(mutaties)

        fig, ax = plt.subplots()
        ax.bar(mutaties.keys(), mutaties.values())

        resultaat = plot.opslaan_plot(fig)

        self.assertIsInstance(resultaat, str)
        self.assertGreater(len(resultaat), 0)

    def test_class(self):
        """
        Check of de class Tool goed werkt.
        """
        tool = Tool("minimap2", threads = 8, N = 5)
        self.assertEqual(tool.tool, "minimap2")
        self.assertEqual(tool.configs["threads"], 8)
        self.assertEqual(tool.configs["N"], 5)

    def test_tools(self):
        """
        Check of de tools goed werkt.
        """
        self.maak_vcf("##header\n")
        mutaties, snps, chromosoom = lezen_vcf()
        self.assertIsInstance(mutaties, dict)
        self.assertIsInstance(snps, dict)
        self.assertIsInstance(chromosoom, dict)

    def test_functies(self):
        """
        Check of er geen lege functies zijn.
        """
        for naam, obj in inspect.getmembers(backend, inspect.isfunction):
            source = inspect.getsource(obj)
            self.assertNotIn("pass", source, f"{naam}() bevat 'pass'")

    def test_pep8_valide(self):
        """
        Check of alles PEP8 valide is.
        """
        style = pycodestyle.StyleGuide(quiet=True)
        resultaat = style.check_files(["app.py", "backend.py"])

        self.assertEqual(resultaat.total_errors, 0, f"{resultaat.total_errors} PEP8 fouten gevonden")

if __name__ == "__main__":
    unittest.main()