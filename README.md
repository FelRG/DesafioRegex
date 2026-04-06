# Desafio Regex - Validação e Correção de Produtos com Regex em Python

## Descrição

Este projeto realiza a validação e correção automática de dados de produtos utilizando expressões regulares em Python.

São analisados os seguintes campos:

- Nome do produto
- Código do produto
- Preço
- Data de validade

O programa separa os produtos em válidos e inválidos e também gera uma versão formatada dos dados incorretos. :contentReference[oaicite:0]{index=0}

---

## Bibliotecas Utilizadas

```python
import re
import random
import string
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
```

---

## Estrutura dos Dados

Cada produto possui os seguintes campos:

```python
{
    "nome": "Camiseta Polo Masculina",
    "codigo": "ABCDEF1234",
    "preco": "99.99",
    "validade": "15/12/2025"
}
```

---

## Regras de Validação

### Nome do Produto

O nome deve:

- Começar com letra maiúscula
- Possuir pelo menos 3 palavras
- Conter apenas letras e espaços

Exemplo válido:

```python
"Camiseta Polo Masculina"
```

---

### Código do Produto

O código deve possuir:

- 6 letras maiúsculas
- 4 números ao final

Exemplo válido:

```python
"ABCDEF1234"
```

---

### Preço

O preço pode:

- Ser inteiro
- Ter até 2 casas decimais
- Utilizar ponto ou vírgula

Exemplos válidos:

```python
"99.99"
"149,90"
"199"
```

---

### Data de Validade

A data deve estar no formato:

```python
dd/mm/aaaa
```

Também são tratados casos como:

- Separadores incorretos (`-` ou `.`)
- Dias inválidos
- Meses inválidos
- Ajuste automático para o último dia válido do mês

---

## Funções Utilizadas

### Geração de Dados

- `gerar_letras()`
- `gerar_numeros()`

### Validação e Correção

- `validar_nome()`
- `validar_codigo()`
- `validar_preco()`
- `validar_data()`
- `validar_tudo()`

---

## O que o Código Faz

1. Define uma lista de produtos válidos e inválidos
2. Aplica regex para validar os dados
3. Separa os produtos em válidos e inválidos
4. Corrige automaticamente os dados incorretos
5. Exibe:
   - Quantidade de produtos válidos
   - Quantidade de produtos inválidos
   - Lista de produtos corrigidos

---

## Exemplos de Correções

```python
"abcdef1234" -> "ABCDEF1234"
"30-12-2025" -> "30/12/2025"
"-49,90" -> "49.90"
"Camisa Masculina" -> "Camisa masculina masculina"
```

---

## Como Executar

1. Instale a dependência necessária:

```bash
pip install python-dateutil
```

2. Execute o arquivo Python:

```bash
python nome_do_arquivo.py
```
