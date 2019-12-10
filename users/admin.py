from django.contrib import admin
from .models import Produit, Profile, Ville


class ProduitAdmin(admin.ModelAdmin):
    list_display= ('titre','description','quantite','date_post','auteur','prix')

class ProfileUserAdmin(admin.ModelAdmin):
    list_display= ('user','telephone','localite','can_post')



admin.site.register(Produit,ProduitAdmin)
admin.site.register(Profile, ProfileUserAdmin)
admin.site.register(Ville)

