from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Data
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


@login_required(login_url='/authentication/login')
def index(request):
    return redirect('main')


@login_required(login_url='/authentication/login')
def mainView(request):
    datas = Data.objects.filter(owner=request.user)
    paginator = Paginator(datas, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'data': datas,
        'page_obj': page_obj
    }
    return render(request, 'diplom/data.html', context)



@login_required(login_url='/authentication/login')
def download_file(request, pk):
    data = get_object_or_404(Data, pk=pk)
    file_path = data.linkToFile.path
    file_name = data.linkToFile.name.split('/')[-1]

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
