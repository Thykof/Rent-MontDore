from django.shortcuts import render

# Create your views here.

def description(request):
    wishes = [
        "d'un bon souvenir, agréable 2 pièces lumineux avec vue sur le Mont-Dore",
        "de repos, installez-vous sur le balcon et admirez la montagne",
        "de détente, préparez-vous un bon bain",
        "de cuisiner, direction la cuisine où vous trouverez tout le nécessaire",
        "de shopping, produits locaux, artisanaux, articles de sport, décorations, centre-ville à 5 min à pieds",
        "d'une soirée tranquille, de nombreux restaurants vous attendent à 5 min à pied",
        "de grand air, de nombreuses randonnées pour découvrir les cascades, le Sancy...",
        "de ski, le domaine du Sancy et de Super-besse vous proposent de nombreuses pistes, navette gratuite à 20 m",
        "d'une randonnée en raquettes, des départs balisés à 100 m",
        "des bienfaits de l'eau des volcans d'Auvergne, les thermes vous attendent à 300 m"
    ]
    return render(request, 'presentation/description.html', {'wishes': wishes})
