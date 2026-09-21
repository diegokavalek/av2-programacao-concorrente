"""Gera arquivos de IDs alternativos. Uso: python gerar_listas.py"""

from pathlib import Path


PASTA = Path(__file__).resolve().parent / "listas"
TAMANHOS = {"pequena": 50, "media": 200, "grande": 500}

PASTA.mkdir(exist_ok=True)
for nome, quantidade in TAMANHOS.items():
    ids = "\n".join(str(10000 + indice) for indice in range(quantidade))
    (PASTA / f"lista_ids_{nome}.txt").write_text(ids + "\n", encoding="utf-8")

print("Listas geradas com sucesso.")
