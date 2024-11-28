from .models import Livre, Utilisateur, Emprunt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_livres(request):
    if request.method == "GET":
        livres = Livre.objects.all().values()
        return JsonResponse(list(livres), safe=False)
def get_livre(request, id):
    if request.method == "GET":
        try:
            livre = Livre.objects.get(id=id)
            return JsonResponse({
                "id": livre.id,
                "titre": livre.titre,
                "auteur": livre.auteur,
                "isbn": livre.isbn,
                "genre": livre.genre,
                "emplacement": livre.emplacement,
                "disponible": livre.disponible
            })
        except Livre.DoesNotExist:
            return JsonResponse({"error": "Livre non trouvé"}, status=404)
@csrf_exempt
def add_livre(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        # Vérifier si un livre avec le même ISBN existe déjà
        if Livre.objects.filter(isbn=data.get('isbn')).exists():
            return JsonResponse({"error": "Un livre avec ce ISBN existe déjà."}, status=400)

        livre = Livre.objects.create(
            titre=data.get('titre'),
            auteur=data.get('auteur'),
            isbn=data.get('isbn'),
            genre=data.get('genre'),
            emplacement=data.get('emplacement'),
            disponible=data.get('disponible')
        )

        return JsonResponse({
            "id": livre.id,
            "titre": livre.titre,
            "auteur": livre.auteur,
            "isbn": livre.isbn,
            "genre": livre.genre,
            "emplacement": livre.emplacement,
            "disponible": livre.disponible
        }, status=201)

@csrf_exempt
def update_livre(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            livre = Livre.objects.get(id=id)
        except Livre.DoesNotExist:
            return JsonResponse({"error": "Livre non trouvé"}, status=404)
        
        livre.titre = data.get('titre', livre.titre)
        livre.auteur = data.get('auteur', livre.auteur)
        livre.isbn = data.get('isbn', livre.isbn)
        livre.genre = data.get('genre', livre.genre)
        livre.emplacement = data.get('emplacement', livre.emplacement)
        livre.disponible = data.get('disponible', livre.disponible)
        livre.save()

        return JsonResponse({
            "id": livre.id,
            "titre": livre.titre,
            "auteur": livre.auteur,
            "isbn": livre.isbn,
            "genre": livre.genre,
            "emplacement": livre.emplacement,
            "disponible": livre.disponible
        })
@csrf_exempt
def delete_livre(request, id):
    if request.method == "DELETE":
        try:
            livre = Livre.objects.get(id=id)
            livre.delete()
            return JsonResponse({"message": "Livre supprimé avec succès"}, status=204)
        except Livre.DoesNotExist:
            return JsonResponse({"error": "Livre non trouvé"}, status=404)
def get_utilisateurs(request):
    if request.method == "GET":
        utilisateurs = Utilisateur.objects.all().values()
        return JsonResponse(list(utilisateurs), safe=False)
def get_utilisateur(request, id):
    if request.method == "GET":
        try:
            utilisateur = Utilisateur.objects.get(id=id)
            return JsonResponse({
                "id": utilisateur.id,
                "username": utilisateur.username,
                "email": utilisateur.email,
                "date_creation": utilisateur.date_creation
            })
        except Utilisateur.DoesNotExist:
            return JsonResponse({"error": "Utilisateur non trouvé"}, status=404)
@csrf_exempt
def add_utilisateur(request):
    if request.method == "POST":
        data = json.loads(request.body)
        utilisateur = Utilisateur.objects.create(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            date_creation=data.get('date_creation')
        )
        return JsonResponse({
            "id": utilisateur.id,
            "username": utilisateur.username,
            "email": utilisateur.email,
            "date_creation": utilisateur.date_creation
        }, status=201)
@csrf_exempt
def update_utilisateur(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            utilisateur = Utilisateur.objects.get(id=id)
        except Utilisateur.DoesNotExist:
            return JsonResponse({"error": "Utilisateur non trouvé"}, status=404)
        
        utilisateur.username = data.get('username', utilisateur.username)
        utilisateur.password = data.get('password', utilisateur.password)
        utilisateur.email = data.get('email', utilisateur.email)
        utilisateur.date_creation = data.get('date_creation', utilisateur.date_creation)
        utilisateur.save()

        return JsonResponse({
            "id": utilisateur.id,
            "username": utilisateur.username,
            "email": utilisateur.email,
            "date_creation": utilisateur.date_creation
        })
@csrf_exempt
def delete_utilisateur(request, id):
    if request.method == "DELETE":
        try:
            utilisateur = Utilisateur.objects.get(id=id)
            utilisateur.delete()
            return JsonResponse({"message": "Utilisateur supprimé avec succès"}, status=204)
        except Utilisateur.DoesNotExist:
            return JsonResponse({"error": "Utilisateur non trouvé"}, status=404)
def get_emprunts(request):
    if request.method == "GET":
        emprunts = Emprunt.objects.all().values()
        return JsonResponse(list(emprunts), safe=False)
def get_emprunt(request, id):
    if request.method == "GET":
        try:
            emprunt = Emprunt.objects.get(id=id)
            return JsonResponse({
                "id": emprunt.id,
                "livre": emprunt.livre.titre,
                "utilisateur": emprunt.utilisateur.username,
                "date_emprunt": emprunt.date_emprunt,
                "date_retour": emprunt.date_retour
            })
        except Emprunt.DoesNotExist:
            return JsonResponse({"error": "Emprunt non trouvé"}, status=404)

@csrf_exempt
def add_emprunt(request):
    if request.method == "POST":
        try:
            # Récupérer les données de la requête
            data = json.loads(request.body)

            # Valider les champs nécessaires
            livre = data.get("livre")
            utilisateur = data.get("utilisateur")
            date_emprunt = data.get("date_emprunt")
            date_retour = data.get("date_retour")

            if not livre or not utilisateur or not date_emprunt:
                return JsonResponse(
                    {"error": "Les champs 'livre_id', 'utilisateur_id' et 'date_emprunt' sont requis."},
                    status=400,
                )

            # Vérifier si le livre existe
            try:
                livre = Livre.objects.get(id=livre)
            except Livre.DoesNotExist:
                return JsonResponse({"error": "Livre non trouvé."}, status=404)

            # Vérifier si l'utilisateur existe
            try:
                utilisateur = Utilisateur.objects.get(id=utilisateur)
            except Utilisateur.DoesNotExist:
                return JsonResponse({"error": "Utilisateur non trouvé."}, status=404)

            # Créer l'emprunt
            emprunt = Emprunt.objects.create(
                livre=livre,
                utilisateur=utilisateur,
                date_emprunt=date_emprunt,
                date_retour=date_retour,
            )

            # Retourner une réponse JSON avec les données de l'emprunt
            return JsonResponse(
                {
                    "id": emprunt.id,
                    "livre": emprunt.livre.titre,
                    "utilisateur": emprunt.utilisateur.username,
                    "date_emprunt": emprunt.date_emprunt,
                    "date_retour": emprunt.date_retour,
                },
                status=201,
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Requête invalide, données JSON attendues."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée."}, status=405)
@csrf_exempt
def update_emprunt(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            emprunt = Emprunt.objects.get(id=id)
        except Emprunt.DoesNotExist:
            return JsonResponse({"error": "Emprunt non trouvé"}, status=404)
        
        emprunt.livre_id = data.get('livre_id', emprunt.livre_id)
        emprunt.utilisateur_id = data.get('utilisateur_id', emprunt.utilisateur_id)
        emprunt.date_emprunt = data.get('date_emprunt', emprunt.date_emprunt)
        emprunt.date_retour = data.get('date_retour', emprunt.date_retour)
        emprunt.save()

        return JsonResponse({
            "id": emprunt.id,
            "livre_id": emprunt.livre_id,
            "utilisateur_id": emprunt.utilisateur_id,
            "date_emprunt": emprunt.date_emprunt,
            "date_retour": emprunt.date_retour
        })
@csrf_exempt
def delete_emprunt(request, id):
    if request.method == "DELETE":
        try:
            emprunt = Emprunt.objects.get(id=id)
            emprunt.delete()
            return JsonResponse({"message": "Emprunt supprimé avec succès"}, status=204)
        except Emprunt.DoesNotExist:
            return JsonResponse({"error": "Emprunt non trouvé"}, status=404)


