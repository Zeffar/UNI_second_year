
from printshop.models import prajituri, Ambalaj

def run():
    # Create Ambalaj objects if they don't already exist
    Ambalaj.objects.get_or_create(nume="Cutie carton", material="Carton", pret=5.00)
    Ambalaj.objects.get_or_create(nume="Hartie", material="Hartie", pret=1.00)
    Ambalaj.objects.get_or_create(nume="Plastic", material="Plastic", pret=2.00)

    # Create Prajituri objects if they don't already exist
    prajitura1, created = prajituri.objects.get_or_create(
        titlu="Tort de ciocolata",
        descriere="Un tort delicios de ciocolata",
        pret=120.50,
        gramaj=1500,
        tip_produs=prajituri.tipuri_produse_optiuni.cofetarie,
        calorii=3500,
        categ_prajitura=prajituri.categ_prajitura_optiuni.aniversara,
        pt_diabetici=False,
        ambalaj=Ambalaj.objects.get(nume="Cutie carton")
    )
    if created:
        print(f"Created: {prajitura1.titlu}")
    else:
        print(f"Already exists: {prajitura1.titlu}")

    prajitura2, created = prajituri.objects.get_or_create(
        titlu="Ecler cu vanilie",
        descriere="Ecler clasic cu crema de vanilie",
        pret=15.00,
        gramaj=100,
        tip_produs=prajituri.tipuri_produse_optiuni.patiserie,
        calorii=250,
        categ_prajitura=prajituri.categ_prajitura_optiuni.comuna,
        pt_diabetici=False,
        ambalaj=Ambalaj.objects.get(nume="Hartie")
    )
    if created:
        print(f"Created: {prajitura2.titlu}")
    else:
        print(f"Already exists: {prajitura2.titlu}")

    prajitura3, created = prajituri.objects.get_or_create(
        titlu="Inghetata de capsuni",
        descriere="Inghetata racoritoare de capsuni",
        pret=10.00,
        gramaj=200,
        tip_produs=prajituri.tipuri_produse_optiuni.gelaterie,
        calorii=150,
        categ_prajitura=prajituri.categ_prajitura_optiuni.editie_limitata,
        pt_diabetici=True,
        ambalaj=Ambalaj.objects.get(nume="Plastic")
    )
    if created:
        print(f"Created: {prajitura3.titlu}")
    else:
        print(f"Already exists: {prajitura3.titlu}")

    prajitura4, created = prajituri.objects.get_or_create(
        titlu="Cheesecake cu fructe de padure",
        descriere="Cheesecake cremos cu fructe de padure",
        pret=25.00,
        gramaj=250,
        tip_produs=prajituri.tipuri_produse_optiuni.cofetarie,
        calorii=500,
        categ_prajitura=prajituri.categ_prajitura_optiuni.comuna,
        pt_diabetici=False,
        ambalaj=Ambalaj.objects.get(nume="Cutie carton")
    )
    if created:
        print(f"Created: {prajitura4.titlu}")
    else:
        print(f"Already exists: {prajitura4.titlu}")
        
    print("Script completed successfully!")
