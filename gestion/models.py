from django.db import models

class Livre(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    genre = models.CharField(max_length=100)
    emplacement = models.CharField(max_length=255)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

class Utilisateur(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Emprunt(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_emprunt = models.DateField()
    date_retour = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.utilisateur.username} emprunte {self.livre.titre}"
