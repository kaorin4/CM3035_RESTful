# Generated by Django 3.2.2 on 2021-05-23 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proteindata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pfam',
            name='domain_id',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='taxonomy',
            name='taxa_id',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
