# Divisor de arquivos mbox

Ferramenta para dividir arquivos mbox por ano ou por ano-mes, mantendo as mensagens em formato mbox.

Arquivos mbox podem ter extensao `.mbox` ou nao ter extensao. O Thunderbird, por exemplo, armazena caixas como `Inbox`, `Sent`, `Archives` e outras pastas locais em arquivos mbox sem extensao.

## Arquivos

- `dividir_mbox.py`: versao de terminal.
- `dividir_mbox_gui.py`: versao com interface grafica Tkinter.

## Requisitos

- Windows ou Linux com Python 3 instalado para a versao de terminal.
- Windows com Python 3 e Tkinter disponivel para a versao grafica.
- Nenhuma dependencia externa para executar os scripts.
- PyInstaller apenas se for gerar `.exe`.

## Uso pela interface grafica

Execute:

```powershell
py dividir_mbox_gui.py
```

Na janela:

1. Selecione o arquivo mbox, com ou sem extensao.
2. Escolha `Por ano` ou `Por ano-mes`.
3. Clique em `Dividir mbox`.

Os arquivos gerados ficam no mesmo diretorio do arquivo original.

Exemplos:

```text
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

Gerar a versao grafica:

```powershell
py -m PyInstaller --onefile --windowed dividir_mbox_gui.py
```

O executavel sera criado em:

```text
dist\dividir_mbox_gui.exe
```

Gerar a versao terminal:

```powershell
py -m PyInstaller --onefile dividir_mbox.py
```

O executavel sera criado em:

```text
dist\dividir_mbox.exe
```

## Usar versao compilada

Para usuarios Windows sem Python instalado, distribua o arquivo compilado:

```text
dividir_mbox_gui.exe
```

O usuario deve executar o `.exe`, selecionar o arquivo mbox, escolher o modo de divisao e iniciar o processamento pela interface.

Se tambem distribuir a versao terminal compilada, o executavel correspondente sera:

```text
dividir_mbox.exe
```

## Observacoes de distribuicao

- Distribua preferencialmente o `.exe` gerado em `dist` para usuarios Windows.
- Inclua o `README.md` junto com a versao compilada.
- Nao inclua arquivos mbox reais no repositorio, mesmo quando nao tiverem extensao.
- Recomende que o usuario mantenha backup do mbox original antes da divisao.
- Reexecutar sobre o mesmo diretorio pode acrescentar mensagens aos arquivos de saida existentes.
