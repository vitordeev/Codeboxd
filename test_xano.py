"""Script temporário só pra testar a conexão com o Xano.
Depois de confirmar que funciona, pode apagar este arquivo.
"""

import asyncio

from Codeboxd_main.services.xano_client import xano_get


async def main():
    print("Testando conexão com o Xano...")
    titulos = await xano_get("/titulos")
    print("Conectou! Resposta da API:")
    print(titulos)


if __name__ == "__main__":
    asyncio.run(main())