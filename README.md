# AV2_TPE - Programacao Concorrente

Implementacao em Python do sistema P0/P1 solicitado na atividade de Sistemas
Operacionais. O programa funciona no Windows, Linux e macOS e nao utiliza
bibliotecas externas.

## O que cada arquivo faz

- `p0_orquestrador.py`: processo pai. Gera as listas, inicia P1 seis vezes,
  espera cada termino, cronometra, audita o codigo de saida e a quantidade de
  linhas do log e mostra a tabela final.
- `p1_worker.py`: processo filho. Le IDs, cria as threads, simula a API e grava
  o log usando dois mutexes (`threading.Lock`).
- `gerar_listas.py`: gerador opcional das listas pequena, media e grande.
- `lista_ids.txt`: lista de exemplo exigida no enunciado.
- `listas/`: listas usadas nos testes.
- `logs/`: seis logs produzidos pela execucao.
- `resultados.csv`: tempos medidos na ultima execucao.
- `Relatorio_AV2_TPE.pdf`: relatorio curto com tabela e analise.

## Como executar no Windows

1. Instale o Python 3, caso ainda nao esteja instalado. Durante a instalacao,
   marque **Add Python to PATH**.
2. Extraia este projeto.
3. Abra a pasta extraida, clique na barra de endereco do Explorador, digite
   `cmd` e pressione Enter.
4. Execute:

```text
python p0_orquestrador.py
```

Se `python` nao for reconhecido, tente:

```text
py p0_orquestrador.py
```

Ao final aparecera a tabela com as seis execucoes. Os logs e o arquivo
`resultados.csv` serao recriados automaticamente.

## Como colocar no GitHub

1. Crie um repositorio vazio no GitHub.
2. Envie todos os arquivos e pastas deste projeto.
3. Copie o link do repositorio e entregue-o junto com o PDF.

Nao e necessario editar os codigos para executar o experimento.
