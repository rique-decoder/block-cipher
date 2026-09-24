import operator

TAMANHO_BLOCO = 4

class CipherBlockChaining():
    def __init__(self, mensagem_binaria: str, chave: int, iv: int):
        self.mensagem = mensagem_binaria
        self.chave = chave
        self.iv = iv
        # ex: iv = 0b0101

    def gerar_blocos(self):
        resto = len(self.mensagem) % TAMANHO_BLOCO
        msg = self.mensagem
        if resto != 0:
            msg += "0" * (TAMANHO_BLOCO - resto)

        blocos = []
        for i in range(0, len(msg), TAMANHO_BLOCO):
            fatia = msg[i:i + TAMANHO_BLOCO]
            blocos.append(int(fatia, 2))
        return blocos

    def criptografar(self):
        blocos = self.gerar_blocos()
        mensagem_criptografada = []

        bloco_anterior = self.iv  # no primeiro bloco, "anterior" é o IV

        for bloco in blocos:
            # Ci = (Pi XOR C(i-1)) XOR K
            entrada = operator.xor(bloco, bloco_anterior)
            bloco_cifrado = operator.xor(entrada, self.chave)

            mensagem_criptografada.append(bloco_cifrado)
            bloco_anterior = bloco_cifrado  # atualiza para a próxima rodada

        return mensagem_criptografada

    def descriptografar(self, blocos_cifrados):
        blocos_decifrados = []

        for i, bloco_cifrado in enumerate(blocos_cifrados):
            # bloco anterior: IV se for o primeiro, senão o cifrado da posição anterior
            bloco_anterior = self.iv if i == 0 else blocos_cifrados[i - 1]

            # Pi = (Ci XOR K) XOR C(i-1)
            parcial = operator.xor(bloco_cifrado, self.chave)
            bloco_original = operator.xor(parcial, bloco_anterior)

            blocos_decifrados.append(bloco_original)

        return blocos_decifrados


def mostrar(titulo, blocos):
    formatado = " | ".join(f"{b:0{TAMANHO_BLOCO}b}" for b in blocos)
    print(f"{titulo:<12}: {formatado}")


texto_plano = "11110110100101010"
chave = 0b1010
iv = 0b0101  # vetor de inicialização, mesmo tamanho de um bloco

cbc = CipherBlockChaining(texto_plano, chave, iv)

blocos = cbc.gerar_blocos()
mostrar("Texto claro", blocos)

cifrado = cbc.criptografar()
mostrar("Cifrado", cifrado)

decifrado = cbc.descriptografar(cifrado)
mostrar("Decifrado", decifrado)