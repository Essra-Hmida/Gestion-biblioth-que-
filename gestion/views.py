from .models import Livre, Utilisateur, Emprunt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
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
        try:
            data = json.loads(request.body)

            # Vérifier si l'utilisateur demandeur est un administrateur
            requester_id = data.get("requester_id")  # ID de l'utilisateur demandeur
            try:
                requester = Utilisateur.objects.get(id=requester_id)
                if not requester.is_admin:
                    return JsonResponse({"error": "Permission refusée : seuls les administrateurs peuvent ajouter un livre."}, status=403)
            except Utilisateur.DoesNotExist:
                return JsonResponse({"error": "Utilisateur demandeur non trouvé."}, status=404)

            # Ajouter le livre
            livre = Livre.objects.create(
                titre=data.get("titre"),
                auteur=data.get("auteur"),
                isbn=data.get("isbn"),
                genre=data.get("genre"),
                emplacement=data.get("emplacement"),
                disponible=data.get("disponible", True)
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

        except json.JSONDecodeError:
            return JsonResponse({"error": "Requête invalide, données JSON attendues."}, status=400)


@csrf_exempt
def update_livre(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)

            # Vérifier si l'utilisateur demandeur est un administrateur
            requester_id = data.get("requester_id")  # ID de l'utilisateur demandeur
            try:
                requester = Utilisateur.objects.get(id=requester_id)
                if not requester.is_admin:
                    return JsonResponse({"error": "Permission refusée : seuls les administrateurs peuvent modifier un livre."}, status=403)
            except Utilisateur.DoesNotExist:
                return JsonResponse({"error": "Utilisateur demandeur non trouvé."}, status=404)

            # Rechercher le livre à mettre à jour
            try:
                livre = Livre.objects.get(id=id)
            except Livre.DoesNotExist:
                return JsonResponse({"error": "Livre non trouvé."}, status=404)

            # Mettre à jour les champs du livre
            livre.titre = data.get("titre", livre.titre)
            livre.auteur = data.get("auteur", livre.auteur)
            livre.isbn = data.get("isbn", livre.isbn)
            livre.genre = data.get("genre", livre.genre)
            livre.emplacement = data.get("emplacement", livre.emplacement)
            livre.disponible = data.get("disponible", livre.disponible)
            livre.save()

            return JsonResponse({
                "message": "Livre mis à jour avec succès.",
                "id": livre.id,
                "titre": livre.titre,
                "auteur": livre.auteur,
                "isbn": livre.isbn,
                "genre": livre.genre,
                "emplacement": livre.emplacement,
                "disponible": livre.disponible
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Requête invalide, données JSON attendues."}, status=400)

@csrf_exempt
def delete_livre(request, id):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)

            # Vérifier si l'utilisateur demandeur est un administrateur
            requester_id = data.get("requester_id")  # ID de l'utilisateur demandeur
            try:
                requester = Utilisateur.objects.get(id=requester_id)
                if not requester.is_admin:
                    return JsonResponse({"error": "Permission refusée : seuls les administrateurs peuvent supprimer un livre."}, status=403)
            except Utilisateur.DoesNotExist:
                return JsonResponse({"error": "Utilisateur demandeur non trouvé."}, status=404)

            # Rechercher le livre à supprimer
            try:
                livre = Livre.objects.get(id=id)
                livre.delete()
                return JsonResponse({"message": "Livre supprimé avec succès."}, status=200)
            except Livre.DoesNotExist:
                return JsonResponse({"error": "Livre non trouvé."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Requête invalide, données JSON attendues."}, status=400)

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
#@csrf_exempt
#def add_utilisateur(request):
#    if request.method == "POST":
#        data = json.loads(request.body)
#        utilisateur = Utilisateur.objects.create(
#            username=data.get('username'),
#            password=data.get('password'),
#           email=data.get('email'),
#            date_creation=data.get('date_creation')
#        )
#        return JsonResponse({
#            "id": utilisateur.id,
#            "username": utilisateur.username,
#            "email": utilisateur.email,
#            "date_creation": utilisateur.date_creation
#        }, status=201)
@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Récupérer les champs nécessaires
            username = data.get("username")
            password = data.get("password")
            email = data.get("email")

            # Vérifier si les champs sont présents
            if not username or not password or not email:
                return JsonResponse({"error": "Tous les champs sont obligatoires."}, status=400)

            # Vérifier si l'utilisateur ou l'email existent déjà
            if Utilisateur.objects.filter(username=username).exists():
                return JsonResponse({"error": "Ce nom d'utilisateur est déjà pris."}, status=400)

            if Utilisateur.objects.filter(email=email).exists():
                return JsonResponse({"error": "Cet email est déjà utilisé."}, status=400)

            # Créer un utilisateur normal (non administrateur)
            utilisateur = Utilisateur.objects.create(
                username=username,
                password=password,
                email=email,
                is_admin=False  # Par défaut, les utilisateurs ne sont pas administrateurs
            )

            return JsonResponse({
                "message": "Inscription réussie",
                "id": utilisateur.id,
                "username": utilisateur.username,
                "email": utilisateur.email
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Requête invalide, données JSON attendues."}, status=400)

@csrf_exempt # Pour permettre les requêtes POST sans vérification CSRF
def sign_in(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Récupérer les données d'authentification
            username = data.get("username")
            password = data.get("password")
            # Vérifier si l'utilisateur existe
            try:
                utilisateur = Utilisateur.objects.get(username=username)
                # Vérifier le mot de passe
                if check_password(password, utilisateur.password):
                # Vérification du rôle administrateur
                    if utilisateur.is_admin:
                        return JsonResponse({
                            "message": "Connexion réussie (Admin).",
                            "redirect_to": "/admin-dashboard", # Indiquer la redirection
                            "utilisateur": {
                                "id": utilisateur.id,
                                "username": utilisateur.username,
                                "email": utilisateur.email,
                                "is_admin": utilisateur.is_admin
                            }
                        }, status=200)
                    else:
                        return JsonResponse({
                            "message": "Connexion réussie (Utilisateur).",
                            "redirect_to": "/book-list", # Indiquerla redirection
                            "utilisateur": {
                                "id": utilisateur.id,
                                "username": utilisateur.username,
                                "email": utilisateur.email,
                                "is_admin": utilisateur.is_admin
                            }
                        }, status=200)
                else:
                    return JsonResponse({"error": "Mot de passe incorrect."}, status=400)
            except Utilisateur.DoesNotExist:
                return JsonResponse({"error": "Utilisateur non trouvé."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides."}, status=400)
    else:
        return JsonResponse({"error": "Méthode non autorisée."},status=405)
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
@csrf_exempt
def promote_to_admin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Vérifier si l'utilisateur demandeur est un superutilisateur
            requester_id = data.get("requester_id")  # ID de l'utilisateur demandeur
            try:
                requester = Utilisateur.objects.get(id=requester_id)
                if not requester.is_admin:  # Vérifie si l'utilisateur est administrateur
                    return JsonResponse({"error": "Permission refusée."}, status=403)
            except Utilisateur.DoesNotExist:
                return JsonResponse({"error": "Demandeur non trouvé."}, status=404)

            # Promouvoir l'utilisateur cible
            user_id = data.get("user_id")  # ID de l'utilisateur à promouvoir
            try:
                user = Utilisateur.objects.get(id=user_id)
                user.is_admin = True
                user.save()

                return JsonResponse({"message": f"L'utilisateur {user.username} a été promu administrateur avec succès."}, status=200)
            except Utilisateur.DoesNotExist:
                return JsonResponse({"error": "Utilisateur non trouvé."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Requête invalide, données JSON attendues."}, status=400)



