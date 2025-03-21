import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix, issparse

movies = pd.read_csv('preprocessed_data.csv')

movies['tag'] = movies['tag'].fillna('')

genres = movies['genres'].str.get_dummies(sep='|')

features = csr_matrix(genres.values)

def calcular_inercia(dados, k):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(dados)
    return kmeans.inertia_

def gerar_dados_referencia(dados):
    if issparse(dados):
        min_vals = np.array(dados.min(axis=0).todense()).flatten()
        max_vals = np.array(dados.max(axis=0).todense()).flatten()
        shape = dados.shape
        referencia = np.random.uniform(low=min_vals, high=max_vals, size=shape)
        referencia = csr_matrix(referencia)
    else:
        min_vals = np.min(dados, axis=0)
        max_vals = np.max(dados, axis=0)
        referencia = np.random.uniform(low=min_vals, high=max_vals, size=dados.shape)
    return referencia

def calcular_gap_statistic(dados, k_max, n_refs=10):
    gaps = []
    inercias_reais = []
    inercias_referencia = []

    for k in range(1, k_max + 1):
        inercia_real = calcular_inercia(dados, k)
        inercias_reais.append(inercia_real)

        inercias_ref_k = []
        for _ in range(n_refs):
            referencia = gerar_dados_referencia(dados)
            inercia_ref = calcular_inercia(referencia, k)
            inercias_ref_k.append(inercia_ref)
        inercia_ref_media = np.mean(inercias_ref_k)
        inercias_referencia.append(inercia_ref_media)

        gap = np.log(inercia_ref_media) - np.log(inercia_real)
        gaps.append(gap)

    return gaps, inercias_reais, inercias_referencia

k_max = 10 
gaps, inercias_reais, inercias_referencia = calcular_gap_statistic(features, k_max)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(range(1, k_max + 1), gaps, 'bo-', markersize=8)
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Gap Statistic')
plt.title('Gap Statistic')

plt.subplot(1, 2, 2)
plt.plot(range(1, k_max + 1), np.log(inercias_reais), 'bo-', markersize=8, label='Dados Reais')
plt.plot(range(1, k_max + 1), np.log(inercias_referencia), 'ro-', markersize=8, label='Dados de Referência')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Log(Inércia)')
plt.title('Inércia dos Dados Reais vs Referência')
plt.legend()

plt.tight_layout()
plt.savefig('gap_statistic_manual.png') 
plt.close()