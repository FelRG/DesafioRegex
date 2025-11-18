import re
import random
import string
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Regex-Dataset.txt
dados_produtos = [
    # Totalmente válidos
    {
        "nome": "Camiseta Polo Masculina",
        "codigo": "ABCDEF1234",
        "preco": "99.99",
        "validade": "15/12/2025"
    },
    {
        "nome": "Tênis Esportivo Masculino",
        "codigo": "ZXCVBN5678",
        "preco": "149,90",
        "validade": "01/01/2026"
    },
    {
        "nome": "Bermuda Jeans Masculina",
        "codigo": "QWERTY0001",
        "preco": "79.9",
        "validade": "31/10/2025"
    },
    {
        "nome": "Vestido Longo Estampado",
        "codigo": "LONGDR1234",
        "preco": "120.00",
        "validade": "28/02/2024"  # válido (ano bissexto)
    },

    # Inválidos
    {
        "nome": "camiseta polo masculina",  # minúsculas
        "codigo": "abcdef1234",             # minúsculas
        "preco": "99.999",                  # 3 casas decimais
        "validade": "15/12/25"              # ano com 2 dígitos
    },
    {
        "nome": "Camisa Masculina",         # menos de 3 palavras
        "codigo": "ABC1234@",               # caractere especial
        "preco": "-49,90",                  # valor negativo
        "validade": "32/12/2025"            # dia inválido
    },
    {
        "nome": "Calça Jeans Slim",
        "codigo": "ABCDE1234",              # só 5 letras
        "preco": "100,999",                 # 3 casas decimais
        "validade": "30-12-2025"            # separadores errados
    },
    {
        "nome": "Blusa De Frio",
        "codigo": "1234567890",             # só números
        "preco": "0.00",
        "validade": "00/00/0000"            # tudo inválido
    },
    {
        "nome": "Jaqueta Masculina Couro",
        "codigo": "C0D1C01234",             # contém números entre letras
        "preco": "abc",                     # não é número
        "validade": "31/04/2025"            # abril não tem 31 dias (invalidez lógica)
    },
    {
        "nome": "Boné Vermelho Casual",
        "codigo": "VERMEL0000",
        "preco": "199",                     # inteiro, mas válido
        "validade": "29/02/2023"            # 2023 não é bissexto
    },
    {
        "nome": "Mochila Escolar Grande",
        "codigo": "MOCHIL123",              # só 3 dígitos
        "preco": "250.5",                   # 1 casa decimal (válido)
        "validade": "12/13/2025"            # mês inválido
    },
    {
        "nome": "Tênis Corrida Branco",
        "codigo": "RUNSHO1234",
        "preco": "300,00",
        "validade": "15/06/2030"
    }
]

# Regexes para cada campo para validação
regexNomeProduto = re.compile(r"^[A-Z][a-z]+(?:\s[a-z]+){2,}$")
regexCodigo = re.compile(r"^[A-Z]{6}\d{4}$")
regexPreco = re.compile(r"^\d+([.,]\d{1,2})?$")
regexDataValidade = re.compile(r"^(?:(?:31\/(0[13578]|1[02]))|(?:30\/(0[13-9]|1[0-2]))|(?:0[1-9]|1\d|2\d)\/(0[1-9]|1[0-2]))\/\d{4}$")

# Fnções para geração de letras e números
def gerar_letras(qtd):
    return ''.join(random.choices(string.ascii_uppercase, k=qtd))

def gerar_numeros(qtd):
    return ''.join(random.choices(string.digits, k=qtd))

# Funções validadoras
def validar_nome(nome):

    regexApenasLetras = re.compile(r'[^a-zA-Z\s]$')

    if not isinstance(nome, str) or not nome.strip():
        return "Item item item"

    if regexNomeProduto.match(nome):
        return nome

    nome = regexApenasLetras.sub('', nome)
    nome = nome.lower()
    nome_array = re.split(r"\s+", nome.strip())

    if len(nome_array) == 1:
        nome_array *= 3
    elif len(nome_array) == 2:
        nome_array.append(nome_array[1])

    nome_array[0] = nome_array[0].capitalize()

    return ' '.join(nome_array)

