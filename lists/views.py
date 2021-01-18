from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
import random
# Create your views here.
def home_page(request):
    tips_list=["Don't hurry!", 'Keep calm', 'Smile!', 'Love and peace!', 'Think twice', 'Run away']
    return render(request, 'home.html', {'name':tips_list[random.choice(range(len(tips_list)))]})
def view_list(request, list_id,):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})
def new_list(request):
    list_=List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/'%(list_.id,))
def add_item(request, list_id):
    list_=List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/'%(list_.id,))
