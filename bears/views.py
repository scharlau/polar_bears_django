from django.shortcuts import render, get_object_or_404
from .models import Bear

def bear_list(request):
    bears = Bear.objects.all()
    return render(request, 'bears/bear_list.html', {'bears' : bears})

def bear_detail(request, id):
    bear = get_object_or_404(Bear, id=id)
    return render(request, 'bears/bear_detail.html', {'bear' : bear})