# Generated by Django 3.0.8 on 2020-07-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_auto_20200722_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainMustBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=64)),
                ('trackid', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_mustbuy',
            },
        ),
    ]