def validar_codigo(codigo):
    if not isinstance(codigo, str):
        return "AAAAAA1111"

    regexApenasLetraseNumeros = re.compile(r'[^a-zA-Z0-9]$')

    codigo = regexApenasLetraseNumeros.sub('', codigo).upper()

    if regexCodigo.match(codigo):
        return codigo

    partes = re.split(r'(?<=\D)(?=\d)|(?<=\d)(?=\D)', codigo)
    letras = ''.join(filter(str.isalpha, partes))
    numeros = ''.join(filter(str.isdigit, partes))

    # Caso só números
    if letras == '' and numeros:
        if len(numeros) >= 4:
            numeros = numeros[:4]
        else:
            numeros += numeros[-1] * (4 - len(numeros))
        letras = gerar_letras(6)
        return letras + numeros

    # Caso só letras
    if numeros == '' and letras:
        if len(letras) >= 6:
            letras = letras[:6]
        else:
            letras += letras[-1] * (6 - len(letras))
        numeros = gerar_numeros(4)
        return letras + numeros

    # Caso letras e números misturados
    if letras and numeros:
        if len(letras) < 6:
            letras += letras[-1] * (6 - len(letras))
        else:
            letras = letras[:6]

        if len(numeros) < 4:
            numeros += numeros[-1] * (4 - len(numeros))
        else:
            numeros = numeros[:4]

        return letras + numeros

    return "AAAAAA1111"

def validar_preco(preco):
    regexApenasNumeros = re.compile(r'[^\d,.]')

    if regexPreco.match(preco):
        return preco

    preco = re.sub(regexApenasNumeros, "", preco)
    preco_array = re.split(r"[.,]", preco.strip())

    inteiro = "0"
    decimal = ""

    if len(preco_array) == 1:
        # Ex: "123abc" → apenas parte inteira
        inteiro = ''.join(re.findall(r'\d+', preco_array[0])) or "0"
    elif len(preco_array) >= 2:
        inteiro = ''.join(re.findall(r'\d+', preco_array[0])) or "0"
        decimal = ''.join(re.findall(r'\d+', preco_array[1]))[:2]  # até 2 casas

    if decimal:
        return f"{str(inteiro)}.{decimal}"
    else:
        return f"{str(inteiro)}"

def validar_data(data):

    # Corrige separadores errados: troca '-' ou '.' por '/'
    data = re.sub(r"[-.]", "/", data.strip())

    # Verifica se a data está no formato dd/mm/aaaa
    padrao_data = re.compile(r"^(\d{2})/(\d{2})/(\d{4})$")
    match = padrao_data.match(data)

    if match:
        dia, mes, ano = map(int, match.groups())
        try:
            # Corrige datas impossíveis automaticamente
            if mes < 1:
                mes = 1
            elif mes > 12:
                mes = 12

            # Verifica o último dia do mês com base no calendário
            ultimo_dia_mes = (datetime(ano, mes, 1) + relativedelta(months=1) - timedelta(days=1)).day
            if dia < 1:
                dia = 1
            elif dia > ultimo_dia_mes:
                dia = ultimo_dia_mes

            data_valida = datetime(ano, mes, dia)
            return data_valida.strftime("%d/%m/%Y")
        except Exception:
            pass

    # Se não for possível validar, retorna a data atual + 3 meses
    nova_data = datetime.now() + relativedelta(months=3)
    return nova_data.strftime("%d/%m/%Y")

# Separação dos produtos
produtos_validos = []
produtos_invalidos = []
produtos_formatados = []

def validar_tudo(nome, codigo, preco, validade):
    validanome = re.search(regexNomeProduto, nome)
    validacodigo = re.search(regexCodigo, codigo)
    validapreco = re.search(regexPreco, preco)
    validavalidade = re.search(regexDataValidade, validade)

    if validanome and validacodigo and validapreco and validavalidade:
        return True
    else:
        return False

for produto in dados_produtos:
    valicao = validar_tudo(produto["nome"], produto["codigo"], produto["preco"], produto["validade"])
    if valicao:
        produtos_validos.append(produto)
    else:
        produtos_invalidos.append(produto)

# Resultados
print(f"Produtos válidos: {len(produtos_validos)}")
print(f"Produtos inválidos: {len(produtos_invalidos)}")

print("\n--- Produtos Válidos ---")
for p in produtos_validos:
    print(p)

print("\n--- Produtos Invalidos ---")
for p in produtos_invalidos:
    print(p)

for produto in dados_produtos:
    produto["nome"] = validar_nome(produto["nome"])
    produto["codigo"] = validar_codigo(produto["codigo"])
    produto["preco"] = validar_preco(produto["preco"])
    produto["validade"] = validar_data(produto["validade"])
    produtos_formatados.append(produto)

print(f"Produtos formatados: {len(produtos_formatados)}")

print("\n--- Produtos Formatados ---")
for p in produtos_formatados:
    print(p)
