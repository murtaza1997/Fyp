# Generated by Django 2.1.14 on 2019-11-29 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myCart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProCategory',
            fields=[
                ('ProductCatID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
