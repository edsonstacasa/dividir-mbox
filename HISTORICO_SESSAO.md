# Histórico de Sessão - Santa Casa de Batatais
# Última modificação: 05/06/2026

## Informações do Projeto
- **Cliente/Local:** Santa Casa de Misericórdia de Batatais
- **Objetivo:** Revisar e manter scripts Python no workspace local.

## Diretrizes de Trabalho
- Manter este histórico atualizado imediatamente após decisões, correções, criação de arquivos ou mudança de status.
- Comunicação objetiva, com foco em causa raiz e impacto técnico.
- Não usar valores hexadecimais diretamente em código gerado, salvo em `theme.json`.

## Estrutura de Arquivos
- `dividir_mbox.py` — script Python principal; solicita o arquivo mbox de entrada e gera saídas por ano ou por ano-mês.
- `dividir_mbox_gui.py` — versão com interface gráfica Tkinter para selecionar arquivo mbox e modo de divisão.
- `README.md` — documentação de uso em Windows/Linux, distribuição e geração de executável Windows.
- `.gitignore` — regras para ignorar cache Python, builds PyInstaller, ambientes virtuais e arquivos mbox locais.
- `HISTORICO_SESSAO.md` — histórico persistente da sessão.
- `__pycache__/` — artefato gerado por `py -m py_compile` durante validação de sintaxe.
- `build/` — artefato local gerado pelo PyInstaller, ignorado pelo Git.
- `dist/dividir_mbox_gui.exe` — executável Windows compilado da versão GUI.
- `dividir_mbox_gui.spec` — especificação local gerada pelo PyInstaller, ignorada pelo Git.

---

## Log de Atividades e Decisões

### 01/06/2026: Inicialização do Histórico de Sessão
- **Ações:** Criado `HISTORICO_SESSAO.md` na raiz do workspace conforme instrução obrigatória.
- **Decisões:** Objetivo inferido como revisão e manutenção de scripts Python locais, pois o workspace contém scripts de divisão de mbox.
- **Bugs corrigidos:** Nenhum.

### 01/06/2026: Revisão de `dividir_mbox.py`
- **Ações:** Revisado `dividir_mbox.py`; validada sintaxe com `py -m py_compile`; confirmado que `dividir mbox.py` não existe no workspace.
- **Decisões:** Nenhuma alteração aplicada ao script nesta etapa; revisão entregue como achados técnicos.
- **Bugs corrigidos:** Nenhum.

### 01/06/2026: Entrada Interativa do Arquivo Mbox
- **Ações:** Alterado `dividir_mbox.py` para solicitar o caminho do arquivo mbox; adicionada validação de arquivo existente; saídas passaram a usar o nome do arquivo informado com sufixo `_ANO`; validada sintaxe com `py -m py_compile`.
- **Decisões:** Removida dependência do nome fixo `Inbox`; encapsulado fluxo em `main()` e adicionada finalização garantida dos arquivos mbox em `finally`.
- **Bugs corrigidos:** Uso fixo de `Inbox` impedia reutilização com outros arquivos → caminho estava hardcoded → entrada passou a ser solicitada via `input()`.

### 01/06/2026: Opção de Divisão por Ano ou Ano-Mês
- **Ações:** Adicionada escolha interativa entre divisão por ano e por ano-mês; substituída a chave fixa de ano por período (`AAAA` ou `AAAA-MM`); validada sintaxe com `py -m py_compile`.
- **Decisões:** Mantidos grupos especiais `sem_data` e `erro_data` para mensagens sem cabeçalho `Date` ou com data inválida.
- **Bugs corrigidos:** Nenhum.

### 01/06/2026: Versão GUI para Divisão de Mbox
- **Ações:** Criado `dividir_mbox_gui.py` com interface Tkinter; adicionada seleção de arquivo via diálogo, escolha por ano ou ano-mês, processamento em thread e log de execução; validada sintaxe com `py -m py_compile`; confirmado `tkinter` disponível.
- **Decisões:** Mantida dependência apenas da biblioteca padrão; processamento executa em thread para evitar travamento da janela durante arquivos grandes.
- **Bugs corrigidos:** Nenhum.

### 01/06/2026: Documentação e Regras de Distribuição
- **Ações:** Criados `README.md` e `.gitignore`; documentado uso por GUI e terminal, comandos PyInstaller e observações de distribuição.
- **Decisões:** `.gitignore` passa a excluir `build/`, `dist/`, `*.spec`, caches Python, ambientes virtuais e arquivos mbox locais para evitar versionar dados sensíveis e artefatos gerados.
- **Bugs corrigidos:** Nenhum.

### 01/06/2026: Compatibilidade Linux no README
- **Ações:** Atualizado `README.md` para informar que a versão CLI também funciona em Linux; adicionados comandos separados para Windows (`py`) e Linux (`python3`).
- **Decisões:** Mantida geração de `.exe` documentada como fluxo específico de Windows.
- **Bugs corrigidos:** Nenhum.

