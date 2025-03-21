### **Gap Statistic**

#### O que é?

O **Gap Statistic** compara a inércia dos seus dados reais com a inércia de dados de referência (gerados aleatoriamente). Ele ajuda a determinar o número ideal de clusters (`k`) identificando onde a inércia dos dados reais se desvia significativamente da inércia dos dados de referência.

#### Como interpretar?

- **Gráfico do Gap Statistic**:
    - **Eixo X**: Número de clusters (`k`).
    - **Eixo Y**: Valor do Gap Statistic.
    - **O que procurar**: O valor de `k` que maximiza o Gap Statistic.

- **Gráfico das inércias**:
    - **Eixo X**: Número de clusters (`k`).
    - **Eixo Y**: Logaritmo da inércia.
    - **O que procurar**: A diferença entre a inércia dos dados reais e a inércia dos dados de referência.