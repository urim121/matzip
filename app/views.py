from django.shortcuts import render, redirect as r
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from .models import restaurant, User, Article
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

def signup(request):
  if request.method == 'POST':
    # 회원정보 저장
    email = request.POST.get('email')
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    user = User(email=email, name=name, pwd=pwd)
    user.save()
    return HttpResponseRedirect('/main/')

  return render(request, 'signup.html')

def signin(request):
  if request.method == 'POST':
    # 회원정보 조회
    email = request.POST.get('email')
    pwd = request.POST.get('pwd')
    
    try:
      # select * from user where email=? and pwd=?
      user = User.objects.get(email=email, pwd=pwd)
      request.session['email'] = email
      return render(request, 'signin_success.html')
    except:
      return render(request, 'signin_fail.html')

  return render(request, 'signin.html')

def signout(request):
  del request.session['email']  # 개별 삭제
  request.session.flush()  # 전체 삭제

  return HttpResponseRedirect('/main/')

def write(request):
  if request.method == 'POST':
    title = request.POST.get('title')
    content = request.POST.get('content')
    
    try:
      email = request.session['email']
      # select * from user where email = ?
      user = User.objects.get(email=email)
      # insert into article (title, content, user_id) values (?, ?, ?)
      article = Article(title=title, content=content, user=user)
      article.save()
      return render(request, 'write_success.html')
    except:
      return render(request, 'write_fail.html')

  return render(request, 'write.html')

def list(request):
  # select * from article order by id desc
  article_list = Article.objects.order_by('-id')
  context = { 
    'article_list' : article_list 
  }
  return render(request, 'list.html', context)

def detail(request, id):
  # select * from article where id = ?
  article = Article.objects.get(id=id)
  context = { 
    'article' : article 
  }
  return render(request, 'detail.html', context)

def update(request, id):
  # select * from article where id = ?
  article = Article.objects.get(id=id)

  if request.method == 'POST':
    title = request.POST.get('title')
    content = request.POST.get('content')
    
    try:
      # update article set title = ?, content = ? where id = ?
      article.title = title
      article.content = content
      article.save()
      return render(request, 'update_success.html')
    except:
      return render(request, 'update_fail.html')

  context = { 
    'article' : article 
  }
  return render(request, 'update.html', context)

def delete(request, id):
  try:
    # select * from article where id = ?
    article = Article.objects.get(id=id)
    article.delete()
    return render(request, 'delete_success.html')
  except:
    return render(request, 'delete_fail.html')