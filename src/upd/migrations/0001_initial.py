# Generated by Django 3.1.3 on 2020-11-11 20:17

from django.db import migrations, models
import django.db.models.deletion
from upd.models.models import fw_upload_to


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_upd.notification_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('plugin', models.CharField(choices=[('plugins.ubiquiti.base.UbiquitiFirmwarePlugin', 'Ubiquiti Firmware Plugin'), ('plugins.supermicro.base.SupermicroBIOSFirmwarePlugin', 'Supermicro BIOS Firmware Plugin'), ('plugins.supermicro.base.SupermicroBMCFirmwarePlugin', 'Supermicro BMC Firmware Plugin'), ('plugins.grandstream.base.GrandstreamFirmwarePlugin', 'Grandstream Firmware Plugin'), ('plugins.zyxel.http.ZyxelFirmwareHTTPPlugin', 'ZyXEL HTTP Firmware Plugin')], max_length=255)),
                ('plugin_config', models.TextField(blank=True)),
                ('notify', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='upd.notification')),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('upd.notification',),
        ),
        migrations.CreateModel(
            name='PushoverNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='upd.notification')),
                ('name', models.CharField(max_length=256)),
                ('token', models.CharField(max_length=256)),
                ('user', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('upd.notification',),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=255)),
                ('fw_link', models.TextField()),
                ('fw', models.FileField(upload_to=fw_upload_to)),
                ('changelog', models.TextField(blank=True, null=True)),
                ('date_published', models.DateField(blank=True, null=True)),
                ('last_pulled', models.DateTimeField(blank=True, null=True)),
                ('pullable', models.BooleanField(default=True)),
                ('indexed', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='upd.product')),
            ],
            options={
                'ordering': ['-indexed'],
            },
        ),
    ]
