# Generated by Django 5.1.6 on 2025-03-01 07:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cultivos', '0004_alter_cultivo_campo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cultivo',
            name='campo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cultivos.campo'),
        ),
    ]
