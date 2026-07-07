import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _extrair_json(resultado, como_lista: bool = False):
    """Extrai o payload JSON de um CallToolResult, seja qual for o formato
    de `content` usado pela versão instalada do SDK.

    Quando a tool devolve uma lista, o FastMCP serializa **um TextContent por
    item** em vez de um único bloco com o array inteiro; por isso, se
    `como_lista=True`, juntamos o JSON de todos os blocos numa lista.
    """
    if getattr(resultado, "structuredContent", None) is not None:
        return resultado.structuredContent

    blocos = [json.loads(b.text) for b in resultado.content if getattr(b, "text", None) is not None]

    if como_lista:
        return blocos

    if not blocos:
        raise ValueError(f"não foi possível extrair JSON de: {resultado!r}")

    return blocos[0]


async def main() -> dict:
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]

            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})

            return {
                "tools": nomes,
                "criar_resultado": _extrair_json(criar),
                "listar_resultado": _extrair_json(listar, como_lista=True),
            }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(main())))
