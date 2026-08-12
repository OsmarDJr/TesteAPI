import json
import re
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def normalizar_cep(cep):
    return re.sub(r"\D", "", cep)


if len(sys.argv) < 2:
    print("Erro: informe um CEP.")
    sys.exit(1)


cep = normalizar_cep(sys.argv[1])

if len(cep) != 8:
    print("Erro: o CEP deve possuir 8 dígitos.")
    sys.exit(1)


url = f"https://viacep.com.br/ws/{cep}/json/"

print("--------------------------------")
print("CONSULTA DE CEP")
print("--------------------------------")
print(f"Consultando CEP: {cep}")
print(f"URL: {url}")
print()


try:
    requisicao = Request(
        url,
        headers={"User-Agent": "GitHub-Actions-Consulta-CEP"}
    )

    with urlopen(requisicao, timeout=15) as resposta:
        dados = json.load(resposta)

except HTTPError as erro:
    print(f"Erro HTTP: {erro.code}")
    sys.exit(1)

except URLError as erro:
    print(f"Erro de conexão: {erro.reason}")
    sys.exit(1)


if dados.get("erro"):
    print("CEP não encontrado.")
    sys.exit(1)


print("RESULTADO")
print("--------------------------------")
print(f"CEP:        {dados.get('cep', '')}")
print(f"Logradouro: {dados.get('logradouro', '')}")
print(f"Bairro:     {dados.get('bairro', '')}")
print(f"Cidade:     {dados.get('localidade', '')}")
print(f"Estado:     {dados.get('estado', '')}")
print(f"UF:         {dados.get('uf', '')}")
print(f"DDD:        {dados.get('ddd', '')}")
print("--------------------------------")


with open("resultado.json", "w", encoding="utf-8") as arquivo:
    json.dump(
        dados,
        arquivo,
        ensure_ascii=False,
        indent=4
    )


print()
print("Arquivo resultado.json criado com sucesso.")
