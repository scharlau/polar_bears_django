from django.shortcuts import render, get_object_or_404
from .models import Bear, Sighting

def bear_list(request):
    bears = Bear.objects.all()
    return render(request, 'bears/bear_list.html', {'bears' : bears})

def bear_detail(request, id):
    bear = get_object_or_404(Bear, id=id)
    sightings = Sighting.objects.filter(bear_id=id)
    return render(request, 'bears/bear_detail.html', {'bear' : bear, 'sightings' : sightings})