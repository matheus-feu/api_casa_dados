[![wakatime](https://wakatime.com/badge/user/3bd24664-869f-460a-94e1-b98da8136504/project/018b554b-1b9d-432e-8ece-afd73bad6c25.svg)](https://wakatime.com/badge/user/3bd24664-869f-460a-94e1-b98da8136504/project/018b554b-1b9d-432e-8ece-afd73bad6c25)

<h2 align="center"> API Casa dos Dados - Web Scraping 🚀 </h2> 

## 📖 Sobre

Esta API foi desenvolvida para o projeto do site [Casa dos Dados](https://casadosdados.com.br/), que tem como objetivo
facilitar o acesso a dados públicos
através de endpoints RESTful. A API faz uso do framework [FastAPI](https://fastapi.tiangolo.com/) e utiliza do RPA (
Robotic Process Automation) para realizar a coleta de dados.

Os dados são retornados em formato JSON, e é possível realizar o download dos dados em formato Excel e armazenar no
banco de dados MongoDB.

Necessário realizar cadastro no sistema para ter acesso aos endpoints. A API está com seguro com autenticação JWT.

## 🚀 Tecnologias utilizadas

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Pycharm](https://img.shields.io/badge/pycharm-%23000000.svg?style=for-the-badge&logo=pycharm&logoColor=white)
![Postman](https://img.shields.io/badge/postman-%23FF6C37.svg?style=for-the-badge&logo=postman&logoColor=white)

## ⚙️ Instalação

#### 💻 Pré-requisitos

Antes de começar você vai precisar ter instalado em sua máquina as seguintes ferramentas:

- Você instalar o versão mais recente do [Python](https://www.python.org/downloads/), estou utilizando a 3.11.
- Você precisa instalar o [MongoDB](https://www.mongodb.com/try/download/community) para armazenar os dados ou utilizar
  o [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register).
- Você precisa instalar o [PyCharm](https://www.jetbrains.com/pt-br/pycharm/download/) para desenvolver o projeto.
- Ter instalado o [Git](https://git-scm.com/downloads) para clonar o projeto.

Com tudo instalado, você pode seguir os passos abaixo:

#### 🎲 Rodando o projeto

- Clone este repositório

```bash
$ git clone https://github.com/matheus-feu/api_casa_dados.git
```

- Acesse a pasta do projeto no terminal/cmd

```bash
$ cd api_casa_dados
```

- Crie um ambiente virtual com o Python

```bash
$ python -m venv venv
```

- Ative o ambiente virtual

```bash
$ venv\Scripts\activate
```

- Instale as dependências

```bash
$ pip install -r requirements.txt
```

Ou caso esteja utilizando poetry igual a mim, basta rodar o comando abaixo:

```bash
$ poetry install
```

```bash
$ poetry shell
```

- Crie um arquivo `.env` na raiz do projeto e adicione as variáveis de ambiente que estão no arquivo `.env.example`

```bash
$ touch .env
```

## 📌 Endpoints

## Endpoint de Consulta Básica

### Descrição

Este endpoint permite realizar uma pesquisa básica de dados de uma empresa. Onde é necessário informar o CNPJ da
empresa, que irá retornar os dados da empresa e os dados dos sócios.

O endpoint retorna os dados na seguinte estrutura:

```json
{
  "result": {}
}
```

Onde `result` é um dicionário com os dados da empresa e o quadro societário.

### URL do Endpoint

- `POST /api/v1/scraping_data/basic_search`

### Parâmetros da Solicitação

- `cnpj`: O CNPJ da empresa que deseja consultar.

### Exemplo de Solicitação

```http
POST /api/v1/scraping_data/basic_search
Content-Type: application/json
```

```json
{
  "cnpj": "00000000000000"
}
```

## Endpoint de Consulta Avançada

### Descrição

Este endpoint permite realizar uma pesquisa avançada de dados de uma empresa.

Os parâmetros são opcionais, e a quantidade de páginas é limitada a 50. Caso deseje quantas páginas sejam retornadas,
basta passar o
parâmetro `qnt_pages` com o valor desejado, irá avaliar a quantidade de resultados com a quantidade de páginas e trazer
o valor menor.

Ao enviar cada parâmetro, irá preencher o campo de pesquisa com o valor informado.

O endpoint retorna os dados na seguinte estrutura:

```json
{
  "results": [
    {}
  ],
  "num_results": "string",
  "qnt_pages": 0
}
```

Onde `results` é uma lista de dicionários com os dados da empresa, `num_results` é a quantidade de resultados
encontrados e `qnt_pages` é a quantidade de páginas retornadas.

### URL do Endpoint

- `POST /api/v1/scraping_data/advanced_search`

### Parâmetros da Solicitação

- `cep`: O CEP da empresa que deseja consultar.
- `city`: A cidade da empresa que deseja consultar.
- `cnae`: O CNAE da empresa que deseja consultar.
- `date_from`: A data inicial da empresa que deseja consultar.
- `date_to`: A data final da empresa que deseja consultar.
- `ddd`: O DDD da empresa que deseja consultar.
- `legal_nature`: A natureza jurídica da empresa que deseja consultar.
- `neighborhood`: O bairro da empresa que deseja consultar.
- `qnt_pages`: A quantidade de páginas que deseja retornar, máximo de 50.
- `share_capital_from`: O capital social inicial da empresa que deseja consultar.
- `share_capital_to`: O capital social final da empresa que deseja consultar.
- `situation`: A situação da empresa que deseja consultar.
- `social_reason`: A razão social da empresa que deseja consultar.
- `state`: O estado da empresa que deseja consultar.

### Exemplo de Solicitação

```http
POST /api/v1/scraping_data/advanced_search
Content-Type: application/json
```

```json
{
  "cep": "04117091",
  "city": "São Paulo",
  "cnae": 123456,
  "date_from": "2021-01-01",
  "date_to": "2021-01-31",
  "ddd": 11,
  "legal_nature": "1015 - SOCIEDADE ANÔNIMA FECHADA",
  "neighborhood": "Vila Mariana",
  "qnt_pages": 1,
  "share_capital_from": 1000,
  "share_capital_to": 100000,
  "situation": "ATIVA",
  "social_reason": "Empresa Teste",
  "state": "SP"
}
```

## 📚 Bibliotecas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- [PyMongo](https://pymongo.readthedocs.io/en/stable/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests](https://docs.python-requests.org/en/latest/)
- [Selenium](https://selenium-python.readthedocs.io/)

## 📞 Contato

- [Linkedin](https://www.linkedin.com/in/matheus-feu-558558186/)
- [GitHub](https://github.com/matheus-feu)
- [Instagram](https://www.instagram.com/math_feu/)
- [Gmail](mailto:matheusfeu@gmail.com)