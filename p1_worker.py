"""P1: processa uma lista de IDs usando varias threads."""

import argparse
import json
import random
import sys
import threading
import time
from datetime import datetime
from pathlib import Path


def consultar_api_mockada(identificador: int) -> dict:
    """Simula a latencia de uma API e devolve JSON no formato exigido."""
    time.sleep(0.005)
    gerador = random.Random(identificador)
    return {
        "id": identificador,
        "status": "ok",
        "valor": round(gerador.uniform(10.0, 1000.0), 2),
    }


def ler_ids(caminho: Path) -> list[int]:
    ids = []
    for numero_linha, texto in enumerate(
        caminho.read_text(encoding="utf-8").splitlines(), start=1
    ):
        texto = texto.strip()
        if not texto:
            continue
        try:
            ids.append(int(texto))
        except ValueError as erro:
            raise ValueError(
                f"ID invalido na linha {numero_linha}: {texto!r}"
            ) from erro
    return ids


def executar(arquivo_ids: Path, arquivo_log: Path, quantidade_threads: int) -> float:
    inicio = time.perf_counter()
    ids = ler_ids(arquivo_ids)
    arquivo_log.parent.mkdir(parents=True, exist_ok=True)

    proximo_indice = 0
    mutex_distribuicao = threading.Lock()
    mutex_log = threading.Lock()

    with arquivo_log.open("w", encoding="utf-8", newline="\n") as log:

        def trabalhar() -> None:
            nonlocal proximo_indice

            while True:
                # Somente uma thread por vez escolhe o proximo item.
                with mutex_distribuicao:
                    if proximo_indice >= len(ids):
                        return
                    identificador = ids[proximo_indice]
                    proximo_indice += 1

                resposta = consultar_api_mockada(identificador)
                data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                json_resposta = json.dumps(
                    resposta, ensure_ascii=False, separators=(",", ":")
                )
                linha = (
                    f"{data}, {threading.current_thread().name}, "
                    f"{identificador}, {json_resposta}\n"
                )

                # Evita que duas threads misturem escritas no arquivo.
                with mutex_log:
                    log.write(linha)
                    log.flush()

        threads = [
            threading.Thread(target=trabalhar, name=f"Thread-{numero}")
            for numero in range(1, quantidade_threads + 1)
        ]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    return time.perf_counter() - inicio


def main() -> int:
    parser = argparse.ArgumentParser(description="P1 - trabalhador concorrente")
    parser.add_argument("arquivo_ids", type=Path)
    parser.add_argument("arquivo_log", type=Path)
    parser.add_argument("threads", type=int)
    argumentos = parser.parse_args()

    if argumentos.threads < 1:
        print("ERRO: a quantidade de threads deve ser maior que zero.", file=sys.stderr)
        return 2

    try:
        tempo = executar(
            argumentos.arquivo_ids,
            argumentos.arquivo_log,
            argumentos.threads,
        )
        print(f"P1 concluido em {tempo:.6f} segundos.")
        return 0
    except Exception as erro:
        print(f"ERRO em P1: {erro}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
