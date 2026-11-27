from django.test import SimpleTestCase

from expert_system.keyword_extractor import extract_symptoms


class KeywordExtractorTests(SimpleTestCase):

    def test_mengenali_beberapa_gejala_dalam_satu_keluhan(self):
        hasil = extract_symptoms(
            "Layar HP retak dan muncul bercak hitam."
        )

        self.assertEqual(
            hasil["fakta"],
            ["G05", "G06"]
        )

    def test_mengenali_gejala_speaker_dan_pemeriksaan_audio(self):
        hasil = extract_symptoms(
            "Speaker tidak bunyi dan suaranya tetap bermasalah "
            "setelah pengaturan audio."
        )

        self.assertEqual(
            hasil["fakta"],
            ["G09", "G20"]
        )

    def test_mengenali_baterai_dan_mengabaikan_gejala_yang_disangkal(self):
        hasil = extract_symptoms(
            "HP saya tidak panas, tetapi baterainya cepat habis."
        )

        self.assertEqual(
            hasil["fakta"],
            ["G01"]
        )

    def test_mengabaikan_restart_yang_disangkal(self):
        hasil = extract_symptoms(
            "HP saya panas, tetapi tidak mengalami restart."
        )

        self.assertEqual(
            hasil["fakta"],
            ["G16"]
        )

    def test_mengabaikan_keluhan_negatif(self):
        hasil = extract_symptoms(
            "HP saya tidak panas."
        )

        self.assertEqual(hasil["fakta"], [])

    def test_keluhan_tanpa_kata_kunci(self):
        hasil = extract_symptoms(
            "HP saya terasa kurang nyaman digunakan."
        )

        self.assertEqual(hasil["fakta"], [])

    def test_keluhan_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            extract_symptoms("")

    def test_input_bukan_teks_ditolak(self):
        with self.assertRaises(ValueError):
            extract_symptoms(123)
