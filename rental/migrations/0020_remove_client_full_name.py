# Generated by Django 5.2 on 2025-05-13 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0019_alter_client_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='full_name',
        ),
    ]
