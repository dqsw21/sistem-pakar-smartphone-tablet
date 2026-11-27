from django.db import models


class Perangkat(models.Model):
    nama = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["nama"]

    def __str__(self):
        return self.nama


class Gejala(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=150)
    deskripsi = models.TextField()
    perangkat = models.ManyToManyField(
        Perangkat,
        related_name="gejala"
    )

    class Meta:
        ordering = ["kode"]

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class Kerusakan(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField()
    rekomendasi = models.TextField()

    class Meta:
        ordering = ["kode"]

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class Aturan(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    perangkat = models.ForeignKey(
        Perangkat,
        on_delete=models.CASCADE,
        related_name="aturan"
    )
    kerusakan = models.ForeignKey(
        Kerusakan,
        on_delete=models.CASCADE,
        related_name="aturan"
    )

    class Meta:
        ordering = ["kode"]

    def __str__(self):
        return self.kode


class KondisiAturan(models.Model):
    aturan = models.ForeignKey(
        Aturan,
        on_delete=models.CASCADE,
        related_name="kondisi"
    )
    gejala = models.ForeignKey(
        Gejala,
        on_delete=models.CASCADE,
        related_name="digunakan_dalam_aturan"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["aturan", "gejala"],
                name="unik_gejala_dalam_aturan"
            )
        ]

    def __str__(self):
        return f"{self.aturan.kode} - {self.gejala.kode}"
