# Generated by Django 5.1.4 on 2024-12-05 11:30

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ambalaj',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=20, unique=True)),
                ('material', models.CharField(choices=[('plastic', 'Plastic'), ('hartie', 'Hartie'), ('carton', 'Carton')], max_length=10)),
                ('pret', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Locatie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresa', models.CharField(max_length=255)),
                ('oras', models.CharField(max_length=100)),
                ('judet', models.CharField(max_length=100)),
                ('cod_postal', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Organizator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Eveniment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_eveniment', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('titlu', models.CharField(max_length=200)),
                ('descriere', models.TextField()),
                ('tip_eveniment', models.CharField(choices=[('conferinta', 'Conferinta'), ('workshop', 'Workshop'), ('intalnire', 'Intalnire'), ('webinar', 'Webinar')], max_length=50)),
                ('capacitate', models.PositiveIntegerField()),
                ('este_public', models.BooleanField(default=True)),
                ('imagine', models.ImageField(blank=True, null=True, upload_to='imagini_evenimente/')),
                ('website', models.URLField(blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('data_creare', models.DateTimeField(auto_now_add=True)),
                ('data_actualizare', models.DateTimeField(auto_now=True)),
                ('locatie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='aplicatie_exemplu.locatie')),
                ('organizator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evenimente', to='aplicatie_exemplu.organizator')),
            ],
        ),
        migrations.CreateModel(
            name='prajituri',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('titlu', models.CharField(max_length=50, unique=True)),
                ('descriere', models.TextField()),
                ('pret', models.DecimalField(decimal_places=2, max_digits=8)),
                ('gramaj', models.IntegerField()),
                ('tip_produs', models.IntegerField(choices=[(1, 'cofetarie'), (2, 'patiserie'), (3, 'gelaterie')], default=1)),
                ('calorii', models.IntegerField()),
                ('categ_prajitura', models.IntegerField(choices=[(1, 'comanda speciala'), (2, 'aniversara'), (3, 'editie limitata'), (4, 'pentru copii'), (5, 'dietetica'), (6, 'comuna')], default=6)),
                ('pt_diabetici', models.BooleanField(default=False)),
                ('imagine', models.ImageField(blank=True, null=True, upload_to='imagini_prajituri/')),
                ('data_adaugare', models.DateTimeField(auto_now_add=True)),
                ('ambalaj', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='prajituri', to='aplicatie_exemplu.ambalaj')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=30, unique=True)),
                ('calorii', models.PositiveIntegerField()),
                ('unitate', models.CharField(max_length=10)),
                ('prajituri', models.ManyToManyField(to='aplicatie_exemplu.prajituri')),
            ],
        ),
    ]