# **Projeto de Clustering de Filmes**

Este projeto tem como objetivo agrupar filmes em clusters (grupos) com base em suas características, como gêneros, tags, ano de lançamento e avaliações. O modelo utiliza técnicas de processamento de texto (TF-IDF) e redução de dimensionalidade (TruncatedSVD) para criar features a partir das tags dos filmes, combinadas com outras informações, e aplica o algoritmo K-Means para realizar o clustering.

## Dataset

- [fonte do dataset usado](https://grouplens.org/datasets/movielens/)

---

## **O que o modelo faz?**
O modelo realiza as seguintes etapas:

1. **Pré-processamento dos dados**:
   - Extrai o ano de lançamento do título do filme.
   - Limpa o título, removendo o ano.
   - Processa as tags dos filmes, agrupando-as por `movieId`.
   - Combina os dados de filmes, avaliações e tags em um único dataframe.

2. **Criação de features**:
   - Converte os gêneros dos filmes em variáveis dummy (one-hot encoding).
   - Aplica TF-IDF nas tags para criar features de texto.
   - Reduz a dimensionalidade das features de tags usando TruncatedSVD.
   - Combina as features de gêneros, tags reduzidas, ano de lançamento e avaliações em uma única matriz de features.

3. **Clustering**:
   - Aplica o algoritmo K-Means para agrupar os filmes em clusters.
   - Atribui um rótulo de cluster a cada filme.

4. **Saída**:
   - Gera um arquivo CSV (`movies_with_clusters.csv`) com os filmes e seus respectivos clusters.

---

## **Como funciona?**
O modelo utiliza as seguintes técnicas:

- **TF-IDF (Term Frequency-Inverse Document Frequency)**:
  - Transforma as tags dos filmes em vetores numéricos, ponderando a importância de cada palavra no contexto do conjunto de tags.

- **TruncatedSVD**:
  - Reduz a dimensionalidade das features de tags, mantendo as informações mais importantes.

- **K-Means**:
  - Agrupa os filmes em clusters com base nas features combinadas (gêneros, tags, ano e avaliações).

---

## **Estrutura do Projeto**
O projeto é dividido em dois scripts principais:

1. **`merge_csv.py`**:
   - Realiza o pré-processamento dos dados.
   - Salva os dados pré-processados em `preprocessed_data.csv`.

2. **`modelo.py`**:
   - Carrega os dados pré-processados.
   - Cria as features e aplica o modelo de clustering.
   - Salva os resultados em `movies_with_clusters.csv`.

---

## **Como executar o projeto?**

### Pré-requisitos
- Python 3.x
- Bibliotecas necessárias: `pandas`, `scikit-learn`, `scipy`, `numpy`

Instale as dependências com:
```bash
pip install pandas scikit-learn scipy numpy
```

### Passos para execução

1. **Pré-processamento**:
   - Execute o script `merge_csv.py` para processar os dados brutos e gerar o arquivo `preprocessed_data.csv`:
     ```bash
     python merge_csv.py
     ```

2. **Clustering**:
   - Execute o script `modelo.py` para aplicar o modelo de clustering e gerar o arquivo `movies_with_clusters.csv`:
     ```bash
     python modelo.py
     ```

---

## **Arquivos gerados**

1. **`preprocessed_data.csv`**:
   - Contém os dados pré-processados, incluindo:
     - `movieId`: ID do filme.
     - `title`: Título do filme.
     - `genres`: Gêneros do filme.
     - `year`: Ano de lançamento.
     - `rating`: Média das avaliações.
     - `tag`: Tags agrupadas por filme.

2. **`movies_with_clusters.csv`**:
   - Contém os dados finais com os rótulos dos clusters:
     - Todas as colunas de `preprocessed_data.csv`.
     - `cluster`: Rótulo do cluster ao qual o filme pertence.

---

## **Interpretação dos resultados**

- **Clusters**:
  - Cada cluster representa um grupo de filmes com características semelhantes.
  - Por exemplo:
    - Cluster 0: Filmes de animação infantil.
    - Cluster 1: Filmes de ação e aventura.
    - Cluster 2: Filmes de comédia romântica.

- **Análise**:
  - Você pode analisar os filmes em cada cluster para entender as características comuns.
  - Use ferramentas de visualização (como `matplotlib` ou `seaborn`) para explorar os clusters.

---

## **Exemplo de uso**

Após executar o projeto, você pode usar o arquivo `movies_with_clusters.csv` para:
- Recomendar filmes com base no cluster.
- Analisar tendências de gêneros, tags e avaliações.
- Visualizar a distribuição dos filmes nos clusters.

---

## **Próximos passos**
- **Otimização**:
  - Ajustar o número de clusters (`n_clusters`) para melhorar a qualidade do agrupamento.
  - Experimentar outros algoritmos de clustering, como DBSCAN ou Hierarchical Clustering.

- **Visualização**:
  - Criar gráficos para visualizar a distribuição dos filmes nos clusters.
  - Usar técnicas como PCA ou t-SNE para reduzir a dimensionalidade e visualizar os clusters em 2D ou 3D.

- **Integração**:
  - Integrar o modelo em um sistema de recomendação de filmes.

---

