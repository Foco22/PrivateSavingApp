# Generated by Django 4.2.3 on 2023-10-13 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_classifieddata'),
    ]

    operations = [
        migrations.AddField(
            model_name='databanks',
            name='indicator_not_category',
            field=models.BooleanField(default=False),
        ),
    ]
