# Generated by Django 3.1.3 on 2020-11-10 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upd', '0004_version_fw'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='plugin_config',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='version',
            name='changelog',
            field=models.TextField(blank=True, null=True),
        ),
    ]