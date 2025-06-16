
# 🐾 Controle de Vacinação de Pets - API RESTful

Este projeto é uma API RESTful desenvolvida para gerenciar o controle de vacinação de animais de estimação. O sistema permite o cadastro de tutores, pets e vacinas, possibilitando o acompanhamento completo do histórico vacinal dos animais.

## 🔧 Tecnologias Utilizadas

- Node.js
- Express.js
- SQLite3 ou PostgreSQL (adaptável)
- Sequelize (ORM)
- Nodemon (para ambiente de desenvolvimento)

## 🚀 Funcionalidades da API

### 🧑‍🤝‍🧑 Tutores
- `GET /tutores` - Listar todos os tutores
- `GET /tutores/:id` - Buscar tutor por ID
- `POST /tutores` - Criar um novo tutor
- `PUT /tutores/:id` - Atualizar dados do tutor
- `DELETE /tutores/:id` - Remover tutor

### 🐶 Pets
- `GET /pets` - Listar todos os pets
- `GET /pets/:id` - Buscar pet por ID
- `POST /pets` - Cadastrar novo pet
- `PUT /pets/:id` - Atualizar informações do pet
- `DELETE /pets/:id` - Remover pet

### 💉 Vacinas
- `GET /vacinas` - Listar todas as vacinas registradas
- `POST /vacinas` - Registrar uma nova vacina
- `PUT /vacinas/:id` - Atualizar registro de vacina
- `DELETE /vacinas/:id` - Remover vacina

## 🛠️ Como Executar Localmente

### Pré-requisitos

- [Node.js](https://nodejs.org/)
- [Git](https://git-scm.com/)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/controle-vacinacap-api.git
cd controle-vacinacap-api

# Instale as dependências
npm install

# Crie o banco de dados e execute as migrations (se aplicável)
npx sequelize db:migrate

# Inicie o servidor
npm start
```

A API será executada em: `http://localhost:3000`

## 🧪 Testes

Você pode utilizar ferramentas como o [Postman](https://www.postman.com/) ou [Insomnia](https://insomnia.rest/) para testar os endpoints da API.

## 📌 Objetivos Acadêmicos

Este projeto foi desenvolvido como parte da Avaliação A3 da unidade curricular **Sistemas Distribuídos e Mobile** do curso de **Sistemas de Informação**, com foco em:

- Estruturação de APIs RESTful
- Manipulação de banco de dados com ORM
- Organização em camadas (MVC)
- Boas práticas de desenvolvimento backend

## 📝 Licença

Este projeto é de uso acadêmico e está disponível sob a Licença MIT.
