from django.core.management.base import BaseCommand
from diagnosis.models import Perangkat, Gejala


class Command(BaseCommand):
    help = "Mengisi data awal perangkat dan gejala"

    def handle(self, *args, **options):
        smartphone, _ = Perangkat.objects.get_or_create(
            nama="Smartphone"
        )

        tablet, _ = Perangkat.objects.get_or_create(
            nama="Tablet"
        )

        data_gejala = [
            ("G01", "Baterai cepat habis", "Daya baterai berkurang lebih cepat dari biasanya."),
            ("G02", "Perangkat mati meskipun baterai masih tersedia", "Perangkat mati ketika indikator baterai masih menunjukkan daya."),
            ("G03", "Persentase baterai turun secara tidak normal", "Persentase baterai mengalami penurunan yang tidak wajar."),
            ("G04", "Baterai menggembung", "Kondisi fisik baterai terlihat membesar atau menggembung."),
            ("G05", "Kaca layar retak atau pecah", "Permukaan kaca layar terlihat mengalami keretakan atau pecah."),
            ("G06", "Layar memiliki bercak hitam", "Layar menampilkan bercak hitam seperti tinta."),
            ("G07", "Layar menampilkan garis atau warna tidak normal", "Tampilan layar menunjukkan garis atau perubahan warna yang tidak wajar."),
            ("G08", "Layar tidak merespons sentuhan setelah benturan", "Layar tidak merespons sentuhan setelah perangkat mengalami benturan."),
            ("G09", "Tidak ada suara dari speaker", "Speaker tidak mengeluarkan suara ketika digunakan."),
            ("G10", "Suara speaker sangat pelan", "Suara speaker tetap pelan meskipun volume telah dinaikkan."),
            ("G11", "Suara speaker pecah atau terdistorsi", "Suara yang dihasilkan speaker terdengar pecah atau tidak jernih."),
            ("G12", "Perangkat melakukan restart berulang", "Perangkat terus melakukan restart tanpa perintah pengguna."),
            ("G13", "Aplikasi sering berhenti sendiri", "Aplikasi sering mengalami crash atau tertutup secara tiba-tiba."),
            ("G14", "Perangkat berhenti merespons", "Perangkat tidak merespons perintah atau sentuhan saat digunakan."),
            ("G15", "Perangkat gagal masuk ke sistem operasi", "Perangkat tidak berhasil menyelesaikan proses masuk ke sistem operasi."),
            ("G16", "Perangkat terasa sangat panas", "Suhu perangkat terasa jauh lebih panas dari kondisi penggunaan normal."),
            ("G17", "Muncul peringatan suhu terlalu tinggi", "Perangkat menampilkan peringatan bahwa suhu terlalu tinggi."),
            ("G18", "Pengisian daya dihentikan karena suhu tinggi", "Perangkat menghentikan proses pengisian daya akibat suhu tinggi."),
            ("G19", "Perangkat mati otomatis setelah terlalu panas", "Perangkat mati secara otomatis setelah mengalami peningkatan suhu."),
        ]

        for kode, nama, deskripsi in data_gejala:
            gejala, _ = Gejala.objects.update_or_create(
                kode=kode,
                defaults={
                    "nama": nama,
                    "deskripsi": deskripsi,
                },
            )
            gejala.perangkat.set([smartphone, tablet])

        self.stdout.write(
            self.style.SUCCESS(
                f"Berhasil mengisi {Perangkat.objects.count()} perangkat "
                f"dan {Gejala.objects.count()} gejala."
            )
        )
