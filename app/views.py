from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import restaurant, User, Article, restaurant
from django.forms.models import model_to_dict
from django.views.decorators.clickjacking import xframe_options_exempt

def main(request):
    return render(
        request,
        'map.html',
        {}
    )

def insert(request):
    restaurant.objects.create(category='한식',name='조치원집',location='세종특별자치시 조치원읍 정리 24-1 ',number='044 -865 -3021',long=127.300569,lat=36.6002684)
    c = restaurant(category='한식',name='한방족발 곰나루',location='세종특별자치시 조치원읍 정리 29-2 ',number='044 -865 -0948',long=127.299651,lat=36.6000454)
    c.save()
    restaurant(category='한식',name='내집닭갈비',location='세종특별자치시 금남면 용포리 193-26',number='044 -865 -3021',long=127.281676,lat=36.4657734).save()
    restaurant(category='일식',name='어순이와돈돌이',location='세종특별자치시 조치원읍 원리 15-4',number='044 -865 -6661',long=127.297339,lat=36.5945092).save()
    restaurant(category='한식',name='삼거리식당',location='세종특별자치시 조치원읍 죽림리 32-8',number='044 -865 -3101',long=127.300569,lat=36.6002684).save()
    restaurant(category='중식',name='형제반점',location='세종특별자치시 조치원읍 정리 99-3 ',number='044 -866 -6607',long=127.298225,lat=36.5983098).save()
    restaurant(category='한식',name='삼흥식당',location='세종특별자치시 조치원읍 원리 141-6 (1층)',number='044 -867 -5311',long=127.29677,lat=36.6006563).save()
    return HttpResponse('데이터 입력 완료')

def show(request):
    res=restaurant.objects.all()
    return render(request, 'app/map.html', {'data':res})


@xframe_options_exempt
def kor(request):
    res=restaurant.objects.filter(category='한식')
    return render(request, 'category_kor.html', {'data':res})

@xframe_options_exempt
def chi(request):
    res=restaurant.objects.filter(category='중식')
    return render(request, 'category_chi.html', {'data':res})

@xframe_options_exempt
def jap(request):
    res=restaurant.objects.filter(category='일식')
    return render(request, 'category_jap.html', {'data':res})

@xframe_options_exempt
def wes(request):
    res=restaurant.objects.filter(category='양식')
    return render(request, 'category_wes.html', {'data':res})

@xframe_options_exempt
def bun(request):
    res=restaurant.objects.filter(category='분식')
    return render(request, 'category_bun.html', {'data':res})

@xframe_options_exempt
def caf(request):
    res=restaurant.objects.filter(category='카페')
    return render(request, 'category_caf.html', {'data':res})


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

    category  = request.POST.get('category')
    title = request.POST.get('title')
    content = request.POST.get('content')
    
    try:
      email = request.session['email']
      # select * from user where email = ?
      user = User.objects.get(email=email)
      # insert into article (title, content, user_id) values (?, ?, ?)
      article = Article(category=category , title=title, content=content, user=user)
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
    category  = request.POST.get('category')
    
    try:
      # update article set title = ?, content = ? where id = ?
      article.category = category 
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
  
def article_list(request):
    category = request.GET.get('category', 'all')  # 기본값은 'all'
    
    if category == 'all':
        article_list = Article.objects.all()
    elif category == '1':
        article_list = Article.objects.filter(category='1')
    elif category == '2':
        article_list = Article.objects.filter(category='2')
    else:
        article_list = Article.objects.all()  # 잘못된 쿼리 파라미터일 경우 기본값으로 모든 게시물 보여줌
        
    context = {'article_list': article_list, 'category': category}
    return render(request, 'article_list.html', context)
