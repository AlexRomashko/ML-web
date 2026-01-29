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
        tau = np.append(tau, np.random.normal(el[0] * 1e-9, el[1] * 1e-9), el[2])
        N = N + el[2]

    f = []
    for k in range(0, len(tau)):
        f.append(-1 * tau[k] * np.log(z))

    dfbins = pd.DataFrame(columns=range(0, K))

    buf = np.linspace(0, 10e-9, num=K + 1)
    for k in range(0, len(f)):
        bins, buf = np.histogram(f[k], bins=buf)
        dfbins.loc[len(dfbins.index)] = pd.Series(bins)

    print(dfbins)

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
