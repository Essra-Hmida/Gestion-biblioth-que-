from django.urls import path, include
from . import views

urlpatterns = [
    # Livre URLs
    path('api/livres', views.get_livres, name='get_livres'),
    path('api/livres/<int:id>', views.get_livre, name='get_livre'),
    path('api/livres/add', views.add_livre, name='add_livre'),
    path('api/livres/<int:id>', views.update_livre, name='update_livre'),
    path('api/livres/<int:id>/delete', views.delete_livre, name='delete_livre'),
    
    # Utilisateur URLs
    path('api/utilisateurs', views.get_utilisateurs, name='get_utilisateurs'),
    path('api/utilisateurs/<int:id>', views.get_utilisateur, name='get_utilisateur'),
    path('api/utilisateurs/add', views.add_utilisateur, name='add_utilisateur'),
    path('api/utilisateurs/<int:id>', views.update_utilisateur, name='update_utilisateur'),
    path('api/utilisateurs/<int:id>/delete', views.delete_utilisateur, name='delete_utilisateur'),
    
    # Emprunt URLs
    path('api/emprunts', views.get_emprunts, name='get_emprunts'),
    path('api/emprunts/<int:id>', views.get_emprunt, name='get_emprunt'),
    path('api/emprunts/add', views.add_emprunt, name='add_emprunt'),
    path('api/emprunts/<int:id>', views.update_emprunt, name='update_emprunt'),
    path('api/emprunts/<int:id>/delete', views.delete_emprunt, name='delete_emprunt'),
]