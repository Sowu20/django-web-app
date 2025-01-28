from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import redirect
from listings.models import Band
from listings.models import Title
from listings.forms import ContactUsForm, BandForm, ListingForm

def band_list(request):
    bands = Band.objects.all()
    return render(request, 'listings/band_list.html',
                  context={'bands': bands})

def band_detail(request, id):
    band = Band.objects.get(id=id) # Nous insérons cette ligne pour obtenir le Band avec cet id
    return render(request,
                  'listings/band_detail.html',
                  {'band':band})# Mise à jour de cette ligne

def band_create(request): 
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            # Créer une nouvelle "Band" et la sauvegarder dans la db
            band = form.save()
            # Rediriger vers la page de détail du groupe que nous venons de créer
            return redirect('band-detail', band.id)
    else:
        form = BandForm()

    return render(request
                  , 'listings/band_create.html',
                  {'form': form})

def band_update(request, id):
    band = Band.objects.get(id=id)

    if request.method == 'POST':
        form = BandForm(request.POST, instance=band) # On pré-rempli le formulaire avec un groupe existant
        if form.is_valid():
            # mettre à jour le groupe existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return redirect('band-detail', band.id)
    else:
        form = BandForm(instance=band) 

    return render(request,
                  'listings/band_update.html',
                  {'form': form})

def band_delete(request, id):
    band = Band.objects.get(id=id) # Nécessaire pour GET et pour POST

    if request.method == 'POST':
        # Supprimer le groupe de la base de donnée
        band.delete()
        # Rediriger vers la liste des groupes
        return redirect('band-list')
    # Pas besoin de "else" ici, si c'est une commande GET, continuez simplement
    return render(request,
                 'listings/band_delete.html',
                 {'band': band})

def about(request):
    return render(request, 'listings/about-us.html')

def listings(request):
    titles = Title.objects.all()
    return render(request, 'listings/listings.html',
                  context={'titles': titles})

def listings_detail(request, id):
    title = Title.objects.get(id=id) # Nous insérons cette ligne pour obtenir le Title avec cet id
    return render(request,
                  'listings/listings_detail.html',
                  {'title':title})

def listings_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            # Créer une nouvelle "Band" et la sauvegarder dans la db
            title = form.save()
            # Rediriger vers la page de détail du groupe que nous venons de créer
            return redirect('listings-detail', title.id)
    else:
        form = ListingForm()

    return render(request
                  , 'listings/listings_create.html',
                  {'form': form})

def listings_update(request, id):
    title = Title.objects.get(id=id)

    if request.method == 'POST':
        form = ListingForm(request.POST, instance=title)
        if form.is_valid():
            form.save()
            return redirect('listings-detail', title.id)
    else:
        form = ListingForm(instance=title)

    return render(request,
                  'listings/listings_update.html',
                  {'form': form})

def listings_delete(request, id):
    title = Title.objects.get(id=id) # Nécessaire pour GET et pour POST

    if request.method == 'POST':
        # Supprimer le groupe de la base de donnée
        title.delete()
        # Rediriger vers la liste des groupes
        return redirect('listings-list')
    # Pas besoin de "else" ici, si c'est une commande GET, continuez simplement
    return render(request,
                 'listings/listings_delete.html',
                 {'title': title})

def contact(request):
    if request.method == 'POST':
        # Créer une instance de notre formulaire et le remplir avec les données POST
        form = ContactUsForm(request.POST)

        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@merchex.xyz'],
        )
    # Si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return ci-dessous et afficher à nouveau le formulaire (avec des erreurs)
        return redirect('email-sent') # Ajout de l'instruction de retour

    else:
        # Ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm() # Ajout d'un nouveau formulaire ici
    
    return render(request,
                  'listings/contact.html',
                  {'form': form}) # Passe ce formulaire au gabarit