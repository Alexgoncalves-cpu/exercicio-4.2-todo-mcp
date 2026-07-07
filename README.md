# Exercício 4.2 — MCP server local que consome a API do 4.1

MCP server (stdio) que expõe duas *tools* para uma aplicação de TODO list,
implementadas chamando a API REST construída no Exercício 4.1
(`http://localhost:8000`).

```
  Agente / LLM   ──MCP──▶   servidor_mcp.py   ──HTTP──▶   API 4.1 (localhost:8000)
```

## Arquivos

- `servidor_mcp.py` — MCP server com as tools `criar_tarefa` e `listar_tarefas`.
- `cliente_teste.py` — sobe o server via stdio, chama as tools e imprime no
  stdout um envelope JSON único com o resultado.
- `requirements.txt` — dependências (`mcp`, `httpx`).

## Como rodar

1. **Terminal A** — suba a API do 4.1 (reinicie para o store ficar limpo):
   ```bash
   uvicorn app.main:app --port 8000     # no repo do 4.1
   ```
2. **Terminal B** — neste repo:
   ```bash
   pip install -r requirements.txt
   python cliente_teste.py
   ```
   O comando deve imprimir um envelope JSON com `tools`, `criar_resultado`
   e `listar_resultado`.

## Como validar

Com a API do 4.1 no ar, neste repo:

```bash
autograde validar 4.2
```

## Reflexão

No 4.1 o cliente precisava falar HTTP diretamente: montar a URL, escolher o
verbo certo, serializar o corpo da requisição e tratar o status code. No 4.2,
o agente só precisa saber que existe uma tool `criar_tarefa(titulo)` e chamá-la
— o MCP tornou irrelevante para quem chama **como** o dado é buscado (protocolo
HTTP, URL da API, formato do request/response). O MCP escondeu o transporte:
o agente fala MCP, e é a tool que sabe traduzir isso para HTTP contra a API.
