import os

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    plugin = models.CharField(max_length=255)

    def __str__(self):
        return f'Product: {self.name}'


def fw_upload_to(instance, filename):
    return os.path.join('fw', str(instance.id), filename)


class Version(models.Model):

    version = models.CharField(max_length=255, null=False)
    fw_link = models.TextField()
    fw = models.FileField(upload_to=fw_upload_to)
    date_published = models.DateField(null=True, blank=True)
    last_pulled = models.DateTimeField(null=True, blank=True)
    indexed = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(Product, models.PROTECT)

    def __str__(self):
        return f'Version: {self.version} of {self.product.name}'

    def get_fw_filename(self):
        if self.fw:
            return os.path.basename(self.fw.name)

    def pulled(self):
        if self.fw:
            return True
        return False