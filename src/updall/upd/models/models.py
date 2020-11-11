import os

from django.db import models
from django.utils.functional import lazy

from plugins.base import PluginCollection


def plugin_choices():
    """
    get available plugins
    :return:
    """
    return [(p.get_cls_str(), p.name,) for p in PluginCollection('plugins').plugins]


class Product(models.Model):
    """
    represents a product to check on
    """

    name = models.CharField(max_length=255)
    plugin = models.CharField(max_length=255, choices=lazy(plugin_choices, list)())
    plugin_config = models.TextField(blank=True)
    notify = models.BooleanField(default=True)

    def __str__(self):
        return f'Product: {self.name}'


def fw_upload_to(instance, filename):
    """
    get internal fw download string in update-all-the-things
    :param instance:
    :param filename:
    :return:
    """
    return os.path.join('fw', str(instance.id), filename)


class Version(models.Model):
    """
    represents a firmware version linked to a product.
    """

    version = models.CharField(max_length=255, null=False)
    fw_link = models.TextField()
    fw = models.FileField(upload_to=fw_upload_to)
    changelog = models.TextField(null=True, blank=True)
    date_published = models.DateField(null=True, blank=True)
    last_pulled = models.DateTimeField(null=True, blank=True)
    pullable = models.BooleanField(default=True)
    indexed = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(Product, models.PROTECT)

    def __str__(self):
        return f'Version: {self.version} of {self.product.name}'

    def get_fw_filename(self):
        """
        get the fw filename from model
        :return:
        """
        if self.fw:
            return os.path.basename(self.fw.name)
        return None

    def pulled(self):
        """check if fw is pulled"""
        if self.fw:
            return True
        return False

    class Meta:
        ordering = ['-indexed']
