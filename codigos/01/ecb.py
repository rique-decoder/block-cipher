"""
Enunciado Prático/Conceitual: Cifre uma mensagem utilizando uma cifra de bloco.

Pergunta 1: Por que o modo ECB - Electronic Codebook (cifrar cada bloco isoladamente) é problemático 
quando blocos de texto claro se repetem? Como o modo CBC resolve isso encadeando os blocos?

Pergunta 2: Explique qual é a função do Vetor de Inicialização (IV) 
e por que ele deve ser imprevisível (mas não necessariamente secreto).

Pergunta 3: Se o terceiro bloco do texto cifrado sofrer uma alteração 
acidental durante a transmissão em rede, quais blocos do texto claro 
resultante serão afetados na hora da descriptografia? Justifique.
"""
import operator

TAMANHO_BLOCO = 4  

class ElectronicCodebook():
    def __init__(self, mensagem_binaria: str, chave: int):

        self.mensagem = mensagem_binaria
        # ex: "1111 0110 1001 01010"

        self.chave = chave
        # ex: "1111"

    def gerar_blocos(self):

        resto = len(self.mensagem) % TAMANHO_BLOCO
        msg = self.mensagem

        if resto != 0:
            msg += "0" * (TAMANHO_BLOCO - resto)
        # padding: completa com zeros à direita até virar múltiplo do tamanho de bloco  

        blocos = []

        for i in range(0, len(msg), TAMANHO_BLOCO):

            fatia = msg[i:i + TAMANHO_BLOCO]

            blocos.append(int(fatia, 2))

        return blocos

    def criptografar(self):

        blocos = self.gerar_blocos()
        mensagem_criptografada = []

        for bloco in blocos:
            bloco_cifrado = operator.xor(bloco, self.chave)
            mensagem_criptografada.append(bloco_cifrado)

        return mensagem_criptografada

    def descriptografar(self, blocos_cifrados):

        blocos_decifrados = []

        for bloco in blocos_cifrados:
            bloco_original = operator.xor(bloco, self.chave)
            blocos_decifrados.append(bloco_original)

        return blocos_decifrados


def mostrar(titulo, blocos):
    formatado = " | ".join(f"{b:0{TAMANHO_BLOCO}b}" for b in blocos)
    print(f"{titulo:<12}: {formatado}")


texto_plano = "11110110100101010" 

chave = 0b1010 

ecb = ElectronicCodebook(texto_plano, chave)

blocos = ecb.gerar_blocos()
mostrar("Texto claro", blocos)

cifrado = ecb.criptografar()
mostrar("Cifrado", cifrado)

decifrado = ecb.descriptografar(cifrado)
mostrar("Decifrado", decifrado)