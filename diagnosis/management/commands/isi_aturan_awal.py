from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from diagnosis.models import (
    Perangkat,
    Gejala,
    Kerusakan,
    Aturan,
    KondisiAturan,
)
from expert_system.knowledge_base import RULE_DEFINITIONS


class Command(BaseCommand):
    help = "Mengisi aturan awal sistem pakar"

    @transaction.atomic
    def handle(self, *args, **options):
        perangkat_data = [
            ("Smartphone", "SM"),
            ("Tablet", "TB"),
        ]

        perangkat_tersedia = {
            perangkat.nama: perangkat
            for perangkat in Perangkat.objects.all()
        }

        gejala_tersedia = {
            gejala.kode: gejala
            for gejala in Gejala.objects.all()
        }

        kerusakan_tersedia = {
            kerusakan.kode: kerusakan
            for kerusakan in Kerusakan.objects.all()
        }

        for nama_perangkat, _ in perangkat_data:
            if nama_perangkat not in perangkat_tersedia:
                raise CommandError(
                    f"Perangkat {nama_perangkat} belum tersedia."
                )

        for definisi in RULE_DEFINITIONS:
            kode_kerusakan = definisi["kerusakan"]

            if kode_kerusakan not in kerusakan_tersedia:
                raise CommandError(
                    f"Kerusakan {kode_kerusakan} belum tersedia."
                )

            for kode_gejala in definisi["gejala"]:
                if kode_gejala not in gejala_tersedia:
                    raise CommandError(
                        f"Gejala {kode_gejala} belum tersedia."
                    )

        jumlah_aturan = 0
        jumlah_kondisi = 0

        for nama_perangkat, akhiran in perangkat_data:
            perangkat = perangkat_tersedia[nama_perangkat]

            for definisi in RULE_DEFINITIONS:
                kode_aturan = f"{definisi['kode']}-{akhiran}"

                aturan, _ = Aturan.objects.update_or_create(
                    kode=kode_aturan,
                    defaults={
                        "perangkat": perangkat,
                        "kerusakan": kerusakan_tersedia[
                            definisi["kerusakan"]
                        ],
                    },
                )

                KondisiAturan.objects.filter(
                    aturan=aturan
                ).delete()

                kondisi_baru = [
                    KondisiAturan(
                        aturan=aturan,
                        gejala=gejala_tersedia[kode_gejala],
                    )
                    for kode_gejala in definisi["gejala"]
                ]

                KondisiAturan.objects.bulk_create(kondisi_baru)

                jumlah_aturan += 1
                jumlah_kondisi += len(kondisi_baru)

        self.stdout.write(
            self.style.SUCCESS(
                f"Berhasil mengisi {jumlah_aturan} record aturan "
                f"dan {jumlah_kondisi} kondisi aturan."
            )
        )
