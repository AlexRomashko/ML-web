from django.shortcuts import render, redirect
from diplom.models import Data
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import pandas as pd
import os
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
from sklearn.decomposition import NMF


def pca(request):
    new_file_name = None
    if request.method == 'POST':
        options = request.POST.get('options')
        inputValue = request.POST.get('inputValue')
        dropdown = request.POST.get('dropdown')
        fileName = request.POST.get('fileName')

        print(options)
        print(dropdown)
        print(inputValue)

        # Find file by name
        data_instance = Data.objects.filter(name=fileName).first()
        if data_instance:
            file_path = data_instance.linkToFile.path
            data_df = pd.read_csv(file_path)

            data = 0

            if str(options) == 'pca':
                model = PCA(n_components=int(inputValue), svd_solver=str(dropdown))
                data = pd.DataFrame(model.fit_transform(data_df))

            elif str(options) == 'ica':
                model = FastICA(n_components=int(inputValue), whiten_solver=str(dropdown))
                data = pd.DataFrame(model.fit_transform(data_df))

            elif str(options) == 'nmf':
                model = NMF(n_components=int(inputValue), solver=str(dropdown))
                data = pd.DataFrame(model.fit_transform(data_df))

            N = data.shape[0]
            K = data.shape[1]
            csv_file_path = f"uploads/{str(options)}_{request.user.username}_{N}_{K}_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.csv"
            new_file_name = csv_file_path.split('/')[-1]

            data.to_csv(csv_file_path, index=False)

            data_instance = Data(
                name=new_file_name,
                N=N,
                K=K,
                owner=request.user,
                linkToFile=csv_file_path
            )
            data_instance.save()

    datas = Data.objects.filter(owner=request.user)
    paginator = Paginator(datas, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'data': datas,
        'page_obj': page_obj,
        'csv_file_name': new_file_name
    }
    return render(request, 'MineData/pca.html', context)
