# Generated by Django 3.2.4 on 2021-06-30 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20210629_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('colour', models.CharField(max_length=20)),
            ],
        ),
    ]
