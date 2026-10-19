# Backup local de uploads — P.3 — 13/10/2026

Escopo autorizado: preservar uploads durante a execução local com `.venv`, sem
Docker. Esta entrega acrescenta `tools/backup_uploads.py`, um utilitário que cria
um ZIP novo, inclui manifesto SHA-256 e confere CRC e conteúdo após a gravação.
O utilitário não apaga fontes nem sobrescreve backups existentes, recusa destino
dentro da origem e não cria uma cópia vazia que pareça válida.

## Execução verificada

```powershell
.venv\Scripts\python.exe tools/backup_uploads.py --destination .local/backups/uploads-before-admin-2026-10-13.zip
```

- Dois arquivos originais, 86.516 bytes, preservados.
- CRC e SHA-256 conferidos após a criação do ZIP.
- SHA-256 do ZIP: `c310d4da3a2c639d120a2b923313cc2312ce0c69d2acb71dc96e989ff2e1096d`.
- `.local/` é ignorada pelo Git; o conteúdo do backup não entra no commit.
- Quatro testes em `tests/test_backup_uploads.py` aprovados: leitura dos arquivos
  restauráveis, proteção de backup anterior, rejeição de destino na origem e
  rejeição de origem vazia. A suíte completa de 120 testes passou e o Reflex
  compilou na rodada atual.

Para criar novas cópias com nome único:

```powershell
.venv\Scripts\python.exe tools/backup_uploads.py
```

O script usa `uploaded_files/` por padrão. Se o diretório efetivo estiver
personalizado, passar `--source` explicitamente. As cópias padrão ficam em
`.local/backups/`. Esse backup no mesmo disco não substitui uma cópia externa
para falha/perda do disco; hospedagem e migração de armazenamento ficam pendentes.

Commit desta rodada limitado ao utilitário, seus testes e esta evidência. As
alterações administrativas e os testes de imagem em andamento ficam para uma
entrega posterior com suas próprias evidências.
