import re


KEYWORD_RULES = {
    "G01": [
        "baterai cepat habis",
        "baterainya cepat habis",
        "baterainya boros",
        "baterai boros",
        "baterai cepat low",
        "daya baterai cepat habis",
        "baterai tidak tahan lama",
        "baterai cepat habis meskipun jarang digunakan",
    ],
    "G02": [
        "perangkat mati sendiri",
        "hp mati sendiri",
        "ponsel mati sendiri",
        "mati mendadak",
        "mati tiba tiba",
        "mati padahal baterai masih ada",
        "hp saya mati sendiri",
    ],
    "G03": [
        "persentase baterai turun tidak normal",
        "persentase baterai turun drastis",
        "baterai drop",
        "persen baterai turun drastis",
        "indikator baterai tidak stabil",
        "persentase baterai tidak stabil",
    ],
    "G04": [
        "baterai menggembung",
        "baterai kembung",
        "baterai membesar",
        "baterai menggelembung",
    ],
    "G05": [
        "layar retak",
        "layar pecah",
        "layar hp retak",
        "layar hp pecah",
        "kaca layar retak",
        "kaca layar pecah",
        "screen crack",
    ],
    "G06": [
        "layar bercak hitam",
        "layar hp bercak hitam",
        "bercak hitam di layar",
        "muncul bercak hitam",
        "muncul bercak hitam di layar",
        "noda hitam pada layar",
        "titik hitam di layar",
        "black spot",
    ],
    "G07": [
        "layar bergaris",
        "layar hp bergaris",
        "muncul garis di layar",
        "garis pada layar",
        "warna layar tidak normal",
        "layar berubah warna",
    ],
    "G08": [
        "layar tidak merespons sentuhan",
        "layar tidak bisa disentuh",
        "touchscreen tidak berfungsi",
        "layar tidak responsif setelah jatuh",
        "layar tidak merespons setelah benturan",
    ],
    "G09": [
        "tidak ada suara dari speaker",
        "speaker tidak mengeluarkan suara",
        "speaker mati",
        "tidak keluar suara",
        "speaker tidak bunyi",
        "speaker hp tidak bunyi",
    ],
    "G10": [
        "suara speaker sangat pelan",
        "suara speaker kecil",
        "speaker kurang keras",
        "volume speaker lemah",
    ],
    "G11": [
        "suara speaker pecah",
        "suara speaker terdistorsi",
        "suara speaker kresek",
        "suara speaker berisik",
        "speaker berdengung",
    ],
    "G12": [
        "restart berulang",
        "sering restart",
        "restart sendiri",
        "hp restart terus",
        "ponsel restart terus",
        "boot ulang berulang",
        "hp sering restart sendiri",
    ],
    "G13": [
        "aplikasi sering berhenti",
        "aplikasi keluar sendiri",
        "aplikasi tertutup sendiri",
        "aplikasi crash",
        "aplikasi force close",
    ],
    "G14": [
        "perangkat tidak merespons",
        "hp tidak merespons",
        "ponsel tidak merespons",
        "perangkat macet",
        "hp ngehang",
        "ponsel hang",
        "layar membeku",
    ],
    "G15": [
        "gagal masuk sistem operasi",
        "tidak bisa masuk sistem",
        "gagal booting",
        "tidak bisa booting",
        "berhenti di logo",
        "stuck di logo",
        "bootloop",
    ],
    "G16": [
        "perangkat terasa sangat panas",
        "hp cepat panas",
        "ponsel cepat panas",
        "hp panas",
        "hp saya panas",
        "ponsel panas",
        "ponsel saya panas",
        "perangkat panas",
        "bodi perangkat panas",
        "suhu perangkat tinggi",
        "overheat",
    ],
    "G17": [
        "peringatan suhu terlalu tinggi",
        "peringatan suhu tinggi",
        "notifikasi suhu tinggi",
        "temperature warning",
        "peringatan overheat",
    ],
    "G18": [
        "pengisian daya dihentikan karena suhu tinggi",
        "pengisian daya berhenti karena panas",
        "tidak bisa mengisi daya karena suhu",
        "charging dihentikan karena panas",
    ],
    "G19": [
        "mati otomatis setelah terlalu panas",
        "mati karena terlalu panas",
        "mati otomatis akibat panas",
        "shutdown karena overheat",
    ],
    "G20": [
        "suara tetap bermasalah setelah pemeriksaan pengaturan audio",
        "suara tetap bermasalah setelah pengaturan audio",
        "suaranya tetap bermasalah setelah pengaturan audio",
        "suara tetap bermasalah meskipun pengaturan audio sudah diperiksa",
        "speaker tetap bermasalah setelah pengaturan audio",
        "masalah suara tetap ada setelah pengaturan audio",
        "suara tetap tidak normal setelah pengaturan audio",
    ],
}


NEGATION_WORDS = {
    "tidak",
    "tak",
    "bukan",
    "belum",
    "tanpa",
    "nggak",
    "enggak",
    "gak",
    "ga",
}


def normalize_text(teks):
    if not isinstance(teks, str):
        raise ValueError("Keluhan harus berupa teks.")

    teks = teks.lower()
    teks = re.sub(r"[^a-z0-9\s]", " ", teks)
    teks = re.sub(r"\s+", " ", teks)

    return teks.strip()


def is_negated(teks, posisi_awal):
    bagian_sebelumnya = teks[:posisi_awal]

    klausa = re.split(
        r"\b(?:dan|tetapi|tapi|namun|sedangkan|melainkan)\b",
        bagian_sebelumnya
    )[-1]

    kata_sebelumnya = klausa.split()[-4:]

    return any(
        kata in NEGATION_WORDS
        for kata in kata_sebelumnya
    )


def extract_symptoms(teks):
    teks_normal = normalize_text(teks)

    if not teks_normal:
        raise ValueError("Keluhan tidak boleh kosong.")

    fakta = set()
    kata_kunci_ditemukan = []
    kata_kunci_disangkal = []

    seluruh_kata_kunci = [
        (kode, kata)
        for kode, daftar_kata in KEYWORD_RULES.items()
        for kata in daftar_kata
    ]

    seluruh_kata_kunci.sort(
        key=lambda item: len(item[1]),
        reverse=True
    )

    rentang_ditemukan = []

    for kode_gejala, kata_kunci in seluruh_kata_kunci:
        pola = (
            r"(?<!\w)"
            + re.escape(kata_kunci)
            + r"(?!\w)"
        )

        for hasil in re.finditer(pola, teks_normal):
            rentang = hasil.span()

            bertumpang_tindih = any(
                rentang[0] < akhir and rentang[1] > awal
                for awal, akhir in rentang_ditemukan
            )

            if bertumpang_tindih:
                continue

            if is_negated(teks_normal, rentang[0]):
                kata_kunci_disangkal.append({
                    "kode": kode_gejala,
                    "kata_kunci": kata_kunci,
                })
                rentang_ditemukan.append(rentang)
                continue

            fakta.add(kode_gejala)

            kata_kunci_ditemukan.append({
                "kode": kode_gejala,
                "kata_kunci": kata_kunci,
            })

            rentang_ditemukan.append(rentang)

    return {
        "fakta": sorted(fakta),
        "kata_kunci_ditemukan": kata_kunci_ditemukan,
        "kata_kunci_disangkal": kata_kunci_disangkal,
    }
