# Generated by Django 3.2.19 on 2023-06-02 22:36

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', help_text=('Обязательное для заполнение поле. Максимальная длинна 7 символов.',), image_field=None, max_length=7, samples=None, unique=True, verbose_name='HEX-код'),
        ),
    ]
