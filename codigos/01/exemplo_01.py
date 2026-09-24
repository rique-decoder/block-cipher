"""
Demonstração independente: por que o modo ECB revela padrões
Mostra que blocos de texto claro repetidos geram blocos cifrados
IDÊNTICOS, mesmo sem o atacante conhecer a chave.
"""

TAMANHO_BLOCO = 4  # caracteres por bloco (32 bits, já que cada char = 8 bits em ASCII)
CHAVE = 0xA1B2C3D4  # chave de 32 bits, fixa para toda a mensagem (características do ECB)


def dividir_em_blocos(texto, tamanho):
    """Quebra a string em pedaços de tamanho fixo, completando o último com espaços se necessário."""
    sobra = len(texto) % tamanho
    if sobra != 0:
        texto += " " * (tamanho - sobra)
    return [texto[i:i + tamanho] for i in range(0, len(texto), tamanho)]


def bloco_para_inteiro(bloco_texto):
    """Converte um bloco de caracteres para um único inteiro (concatenando os bytes ASCII)."""
    valor = 0
    for caractere in bloco_texto:
        valor = (valor << 8) | ord(caractere)
    return valor


def cifrar_ecb(valor_inteiro, chave):
    return valor_inteiro ^ chave


mensagem = "vire a direita, depois  vire a esquerda"

blocos_texto = dividir_em_blocos(mensagem, TAMANHO_BLOCO)

print(f'Mensagem: "{mensagem}"')
print(f"Dividida em {len(blocos_texto)} blocos de {TAMANHO_BLOCO} caracteres cada\n")

linhas = []
cifrados_ja_vistos = {}

for posicao, bloco in enumerate(blocos_texto):
    numero = bloco_para_inteiro(bloco)
    cifrado = cifrar_ecb(numero, CHAVE)
    linhas.append((posicao, bloco, cifrado))

print(f"{'#':<3} {'Bloco claro':<15} {'Bloco cifrado':<15} Observação")
print("-" * 55)
for posicao, bloco, cifrado in linhas:
    observacao = ""
    if cifrado in cifrados_ja_vistos:
        observacao = f"repetiu o bloco #{cifrados_ja_vistos[cifrado]}"
    else:
        cifrados_ja_vistos[cifrado] = posicao
    print(f"{posicao:<3} {repr(bloco):<15} {hex(cifrado):<15} {observacao}")