# Generated by Django 2.2.1 on 2020-02-26 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0002_auto_20200226_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='goods_pic',
            field=models.ImageField(default='img/01.jpg', max_length=200, upload_to='img'),
        ),
    ]
