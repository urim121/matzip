from django.shortcuts import render, redirect as r
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import restaurant

def main(request):
    Res=restaurant.objects.all()
    print(Res)
    if request.method == 'POST':
        category = request.POST.get('category')
        User.object.get(category=category)

    return render(
        request,
        'mapmain.html',
        {'restaurant':Res}
    )

