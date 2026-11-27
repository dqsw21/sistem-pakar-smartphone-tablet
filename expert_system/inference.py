from diagnosis.models import Perangkat, Gejala
from expert_system.knowledge_base import get_knowledge_base


def forward_chaining(nama_perangkat, fakta_awal):
    if not isinstance(nama_perangkat, str) or not nama_perangkat.strip():
        raise ValueError("Nama perangkat harus diisi.")

    perangkat = Perangkat.objects.filter(
        nama__iexact=nama_perangkat.strip()
    ).first()

    if perangkat is None:
        raise ValueError(f"Perangkat '{nama_perangkat}' tidak dikenal.")

    if isinstance(fakta_awal, (str, bytes)):
        raise ValueError("Fakta gejala harus berupa kumpulan kode gejala.")

    try:
        fakta = set(fakta_awal)
    except TypeError as error:
        raise ValueError("Fakta gejala harus berupa kumpulan kode gejala.") from error

    if any(not isinstance(kode, str) or not kode.strip() for kode in fakta):
        raise ValueError("Setiap fakta harus berupa kode gejala yang valid.")

    gejala_valid = set(
        Gejala.objects.filter(
            perangkat=perangkat,
            kode__in=fakta,
        ).values_list("kode", flat=True)
    )

    gejala_tidak_valid = fakta - gejala_valid

    if gejala_tidak_valid:
        daftar_kode = ", ".join(sorted(gejala_tidak_valid))
        raise ValueError(
            f"Gejala berikut tidak dikenal atau tidak berlaku untuk "
            f"{perangkat.nama}: {daftar_kode}"
        )

    basis_pengetahuan = get_knowledge_base(perangkat.nama)

    aturan_terpenuhi = []
    hasil_diagnosis = {}

    for aturan in basis_pengetahuan:
        kondisi = set(aturan["gejala"])

        if kondisi.issubset(fakta):
            aturan_terpenuhi.append({
                "kode": aturan["kode"],
                "gejala": aturan["gejala"],
                "kerusakan_kode": aturan["kerusakan_kode"],
                "kerusakan": aturan["kerusakan"],
            })

            hasil_diagnosis[aturan["kerusakan_kode"]] = {
                "kode": aturan["kerusakan_kode"],
                "nama": aturan["kerusakan"],
            }

    return {
        "perangkat": perangkat.nama,
        "fakta": sorted(fakta),
        "aturan_terpenuhi": aturan_terpenuhi,
        "diagnosis": list(hasil_diagnosis.values()),
        "peringatan_baterai": "G04" in fakta,
    }
