from django.shortcuts import render, redirect as r
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import restaurant
from django.forms.models import model_to_dict

def main(request):
    return render(
        request,
        'mapmain.html',
        {}
    )

def category_data(request):
    category = request.GET.get('category')
    res=restaurant.objects.filter(category=category)
    result = []
    for r in res:
        r2 = model_to_dict(r)
        result.append(r2)

    return JsonResponse(result, safe=False)
