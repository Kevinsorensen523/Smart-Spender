from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)  # Nama barang
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Harga barang

    def __str__(self):
        return self.name
