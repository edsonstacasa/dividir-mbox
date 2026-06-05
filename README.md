# Divisor de arquivos mbox

Ferramenta para dividir arquivos mbox por ano ou por ano-mês, mantendo as mensagens em formato mbox.

Arquivos mbox podem ter extensão `.mbox` ou nao ter extensão. O Thunderbird, por exemplo, armazena caixas como `Inbox`, `Sent`, `Archives` e outras pastas locais em arquivos mbox sem extensão.

## Arquivos

- `dividir_mbox.py`: versão de terminal.
- `dividir_mbox_gui.py`: versão com interface grafica Tkinter.

## Requisitos

- Windows ou Linux com Python 3 instalado para a versão de terminal.
- Windows com Python 3 e Tkinter disponível para a versão grafica.
- Nenhuma dependência externa para executar os scripts.
- PyInstaller apenas se for gerar `.exe`.

## Uso pela interface grafica

Execute:

```powershell
py dividir_mbox_gui.py
```

Na janela:

1. Selecione o arquivo mbox, com ou sem extensão.
2. Escolha `Por ano` ou `Por ano-mes`.
3. Clique em `Dividir mbox`.

Os arquivos gerados ficam no mesmo diretorio do arquivo original.

Exemplos:

```text
Inbox_2024
Inbox_2024-03
Inbox_2024.mbox
Inbox_2024-03.mbox
Inbox_sem_data.mbox
Inbox_erro_data.mbox
```

## Uso pelo terminal

No Windows:

```powershell
py dividir_mbox.py
```

No Linux:

```bash
python3 dividir_mbox.py
```

Informe o caminho do arquivo quando solicitado e selecione o modo de divisao:

```text
1 - Por ano
2 - Por ano-mes
```

## Gerar executavel Windows

Instale o PyInstaller:

```powershell
py -m pip install pyinstaller
```

Gerar a versão grafica:

```powershell
py -m PyInstaller --onefile --windowed --clean dividir_mbox_gui.py
```

O executavel sera criado em:

```text
dist\dividir_mbox_gui.exe
```

Sempre recompile o `.exe` apos alterar `dividir_mbox_gui.py`.

Gerar a versão terminal:

```powershell
py -m PyInstaller --onefile --clean dividir_mbox.py
```

O executavel sera criado em:

```text
dist\dividir_mbox.exe
```

## Usar versão compilada

Para usuarios Windows sem Python instalado, distribua o arquivo compilado:

```text
dividir_mbox_gui.exe
```

O usuario deve executar o `.exe`, selecionar o arquivo mbox, escolher o modo de divisao e iniciar o processamento pela interface.

Se tambem distribuir a versão terminal compilada, o executavel correspondente sera:

```text
dividir_mbox.exe
```

## Observacoes de distribuicao

- Distribua preferencialmente o `.exe` gerado em `dist` para usuarios Windows.
- Inclua o `README.md` junto com a versão compilada.
- Nao inclua arquivos mbox reais no repositorio, mesmo quando nao tiverem extensão.
- Mantenha backup do mbox original antes da divisão.
- Fechar o Thunderbird antes de dividir arquivos da pasta de perfil.
- Reexecutar sobre o mesmo diretório pode acrescentar mensagens aos arquivos de saída existentes.

## Solucao de problemas

Erro semelhante a:

```text
[Errno 22] Invalid argument: 'C:\\Users\\Usuario\\Documents\\Inbox'
```

pode ocorrer quando o antivirus bloqueia o acesso ao arquivo mbox. Isso é comum quando o arquivo `Inbox` ou outra pasta do Thunderbird contém uma mensagem ou anexo identificado como malware.

Nesse caso:

- verifique o alerta ou quarentena do antivirus;
- mantenha o Thunderbird fechado durante o processamento;
- trabalhe sempre sobre uma cópia do arquivo mbox original;
- trate o arquivo como potencialmente contaminado até concluir a análise de segurança.