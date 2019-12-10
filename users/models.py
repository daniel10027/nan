from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
 
# class produits pour la vente de produit

class Ville(models.Model):
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom
    
class Produit(models.Model):
    titre = models.CharField(max_length=20) #Titre du produit
    image1 = models.ImageField(default='default.png',upload_to='profile_pics')
    image2 = models.ImageField(default='default.png',upload_to='profile_pics')
    image3 = models.ImageField(default='default.png',upload_to='profile_pics')
    description = models.TextField() # Description
    quantite = models.IntegerField() # Quantite de produit a vendre 
    date_post = models.DateTimeField(default=timezone.now) # date de publication
    auteur = models.ForeignKey(User, on_delete=models.CASCADE) # info sur lauteur
    prix = models.IntegerField() # Prix du produit 

    def __str__(self): # Fonction pour retourner une info sur le produit(le titre)
        return self.titre 
    def get_absolute_url(self):
        return reverse("produit-detail", kwargs={"pk": self.pk}) # rediriger apres creation de produuits
    

        

class Profile(models.Model): #Profile de l'utilisateur
    # Pour attribuer un statut depuis admin
     
    user = models.OneToOneField(User, on_delete = models.CASCADE) # Cascade (si je supprime un user je supprime toutes ses donneesi)
    telephone = models.CharField(max_length=100)
    localite = models.ForeignKey(Ville, on_delete=models.CASCADE,blank=True, null=True)
    image = models.ImageField(default='default.png',upload_to='profile_pics')
    can_post = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args, **kwargs):
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300 :
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

# Gestion du front end dynamic

class UserPaiement(models.Model):
    description = models.TextField() # Description
    date = models.DateTimeField(default=timezone.now) # date de publication
    auteur = models.ForeignKey(User, on_delete=models.CASCADE) # info sur lauteur
    prix = models.IntegerField() # Prix du produit 
    def __str__(self):
        return self.description

    def savee(self, *args, **kwargs):
        super().save(*args, **kwargs)