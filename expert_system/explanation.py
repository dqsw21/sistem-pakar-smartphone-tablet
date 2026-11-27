from diagnosis.models import Gejala, Kerusakan


def build_explanation(hasil_inferensi):
    kode_fakta = hasil_inferensi["fakta"]

    gejala_tersedia = {
        gejala.kode: gejala
        for gejala in Gejala.objects.filter(
            kode__in=kode_fakta
        )
    }

    fakta_pengguna = [
        {
            "kode": kode,
            "nama": gejala_tersedia[kode].nama,
            "deskripsi": gejala_tersedia[kode].deskripsi,
        }
        for kode in kode_fakta
        if kode in gejala_tersedia
    ]

    diagnosis_dijelaskan = []

    for hasil in hasil_inferensi["diagnosis"]:
        kerusakan = Kerusakan.objects.get(
            kode=hasil["kode"]
        )

        aturan_terkait = [
            aturan
            for aturan in hasil_inferensi["aturan_terpenuhi"]
            if aturan["kerusakan_kode"] == hasil["kode"]
        ]

        kode_gejala = sorted({
            kode
            for aturan in aturan_terkait
            for kode in aturan["gejala"]
        })

        gejala_pendukung = [
            {
                "kode": kode,
                "nama": gejala_tersedia[kode].nama,
            }
            for kode in kode_gejala
            if kode in gejala_tersedia
        ]

        diagnosis_dijelaskan.append({
            "kode": kerusakan.kode,
            "nama": kerusakan.nama,
            "deskripsi": kerusakan.deskripsi,
            "rekomendasi": kerusakan.rekomendasi,
            "gejala_pendukung": gejala_pendukung,
            "aturan_terpenuhi": [
                aturan["kode"]
                for aturan in aturan_terkait
            ],
        })

    return {
        "perangkat": hasil_inferensi["perangkat"],
        "fakta_pengguna": fakta_pengguna,
        "diagnosis": diagnosis_dijelaskan,
        "peringatan_baterai": hasil_inferensi["peringatan_baterai"],
        "pesan": (
            "Sistem menemukan kemungkinan kerusakan berdasarkan "
            "gejala dan aturan yang terpenuhi."
            if diagnosis_dijelaskan
            else "Belum ditemukan aturan diagnosis yang sesuai "
                 "dengan gejala yang dipilih."
        ),
    }
