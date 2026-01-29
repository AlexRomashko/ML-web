from django.shortcuts import render, redirect
from django.views import View
from diplom.models import Data
import os
from django.http import HttpResponse, Http404
from django.conf import settings
import csv
from io import StringIO
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile
import numpy as np
import pandas as pd


def imit_exp(data):
    K = data[0]
    samples = data[1]

    z = np.random.sample(samples)

    tau = []
    data = data[2::]
    N = 0

    for el in data:
        normal_samples = np.random.normal(el[0] * 1e-9, el[1] * 1e-9, el[2])
        tau = np.append(tau, normal_samples)
        N = N + el[2]

    f = []
    for k in range(0, len(tau)):
        f.append(-1 * tau[k] * np.log(z))

    dfbins = pd.DataFrame(columns=range(0, K))

    buf = np.linspace(0, 10e-9, num=K + 1)
    for k in range(0, len(f)):
        bins, buf = np.histogram(f[k], bins=buf)
        dfbins.loc[len(dfbins.index)] = pd.Series(bins)

    i = dfbins.to_numpy()

    e = np.zeros(K)
    e[17:27:1] = 0.02

    I = np.zeros((N, K))
    for l in range(0, N):
        for k in range(0, K):
            for j in range(0, k + 1):
                I[l, k] += e[j] * i[l, k - j]

    data = pd.DataFrame(I)
    return data, N


def process_data(request):
    if request.method == 'POST':
        dynamic_data = [int(request.POST.get('integer0')), int(request.POST.get('integer1'))]
        row_count = int(request.POST.get('rowCount'))

        # Соберите динамические поля
        for i in range(row_count):
            float1 = float(request.POST.get(f'float{i + 1}_1'))
            float2 = float(request.POST.get(f'float{i + 1}_2'))
            integer2 = int(request.POST.get(f'integer{i + 1}_3'))
            dynamic_data.append([float1, float2, integer2])

        result_data, N = imit_exp(dynamic_data)
        # Генерация CSV-файла
        csv_file_path = f"uploads/{request.user.username}_{N}_{dynamic_data[0]}_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.csv"
        csv_file_name = f"{request.user.username}_{N}_{dynamic_data[0]}_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.csv"

        result_data.to_csv(csv_file_path, index=False)

        # Сохранение данных в модель Data
        data_instance = Data(
            name=f"{request.user.username}_{N}_{dynamic_data[0]}_{pd.Timestamp.now().strftime('%Y%m%d')}",
            N=N,
            K=dynamic_data[0],
            owner=request.user,
            linkToFile=csv_file_path
        )
        data_instance.save()
        print('LOL')
        # Вернуть имя файла для отображения в интерфейсе
        return render(request, 'modeling/one_exp.html', {'csv_file_name': csv_file_name})

    return render(request, 'modeling/one_exp.html')


def download_csv(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    raise Http404


