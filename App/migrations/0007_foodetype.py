# Generated by Django 3.0.8 on 2020-07-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_mainshow'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeid', models.IntegerField(default=1)),
                ('typename', models.CharField(max_length=32)),
                ('childtypenames', models.CharField(max_length=255)),
                ('typesort', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf-foodtype',
            },
        ),
    ]