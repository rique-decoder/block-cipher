"""
Demonstração independente: propagação de erro no CBC (bit-flipping)
Versão 2: usa um S-box (substituição não-linear) para simular o
efeito avalanche de uma cifra de bloco real, além do encadeamento CBC.
"""

TAMANHO_BLOCO_BITS = 4
CHAVE = 0b1010
IV = 0b0101

# S-box de 4 bits (mesma ideia usada em DES/AES, só que reduzida a 4 bits
# pra caber nos blocos do nosso exemplo). Qualquer 1 bit diferente na
# entrada tende a mudar VÁRIOS bits na saída -- isso é o efeito avalanche.
SBOX = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
SBOX_INV = [0] * 16
for entrada, saida in enumerate(SBOX):
    SBOX_INV[saida] = entrada


def cifrar_bloco(x, chave):
    """Simula uma 'mini cifra de bloco': XOR com a chave, depois substituição não-linear."""
    return SBOX[x ^ chave]


def decifrar_bloco(y, chave):
    """Inverso exato de cifrar_bloco."""
    return SBOX_INV[y] ^ chave


def cifrar_cbc(blocos_claros, chave, iv):
    cifrados = []
    anterior = iv
    for bloco in blocos_claros:
        cifrado = cifrar_bloco(bloco ^ anterior, chave)
        cifrados.append(cifrado)
        anterior = cifrado
    return cifrados


def decifrar_cbc(blocos_cifrados, chave, iv):
    claros = []
    for i, cifrado in enumerate(blocos_cifrados):
        anterior = iv if i == 0 else blocos_cifrados[i - 1]
        claro = decifrar_bloco(cifrado, chave) ^ anterior
        claros.append(claro)
    return claros


def mostrar(titulo, blocos):
    formatado = " | ".join(f"{b:0{TAMANHO_BLOCO_BITS}b}" for b in blocos)
    print(f"{titulo:<22}: {formatado}")


blocos_claros = [0b1111, 0b0110, 0b1111, 0b0101, 0b1100, 0b0011]

print("=== Situação normal ===")
mostrar("Texto claro", blocos_claros)
cifrado_original = cifrar_cbc(blocos_claros, CHAVE, IV)
mostrar("Cifrado", cifrado_original)
decifrado_normal = decifrar_cbc(cifrado_original, CHAVE, IV)
mostrar("Decifrado (confere)", decifrado_normal)
assert decifrado_normal == blocos_claros, "cifrar/decifrar não bateu!"

print("\n=== Corrompendo 1 bit do bloco de ÍNDICE 2 (C3) ===")
cifrado_corrompido = cifrado_original.copy()
cifrado_corrompido[2] ^= 0b0001

print(f"C3 original  : {cifrado_original[2]:04b}")
print(f"C3 corrompido: {cifrado_corrompido[2]:04b}  (1 bit trocado)\n")

decifrado_corrompido = decifrar_cbc(cifrado_corrompido, CHAVE, IV)

print(f"{'Bloco':<6} {'Original':<10} {'Corrompido':<12} Efeito")
print("-" * 55)
for i in range(len(blocos_claros)):
    original = decifrado_normal[i]
    novo = decifrado_corrompido[i]
    bits_diferentes = bin(original ^ novo).count("1")

    if bits_diferentes == 0:
        efeito = "sem alteração"
    elif i == 2:
        efeito = f"{bits_diferentes} bits diferentes -> AVALANCHE (bloco irreconhecível)"
    else:
        efeito = f"{bits_diferentes} bit diferente -> mudança pontual e previsível"

    print(f"{i:<6} {original:04b}       {novo:04b}         {efeito}")

print("\n=== Resumo final (mesmo formato do início, com o ataque aplicado) ===")
mostrar("Texto claro               ", blocos_claros)
mostrar("Cifrado (c/ C3 alterado)  ", cifrado_corrompido)
mostrar("Decifrado (c/ C3 alterado)", decifrado_corrompido)