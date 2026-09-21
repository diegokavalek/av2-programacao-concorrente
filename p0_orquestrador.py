"""P0: cria P1, espera seu termino, audita logs e compara os tempos."""

import csv
import subprocess
import sys
import time
from pathlib import Path


BASE = Path(__file__).resolve().parent
PASTA_LISTAS = BASE / "listas"
PASTA_LOGS = BASE / "logs"
ARQUIVO_RESULTADOS = BASE / "resultados.csv"
QUANTIDADE_THREADS = 4
TAMANHOS = {"pequena": 50, "media": 200, "grande": 500}


def gerar_listas() -> None:
    PASTA_LISTAS.mkdir(exist_ok=True)
    for nome, quantidade in TAMANHOS.items():
        caminho = PASTA_LISTAS / f"lista_ids_{nome}.txt"
        conteudo = "\n".join(str(10000 + indice) for indice in range(quantidade))
        caminho.write_text(conteudo + "\n", encoding="utf-8")

    # Exemplo com o nome exato solicitado no enunciado.
    (BASE / "lista_ids.txt").write_text(
        (PASTA_LISTAS / "lista_ids_pequena.txt").read_text(encoding="utf-8"),
        encoding="utf-8",
    )


def contar_linhas(caminho: Path) -> int:
    if not caminho.exists():
        return 0
    with caminho.open("r", encoding="utf-8") as arquivo:
        return sum(1 for linha in arquivo if linha.strip())


def executar_p1(tamanho: str, quantidade_threads: int) -> dict:
    entrada = PASTA_LISTAS / f"lista_ids_{tamanho}.txt"
    log = PASTA_LOGS / f"log_{tamanho}_{quantidade_threads}_threads.txt"
    comando = [
        sys.executable,
        str(BASE / "p1_worker.py"),
        str(entrada),
        str(log),
        str(quantidade_threads),
    ]

    inicio = time.perf_counter()
    processo = subprocess.Popen(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = processo.communicate()  # Aguarda P1, equivalente ao wait.
    tempo_total = time.perf_counter() - inicio

    esperado = contar_linhas(entrada)
    gravado = contar_linhas(log)
    codigo = processo.returncode

    if codigo < 0:
        termino = f"sinal {-codigo}"
    elif codigo == 0:
        termino = "normal"
    else:
        termino = f"erro ({codigo})"

    if codigo == 0 and gravado == esperado:
        status = "sucesso"
    elif gravado != esperado:
        status = "enriquecimento incompleto"
    else:
        status = "falha"

    if stdout.strip():
        print(f"P1: {stdout.strip()}")
    if stderr.strip():
        print(f"P1 stderr: {stderr.strip()}")

    return {
        "tamanho": tamanho,
        "ids": esperado,
        "threads": quantidade_threads,
        "tempo_segundos": tempo_total,
        "termino": termino,
        "linhas_log": gravado,
        "status": status,
    }


def imprimir_tabela(resultados: list[dict]) -> None:
    cabecalhos = ["Tamanho", "IDs", "Threads", "Tempo (s)", "Termino", "Log", "Status"]
    linhas = [
        [
            item["tamanho"],
            str(item["ids"]),
            str(item["threads"]),
            f'{item["tempo_segundos"]:.4f}',
            item["termino"],
            str(item["linhas_log"]),
            item["status"],
        ]
        for item in resultados
    ]
    larguras = [
        max(len(cabecalhos[i]), *(len(linha[i]) for linha in linhas))
        for i in range(len(cabecalhos))
    ]

    def formatar(linha: list[str]) -> str:
        return " | ".join(valor.ljust(larguras[i]) for i, valor in enumerate(linha))

    print("\nRELATORIO CONSOLIDADO")
    print(formatar(cabecalhos))
    print("-+-".join("-" * largura for largura in larguras))
    for linha in linhas:
        print(formatar(linha))


def salvar_csv(resultados: list[dict]) -> None:
    with ARQUIVO_RESULTADOS.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=resultados[0].keys())
        escritor.writeheader()
        escritor.writerows(resultados)


def main() -> int:
    gerar_listas()
    PASTA_LOGS.mkdir(exist_ok=True)
    resultados = []

    for tamanho in TAMANHOS:
        for quantidade_threads in (1, QUANTIDADE_THREADS):
            print(f"Executando lista {tamanho} com {quantidade_threads} thread(s)...")
            resultados.append(executar_p1(tamanho, quantidade_threads))

    imprimir_tabela(resultados)
    salvar_csv(resultados)
    return 0 if all(item["status"] == "sucesso" for item in resultados) else 1


if __name__ == "__main__":
    raise SystemExit(main())
