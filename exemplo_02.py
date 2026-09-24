"""
Demonstração independente: como o CBC resolve o vazamento de padrão do ECB
Mesma frase, mesma chave, mesmos blocos "vire" repetidos --
mas agora encadeados com o bloco cifrado anterior (e um IV no primeiro bloco).
"""

TAMANHO_BLOCO = 4  # caracteres por bloco (32 bits)
CHAVE = 0xA1B2C3D4      # mesma chave do exemplo ECB, para comparação direta
IV = 0x5F3759DF          # vetor de inicialização, mesmo tamanho de um bloco (32 bits)


def dividir_em_blocos(texto, tamanho):
    sobra = len(texto) % tamanho
    if sobra != 0:
        texto += " " * (tamanho - sobra)
    return [texto[i:i + tamanho] for i in range(0, len(texto), tamanho)]


def bloco_para_inteiro(bloco_texto):
    valor = 0
    for caractere in bloco_texto:
        valor = (valor << 8) | ord(caractere)
    return valor


mensagem = "vire a direita, depois  vire a esquerda"
blocos_texto = dividir_em_blocos(mensagem, TAMANHO_BLOCO)

print(f'Mensagem: "{mensagem}"')
print(f"IV usado: {hex(IV)}\n")

linhas = []
bloco_anterior_cifrado = IV  # no primeiro bloco, o "anterior" é o IV

for posicao, bloco in enumerate(blocos_texto):
    numero = bloco_para_inteiro(bloco)

    # Ci = (Pi XOR C(i-1)) XOR K   -- é aqui que está o encadeamento
    entrada = numero ^ bloco_anterior_cifrado
    cifrado = entrada ^ CHAVE

    linhas.append((posicao, bloco, cifrado))
    bloco_anterior_cifrado = cifrado  # esse resultado alimenta o próximo bloco

print(f"{'#':<3} {'Bloco claro':<15} {'Bloco cifrado':<15} Observação")
print("-" * 55)
cifrados_ja_vistos = {}
for posicao, bloco, cifrado in linhas:
    observacao = ""
    if cifrado in cifrados_ja_vistos:
        observacao = f"repetiu o bloco #{cifrados_ja_vistos[cifrado]}"
    else:
        cifrados_ja_vistos[cifrado] = posicao
    print(f"{posicao:<3} {repr(bloco):<15} {hex(cifrado):<15} {observacao}")

print("\nConclusão: os blocos #0 e #6 têm o MESMO texto claro ('vire'),")
print("mas agora geram cifrados DIFERENTES -- porque cada um foi combinado")
print("com um 'bloco anterior' diferente antes de entrar na chave.")
print("O padrão que existia no ECB desapareceu no cifrado.")