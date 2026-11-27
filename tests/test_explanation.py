from django.test import TestCase

from diagnosis.models import Perangkat, Gejala, Kerusakan
from expert_system.inference import forward_chaining
from expert_system.explanation import build_explanation


class ExplanationTests(TestCase):
    def setUp(self):
        self.smartphone = Perangkat.objects.create(
            nama="Smartphone"
        )

        self.gejala_1 = Gejala.objects.create(
            kode="G01",
            nama="Baterai cepat habis",
            deskripsi="Daya baterai cepat berkurang."
        )

        self.gejala_3 = Gejala.objects.create(
            kode="G03",
            nama="Persentase baterai turun tidak normal",
            deskripsi="Persentase baterai turun secara tidak wajar."
        )

        self.gejala_1.perangkat.add(self.smartphone)
        self.gejala_3.perangkat.add(self.smartphone)

        self.kerusakan = Kerusakan.objects.create(
            kode="K01",
            nama="Battery Issue",
            deskripsi="Gangguan pada baterai.",
            rekomendasi="Periksa kondisi baterai."
        )

    def test_penjelasan_menampilkan_diagnosis(self):
        from diagnosis.models import Aturan, KondisiAturan

        aturan = Aturan.objects.create(
            kode="R01-SM",
            perangkat=self.smartphone,
            kerusakan=self.kerusakan
        )

        KondisiAturan.objects.create(
            aturan=aturan,
            gejala=self.gejala_1
        )

        KondisiAturan.objects.create(
            aturan=aturan,
            gejala=self.gejala_3
        )

        hasil = forward_chaining(
            "Smartphone",
            ["G01", "G03"]
        )

        penjelasan = build_explanation(hasil)

        self.assertEqual(len(penjelasan["diagnosis"]), 1)
        self.assertEqual(
            penjelasan["diagnosis"][0]["nama"],
            "Battery Issue"
        )
        self.assertEqual(
            penjelasan["diagnosis"][0]["aturan_terpenuhi"],
            ["R01-SM"]
        )
        self.assertEqual(
            len(penjelasan["fakta_pengguna"]),
            2
        )

    def test_penjelasan_tanpa_diagnosis(self):
        hasil = forward_chaining(
            "Smartphone",
            ["G01"]
        )

        penjelasan = build_explanation(hasil)

        self.assertEqual(len(penjelasan["diagnosis"]), 0)
        self.assertIn(
            "Belum ditemukan aturan diagnosis",
            penjelasan["pesan"]
        )
