from django.shortcuts import render
from .models import LabMembers

# Create your views here.
def index(request):
    object_list = LabMembers.objects.all()
    context = {'object_list': object_list}
    return render(request, 'index.html', context)
