# Generated by Django 4.2.3 on 2023-08-16 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataBanks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.TextField(default=None, null=True)),
                ('descripcion', models.TextField(default=None, null=True)),
                ('numero_documento', models.TextField(default=None, null=True)),
                ('cargos', models.IntegerField(default=None, null=True)),
                ('abonos', models.IntegerField(default=None, null=True)),
                ('saldo', models.IntegerField(default=None, null=True)),
                ('banco', models.TextField(default=None, null=True)),
                ('tipo_transaccion', models.TextField(default=None, null=True)),
            ],
        ),
    ]
