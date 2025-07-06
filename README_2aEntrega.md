# meu-checklist-tarefas-mvp

1ª Entrega trabalho PUC-Rio, CCE Extensão - Engenharia de Software (Michelle Rodrigues - Matricula 10914039709)

Para entender o Contexto/Executar a aplicação pela primeira vez (sprint anterior):
Leia: README_1aEntrega.md

Melhorias efetuadas:

1 - Disponibilização de Cadastro de Tarefa para o usuário, com inteligência artifical no backend,
<<imagem>>

2 - Implementação de Software integigente com análise preditiva para a classificação de Tarefas em suas categorias.
2.1 - Execute o Notebook em: 
https://colab.research.google.com/drive/1gA8DLnlkgyxXSB6EuBQrHeFNfOAEcLCw?usp=sharing

3 - Integração Front x Backend na rota de cadastro de tarefas. Onde o usuário digita a tarefa e o backend prevê a categoria

4 - Incorporação e melhoria da base de dados, agora com +10K de tarefas cadastradas
4.1 - Utilização de MLA ([manus](https://manus.im/app)) para gerar tarefas para o dataset

5 - Disponibilização do dataset exemplo utilizado na solução. 
<<LInk do Git>>

6 - Implementação de testes de Automatizados para verificação de acurária e probabilidade






Esta solução PerSpecML => 
US1 - COMO usuária do site meu-checklist-tarefas QUERO realizar a classificação automática de uma tarefa PARA saber em qual categoria ela se encaixa melhor.

Veja a apresentação do site em: https://www.youtube.com/watch?v=J5EoOjXckBQ

## Configuração do Ambiente

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/michellerodrigues/meu-checklist-tarefas-api.git
    cd meu-checklist-tarefas-api
    ```

2. **Crie e ative um ambiente virtual**:
    - **Linux/MacOS**:
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```
    - **Windows**:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3. **Instale as dependências da api**:
    ```bash
    cd api
    pip install -r dependencias.txt
    ```


4. **Configuração do Banco de Dados**:
    - Crie/copie o arquivo `config.env` na raiz do projeto (/api)
    - Exemplo de conteúdo:
        ```env
        SQLALCHEMY_DATABASE_URL=sqlite:///database/banco_tarefas.sqlite3
        ```

5. **Execute a aplicação**:
A escolha do uvicorn + FastApi ajudou na documentação automática, para colocar o swagger :)

    ```bash
    pip install -e .
    python -m uvicorn src.main:app --reload --port 8002
    ```

7. **Acesse a documentação**:
    ```
    http://localhost:8002/meu-checklist-tarefas-doc
    ```


## Estrutura do Projeto


```text
meu-checklist-tarefas-api/
./src
├── database/
│   ├── banco_tarefas.sqlite3
│   ├── database.py
├── models/
│   ├── base.py
│   ├── categoria.py
│   ├── questionario.py
│   ├── usuario.py
│   ├── __init__.py
├── routers/
│   ├── autenticacao.py
│   ├── categorias.py
│   ├── questionario.py
│   ├── __init__.py
├── schemas/
│   ├── base.py
│   ├── categoria.py
│   ├── converters.py
│   ├── questionario.py
│   ├── usuario.py
│   ├── __init__.py
├── security/
│   ├── security.py
│   ├── __init__.py
├── services/
│   ├── autenticacao.py
│   ├── categorias.py
│   ├── questionario.py
├── config.env
├── dependencias.txt
├── main.py
├── __init__.py
```

## Solução de Problemas Comuns

1. **Erro ao instalar dependências**

   - Verifique se o arquivo `dependencias.txt` existe
   - Atualize o pip: `python -m pip install --upgrade pip`


2. **Erro de conexão com o banco de dados**:
   - Verifique o caminho no `config.env`
   - Garanta permissões de escrita no diretório

3. **Documentação não encontrada**:
   - Confira se a aplicação está rodando na porta correta
   - Acesse `/meu-checklist-tarefas-doc` em vez do caminho mencionado anteriormente


## BANCO DE DADOS - Meu checkList Tarefas

<img width="497" alt="image" src="https://github.com/user-attachments/assets/04b3917e-429b-47a6-93f1-1eda663fa253" />

## Apresentação Aplicativo

[MeuCheckLisTarefas-Apresentação.pptx](https://github.com/user-attachments/files/19722216/MeuCheckLisTarefas-Apresentacao.pptx)

## Telas Aplicativo (futuro)

![fluxo_completo](https://github.com/user-attachments/assets/beb3dc38-6277-4e82-adb0-34020c4abcc3)

## Expectativa x MVP (Frontend entregue - versão web)

1 - Tela de Login
![image](https://github.com/user-attachments/assets/14a04544-b879-4313-ae9b-ddd055b5ec07)

2 - Tela de Cadastro
![image](https://github.com/user-attachments/assets/50331b2b-1c65-4eee-abd9-7d54ca6ed842)

3 - Tela de Questionário
![image](https://github.com/user-attachments/assets/695a4bb0-f08a-40db-a35c-200f0d52e426)

4 - Painel do Usuário
![image](https://github.com/user-attachments/assets/9ce0493c-f579-4547-a79f-141c56a75b9e)


## Frontend entregue - versão web

1 - Para executar:
  ```
    > git clone https://github.com/michellerodrigues/meu-checklist-tarefas-mvp.git
    > cd meu-checklist-tarefas-mvp/front
    > python -m http.server 8005
  ```


2 - Estrutura de Pastas
```text
./front
├── cadastro.css
├── cadastro.html
├── index.css
├── index.html
├── painelUsuario.css
├── painelUsuario.html
├── questionario.css
├── questionario.html
├── readme.md
├── js/
│   ├── index.js
│   ├── painelUsuario.js
│   ├── questionario.js
│   ├── script-cadastro.js
│   ├── scripts.js


```



OBRIGADA POR LER ATÉ AQUI!!!! :)
