from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Produit, UserPaiement
import stripe
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import  User
from .forms import UserRegisterFrom, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, 
    DetailView,
    DeleteView, 
    CreateView,
    UpdateView,
    DeleteView
)

stripe.api_key = settings.STRIPE_SECRET_KEY # new









def home(request): # pour afficher les produits a vendre sur l_index
    context = {
        'produits': Produit.objects.all()
    }
    return render(request, 'users/index.html', context)


def public(request): # autre page test
    return render(request, 'users/publication.html')





class Search(ListView): # Rechercher un Produit depuis index (home)
    model = Produit
    template_name = 'users/search.html'
    context_object_name = 'produits'
    ordering = ['-date_post']
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('q')
        liste = Produit.objects.filter(
            Q(titre__icontains = query) | Q (description__icontains = query)
        )
        return liste
        
class ProduitListView(ListView): # list des produits
    model = Produit
    template_name = 'users/index.html'
    context_object_name = 'produits'
    ordering = ['-date_post']
    paginate_by = 8

class UserProduitListView(ListView): # list des produits d'un utilisateur preci
    model = Produit
    template_name = 'users/user_produits.html'
    context_object_name = 'produits'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Produit.objects.filter(auteur=user).order_by('-date_post')


class ProduitDetailtView(DetailView): # Detail sur un produit specifique
    model = Produit
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request): # new
    if request.method == 'POST':
        pr = request.POST.get("montant")
        dr = request.POST.get("descriptionn")
        form = UserPaiement(request.POST)
        form.save()
        charge = stripe.Charge.create(
            amount  = pr,
            currency='xof',
            description = dr,
            source=request.POST['stripeToken']
        )
        messages.success(request, f'Paiement effectué avec succes consulter votre boite mail pour les instructions')
            
        return render(request, 'users/charge.html')

class ProduitCreateView( LoginRequiredMixin, CreateView): # creer nouveau produit
    model = Produit
    fields =  [ 'titre','description','quantite','image1','image2','image3', 'prix']

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        return super().form_valid(form)
        
   

class ProduitUpdateView( LoginRequiredMixin,UserPassesTestMixin, UpdateView): # modifier produit
    model = Produit
    fields =  [ 'titre','description','quantite','image1','image2','image3', 'prix']

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        produit = self.get_object()
        if self.request.user == produit.auteur :
            return True
        return False

class ProduitDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # supprimer un produit specifique
    model = Produit
    success_url = '/'

    def test_func(self):
        produit = self.get_object()
        if self.request.user == produit.auteur :
            return True
        return False

    

def actu(request): # autre page test
    return render(request, 'users/actualite.html')



def register(request): # Pour linscription des utilisateurs
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Félicitation  {username} , vous pouvez vous Connecter. Pensez à mettre votre profile à jour  : )')
            return redirect('login') 

    else:
        form = UserRegisterFrom()
    return render(request, 'users/register.html',{'form': form})

@login_required
def profile(request):
     if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            u_form.save()
            messages.success(request, f'Votre Profile a été mis à jour avec succes !')
            return redirect('profile') 
     else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
         
     context = {
        'u_form': u_form,
        'p_form' : p_form
     }
    
     return render(request, 'users/profile.html', context)


