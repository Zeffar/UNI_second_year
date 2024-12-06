from django.db import models
# from django.contrib.auth.models import AbstractUser
import uuid

class Organizator(models.Model):
    nume = models.CharField(max_length=100)
    email = models.EmailField()

class Locatie(models.Model):
    adresa = models.CharField(max_length=255)
    oras = models.CharField(max_length=100)
    judet = models.CharField(max_length=100)
    cod_postal = models.CharField(max_length=10)


class Eveniment(models.Model):
    id_eveniment = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    titlu = models.CharField(max_length=200)
    descriere = models.TextField()
    categ_prajitura  = [
        ('conferinta', 'Conferinta'), ('workshop', 'Workshop'),
        ('intalnire', 'Intalnire'), ('webinar', 'Webinar')]
    tip_eveniment = models.CharField(max_length=50, choices=categ_prajitura )
    organizator = models.ForeignKey(Organizator, on_delete=models.CASCADE, related_name="evenimente")
    locatie = models.ForeignKey(Locatie, on_delete=models.SET_NULL, null=True)
    capacitate = models.PositiveIntegerField()
    este_public = models.BooleanField(default=True)
    imagine = models.ImageField(upload_to='imagini_evenimente/', null=True, blank=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(unique=True)
    data_creare = models.DateTimeField(auto_now_add=True)
    data_actualizare = models.DateTimeField(auto_now=True)


# pret NUMERIC(8,2) NOT NULL,
#    gramaj INT NOT NULL,  
#    tip_produs tipuri_produse DEFAULT 'cofetarie',
#    calorii INT NOT NULL,
#    categorie categ_prajitura DEFAULT 'comuna',
#    pt_diabetici BOOLEAN NOT NULL DEFAULT FALSE,
#    imagine VARCHAR(300),
#    data_adaugare TIMESTAMP DEFAULT current_timestamp
# );

class Ambalaj(models.Model):
    nume = models.CharField(max_length=20, unique=True)
    material = models.CharField(max_length=10, choices=[('plastic', 'Plastic'), ('hartie', 'Hartie'), ('carton', 'Carton')])
    pret = models.DecimalField(max_digits=5, decimal_places=2)



class prajituri(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    titlu = models.CharField(max_length=50, unique=True , null=False)
    descriere = models.TextField()
    pret = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    gramaj = models.IntegerField(null=False)
    class categ_prajitura_optiuni(models.IntegerChoices):
        speciala = 1, 'comanda speciala'
        aniversara = 2, 'aniversara'
        editie_limitata = 3, 'editie limitata'
        copii = 4, 'pentru copii'
        dietetica = 5, 'dietetica'
        comuna = 6,'comuna'
    class tipuri_produse_optiuni(models.IntegerChoices):
        cofetarie = 1, 'cofetarie'
        patiserie = 2, 'patiserie'
        gelaterie = 3, 'gelaterie'
    tip_produs = models.IntegerField(
        choices=tipuri_produse_optiuni.choices,
        default=tipuri_produse_optiuni.cofetarie
    )
    calorii = models.IntegerField(null=False)
    categ_prajitura = models.IntegerField(
        choices=categ_prajitura_optiuni.choices,
        default=categ_prajitura_optiuni.comuna
    )
    pt_diabetici = models.BooleanField(default=False, null=False)
    imagine = models.ImageField(upload_to='imagini_prajituri/', null=True, blank=True)
    data_adaugare = models.DateTimeField(auto_now_add=True)
    ambalaj = models.ForeignKey(Ambalaj, on_delete=models.DO_NOTHING, related_name='prajituri')



# Creati un model pentru entitatea Ingredient cu proprietatile:
# nume - string unic de maxim 30 caractere
# calorii - intreg pozitiv
# unitate - string de maxim 10 caracatere
# Realizati o legatura many-to-many intre Ingredient si Prajitura

class Ingredient(models.Model):
    nume = models.CharField(max_length=30, unique=True)
    calorii = models.PositiveIntegerField()
    unitate = models.CharField(max_length=10)
    prajituri = models.ManyToManyField(prajituri)

# Creati un model pentru entitatea Ambalaj cu proprietatile:
# nume - string unic de maxim 20 caractere
# material string cu optiunile: plastic, hartie, carton
# pret - numar float de 5 cifre din care doua zecimale

# Realizati o legatura one-to-many intre Ambalaj si Prajitura (o prajitura are un singur tip de ambalaj, dar un ambalaj poate corespunde mai multor prajituri)

# Inserati 3 prajituri.

# Insert 3 prajituri


# Realizati o pagina numita prajituri, in care afisati o lista cu datele tuturor prajiturilor din baza de date.



# class CustomUser(AbstractUser):
#     telefon = models.CharField(max_length=15, blank=True)