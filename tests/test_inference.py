from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from diagnosis.models import Aturan
from expert_system.inference import forward_chaining


class ForwardChainingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("isi_data_awal", stdout=StringIO())
        call_command("isi_kerusakan_awal", stdout=StringIO())
        call_command("isi_aturan_awal", stdout=StringIO())

    def test_aturan_aktif_jika_semua_gejala_terpenuhi(self):
        hasil = forward_chaining("Smartphone", ["G01", "G03"])

        self.assertEqual(len(hasil["aturan_terpenuhi"]), 1)
        self.assertEqual(hasil["aturan_terpenuhi"][0]["kode"], "R01-SM")
        self.assertEqual(hasil["diagnosis"][0]["kode"], "K01")

    def test_aturan_tidak_aktif_jika_gejala_tidak_lengkap(self):
        hasil = forward_chaining("Smartphone", ["G01"])

        self.assertEqual(hasil["aturan_terpenuhi"], [])
        self.assertEqual(hasil["diagnosis"], [])

    def test_diagnosis_yang_sama_tidak_digandakan(self):
        hasil = forward_chaining("Smartphone", ["G01", "G02", "G03"])

        self.assertEqual(len(hasil["aturan_terpenuhi"]), 2)
        self.assertEqual(len(hasil["diagnosis"]), 1)
        self.assertEqual(hasil["diagnosis"][0]["kode"], "K01")

    def test_aturan_tablet_terpisah_dari_smartphone(self):
        hasil = forward_chaining("Tablet", ["G01", "G03"])

        self.assertEqual(hasil["aturan_terpenuhi"][0]["kode"], "R01-TB")
        self.assertEqual(
            Aturan.objects.filter(perangkat__nama="Tablet").count(),
            12,
        )

    def test_baterai_menggembung_memicu_peringatan(self):
        hasil = forward_chaining("Tablet", ["G04"])

        self.assertTrue(hasil["peringatan_baterai"])
        self.assertEqual(hasil["diagnosis"][0]["kode"], "K01")

    def test_perangkat_tidak_dikenal_ditolak(self):
        with self.assertRaisesRegex(ValueError, "tidak dikenal"):
            forward_chaining("Laptop", ["G01"])

    def test_kode_gejala_tidak_dikenal_ditolak(self):
        with self.assertRaisesRegex(ValueError, "tidak dikenal"):
            forward_chaining("Smartphone", ["G99"])
