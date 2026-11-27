from django.core.management.base import BaseCommand
from diagnosis.models import Kerusakan


class Command(BaseCommand):
    help = "Mengisi data awal kategori kerusakan"

    def handle(self, *args, **options):
        data_kerusakan = [
            (
                "K01",
                "Battery Issue",
                "Gangguan pada baterai yang dapat menyebabkan daya cepat habis, penurunan persentase baterai tidak normal, atau perangkat mati secara tiba-tiba.",
                "Periksa kondisi baterai dan kebiasaan pengisian daya. Jika baterai menggembung, hentikan penggunaan dan pengisian daya, jangan menekan atau menusuk baterai, serta serahkan kepada teknisi yang kompeten."
            ),
            (
                "K02",
                "Screen Crack",
                "Kerusakan fisik pada bagian layar yang dapat berupa kaca retak, layar pecah, bercak hitam, atau gangguan tampilan setelah benturan.",
                "Hindari menekan bagian layar yang rusak. Gunakan pelindung sementara jika memungkinkan dan bawa perangkat ke teknisi untuk pemeriksaan serta penggantian komponen layar."
            ),
            (
                "K03",
                "Speaker Malfunction",
                "Gangguan pada sistem keluaran suara yang dapat menyebabkan suara tidak terdengar, terlalu pelan, atau terdengar pecah.",
                "Periksa pengaturan volume, mode senyap, dan koneksi perangkat audio. Jika gangguan tetap terjadi, lakukan pemeriksaan speaker dan komponen audio oleh teknisi."
            ),
            (
                "K04",
                "Software Crash",
                "Gangguan perangkat lunak yang dapat menyebabkan aplikasi berhenti sendiri, perangkat tidak merespons, restart berulang, atau gagal masuk ke sistem operasi.",
                "Coba mulai ulang perangkat dan periksa pembaruan sistem serta aplikasi. Cadangkan data jika memungkinkan sebelum melakukan reset pabrik atau pemeriksaan lebih lanjut."
            ),
            (
                "K05",
                "Overheating",
                "Kondisi ketika suhu perangkat meningkat secara berlebihan sehingga dapat mengganggu kinerja, menghentikan pengisian daya, atau menyebabkan perangkat mati otomatis.",
                "Hentikan aktivitas berat, lepaskan pengisi daya jika perangkat terlalu panas, dan biarkan perangkat mendingin di tempat yang aman. Jika panas berulang atau disertai kerusakan baterai, hentikan penggunaan dan minta pemeriksaan teknisi."
            ),
        ]

        for kode, nama, deskripsi, rekomendasi in data_kerusakan:
            Kerusakan.objects.update_or_create(
                kode=kode,
                defaults={
                    "nama": nama,
                    "deskripsi": deskripsi,
                    "rekomendasi": rekomendasi,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Berhasil mengisi {Kerusakan.objects.count()} kategori kerusakan."
            )
        )
