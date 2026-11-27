RULE_DEFINITIONS = [
    {
        "kode": "R01",
        "gejala": ["G01", "G03"],
        "kerusakan": "K01",
    },
    {
        "kode": "R02",
        "gejala": ["G02", "G03"],
        "kerusakan": "K01",
    },
    {
        "kode": "R03",
        "gejala": ["G04"],
        "kerusakan": "K01",
    },
    {
        "kode": "R04",
        "gejala": ["G05"],
        "kerusakan": "K02",
    },
    {
        "kode": "R05",
        "gejala": ["G09", "G20"],
        "kerusakan": "K03",
    },
    {
        "kode": "R06",
        "gejala": ["G10", "G20"],
        "kerusakan": "K03",
    },
    {
        "kode": "R07",
        "gejala": ["G11", "G20"],
        "kerusakan": "K03",
    },
    {
        "kode": "R08",
        "gejala": ["G12", "G15"],
        "kerusakan": "K04",
    },
    {
        "kode": "R09",
        "gejala": ["G13", "G14"],
        "kerusakan": "K04",
    },
    {
        "kode": "R10",
        "gejala": ["G16", "G17"],
        "kerusakan": "K05",
    },
    {
        "kode": "R11",
        "gejala": ["G16", "G18"],
        "kerusakan": "K05",
    },
    {
        "kode": "R12",
        "gejala": ["G16", "G19"],
        "kerusakan": "K05",
    },
]


def get_knowledge_base(nama_perangkat):
    from diagnosis.models import Aturan

    aturan_perangkat = (
        Aturan.objects
        .filter(perangkat__nama__iexact=nama_perangkat)
        .select_related("perangkat", "kerusakan")
        .prefetch_related("kondisi__gejala")
        .order_by("kode")
    )

    basis_pengetahuan = []

    for aturan in aturan_perangkat:
        gejala = [
            kondisi.gejala.kode
            for kondisi in aturan.kondisi.all()
        ]

        basis_pengetahuan.append({
            "kode": aturan.kode,
            "perangkat": aturan.perangkat.nama,
            "gejala": gejala,
            "kerusakan_kode": aturan.kerusakan.kode,
            "kerusakan": aturan.kerusakan.nama,
        })

    return basis_pengetahuan
