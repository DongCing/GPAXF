# Generated by Django 3.0.8 on 2020-07-24 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_goods'),
    ]

    operations = [
        migrations.CreateModel(
            name='AXFUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_username', models.CharField(max_length=32, unique=True)),
                ('u_password', models.CharField(max_length=256)),
                ('u_email', models.CharField(max_length=64, unique=True)),
                ('u_icon', models.ImageField(upload_to='icons/%Y/%m/%d/')),
                ('is_active', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'axf_user',
            },
        ),
    ]