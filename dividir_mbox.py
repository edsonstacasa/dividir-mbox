import email.utils
import sys
from collections import defaultdict
from email import policy
from email.parser import BytesParser
from pathlib import Path


def iterar_mensagens_mbox(caminho_entrada):
    buffer = None
    encontrou_primeira_mensagem = False

    with open(caminho_entrada, "rb") as arquivo:
        for linha in arquivo:
            if linha.startswith(b"From "):
                if encontrou_primeira_mensagem and buffer:
                    yield bytes(buffer)

                encontrou_primeira_mensagem = True
                buffer = bytearray()
                buffer.extend(linha)
                continue

            if encontrou_primeira_mensagem:
                buffer.extend(linha)

    if encontrou_primeira_mensagem and buffer:
        yield bytes(buffer)


def obter_mensagem(raw_msg):
    linhas = raw_msg.splitlines(keepends=True)
    if linhas and linhas[0].startswith(b"From "):
        raw_email = b"".join(linhas[1:])
    else:
        raw_email = raw_msg

    return BytesParser(policy=policy.compat32).parsebytes(raw_email)


def obter_periodo(msg, modo_divisao):
    try:
        data = msg.get("Date")
        if not data:
            return "sem_data"

        dt = email.utils.parsedate_to_datetime(data)
        if modo_divisao == "ano_mes":
            return f"{dt.year:04d}-{dt.month:02d}"

        return f"{dt.year:04d}"
    except Exception:
        return "erro_data"


def solicitar_arquivo_mbox():
    entrada = input("Informe o caminho do arquivo mbox a dividir: ").strip().strip('"')
    if not entrada:
        print("Nenhum arquivo informado.")
        sys.exit(1)

    caminho = Path(entrada).expanduser()
    if not caminho.is_file():
        print(f"Arquivo nao encontrado: {caminho}")
        sys.exit(1)

    return caminho


def solicitar_modo_divisao():
    while True:
        print("\nComo deseja dividir?")
        print("1 - Por ano")
        print("2 - Por ano-mes")

        opcao = input("Escolha 1 ou 2: ").strip()
        if opcao == "1":
            return "ano"
        if opcao == "2":
            return "ano_mes"

        print("Opcao invalida.")


def obter_caminho_saida(caminho_entrada, periodo):
    sufixo = caminho_entrada.suffix
    nome_base = caminho_entrada.stem if sufixo else caminho_entrada.name
    return caminho_entrada.with_name(f"{nome_base}_{periodo}{sufixo}")


def main():
    caminho_entrada = solicitar_arquivo_mbox()
    modo_divisao = solicitar_modo_divisao()
    arquivos = {}
    contadores = defaultdict(int)

    print(f"Abrindo mbox: {caminho_entrada}")

    try:
        for i, raw_msg in enumerate(iterar_mensagens_mbox(caminho_entrada), start=1):
            msg = obter_mensagem(raw_msg)
            periodo = obter_periodo(msg, modo_divisao)

            if periodo not in arquivos:
                caminho_saida = obter_caminho_saida(caminho_entrada, periodo)
                arquivos[periodo] = open(caminho_saida, "ab")

            arquivos[periodo].write(raw_msg)
            if not raw_msg.endswith(b"\n"):
                arquivos[periodo].write(b"\n")

            contadores[periodo] += 1

            if i % 100 == 0:
                print(f"{i} mensagens processadas...")

        print("\nResumo:")
        for periodo in sorted(contadores):
            print(f"{periodo}: {contadores[periodo]} mensagens")
    finally:
        for arq in arquivos.values():
            arq.flush()
            arq.close()

    print("\nConcluido.")


if __name__ == "__main__":
    main()