### 01/06/2026: Distribuição da Versão Compilada
- **Ações:** Atualizado `README.md` com seção para uso da versão compilada por usuários Windows sem Python instalado.
- **Decisões:** Distribuição recomendada inclui o `.exe` gerado em `dist` e o `README.md`; versão GUI compilada passa a ser o caminho preferencial para usuários finais Windows.
- **Bugs corrigidos:** Nenhum.

### 01/06/2026: Documentação de Mbox sem Extensão
- **Ações:** Atualizado `README.md` para esclarecer que arquivos mbox também podem não ter extensão, como os arquivos `Inbox`, `Sent` e pastas locais do Thunderbird.
- **Decisões:** Documentação passa a tratar "arquivo mbox" como formato, não como dependente da extensão `.mbox`.
- **Bugs corrigidos:** Nenhum.

### 05/06/2026: Correção de Erro em Mbox sem Extensão no GUI Compilado
- **Ações:** Alterados `dividir_mbox_gui.py` e `dividir_mbox.py` para ler o mbox de entrada via streaming binário com `BytesParser`; mantida escrita das saídas com `mailbox.mbox`; atualizado `README.md` com recomendação de recompilar o `.exe` após alteração e fechar o Thunderbird antes de processar arquivos do perfil.
- **Decisões:** A entrada não depende mais de `mailbox.mbox(create=False)`; arquivos mbox sem extensão do Thunderbird passam a ser lidos por `open(..., "rb")` e parseados por separadores `From `.
- **Bugs corrigidos:** GUI compilada retornava `Errno 22 Invalid argument` ao abrir `C:\Users\Cenf\Documents\Inbox` → abertura direta via `mailbox.mbox` era frágil no Windows/EXE para arquivo real sem extensão → substituída leitura de entrada por parser mbox em streaming.

### 05/06/2026: Correção Final para Executável GUI em Windows sem Python
- **Ações:** Removido uso de `mailbox.mbox` também na escrita das saídas em `dividir_mbox_gui.py` e `dividir_mbox.py`; saída passou a ser escrita em binário preservando o bloco mbox original; adicionados traceback detalhado no log da GUI, validação prévia de leitura do arquivo e título `Dividir mbox 1.1`; filtro do seletor agora cobre arquivos `.mbox` e arquivos sem extensão; recompilado `dist/dividir_mbox_gui.exe` com `py -m PyInstaller --onefile --windowed --clean dividir_mbox_gui.py`.
- **Decisões:** Versão distribuível Windows não depende mais de `mailbox.mbox` para entrada nem para saída, evitando lock/dotlock e chamadas frágeis no executável compilado.
- **Bugs corrigidos:** `Errno 22 Invalid argument` persistia no `.exe` distribuído em Windows sem Python → falha podia ocorrer na criação/bloqueio das saídas via `mailbox.mbox` mesmo após corrigir a entrada → escrita das saídas passou para `open(..., "ab")`.

### 05/06/2026: Diagnóstico Real de Bloqueio por Antivírus
- **Ações:** Atualizado `README.md` com seção de solução de problemas para `Errno 22` causado por antivírus bloqueando mbox com mensagem/anexo malicioso.
- **Decisões:** Diagnóstico final do caso reportado: o arquivo `Inbox` continha e-mail com malware e foi bloqueado pelo antivírus; as mudanças de leitura/escrita binária permanecem como robustez adicional, não como causa raiz principal do caso real.
- **Bugs corrigidos:** Erro no `.exe` GUI ao processar `Inbox` → antivírus bloqueava o arquivo por detecção de malware em e-mail armazenado → documentado procedimento seguro: verificar alerta/quarentena, fechar Thunderbird, usar cópia do mbox e tratar o arquivo como potencialmente contaminado.

### Tarefas Pendentes
- [x] Revisar `dividir_mbox.py` — solicitação atual do usuário.
- [x] Alterar `dividir_mbox.py` para solicitar o arquivo mbox — solicitação atual do usuário.
- [x] Adicionar opção de divisão por ano ou ano-mês — solicitação atual do usuário.
- [x] Criar versão GUI em `dividir_mbox_gui.py` — solicitação atual do usuário.
- [x] Criar `README.md` e `.gitignore` para distribuição — solicitação atual do usuário.
- [x] Documentar compatibilidade Linux da versão CLI — solicitação atual do usuário.
- [x] Documentar distribuição da versão compilada — solicitação atual do usuário.
- [x] Documentar arquivos mbox sem extensão do Thunderbird — solicitação atual do usuário.
- [x] Corrigir erro `Errno 22` na versão GUI compilada com arquivo `Inbox` sem extensão — solicitação atual do usuário.
- [x] Corrigir persistência do erro no `.exe` GUI distribuído para Windows sem Python — solicitação atual do usuário.
- [x] Documentar diagnóstico real de bloqueio por antivírus em mbox com malware — solicitação atual do usuário.
