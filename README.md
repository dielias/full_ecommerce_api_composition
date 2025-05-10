# Full Ecommerce API - Microservices Architecture

Este projeto é uma aplicação de ecommerce implementada com **FastAPI**, estruturada com **arquitetura de microserviços** e utilizando o padrão **Per Service Database** e **API Composition** para integração.

## 🧱 Estrutura do Projeto

```
.
├── docker-compose.yml
├── services
│   ├── api-composer        # Serviço que compõe dados dos outros microserviços
│   ├── users               # Microserviço de usuários
│   ├── products            # Microserviço de produtos
│   ├── orders              # Microserviço de pedidos
│   └── db-init             # Inicialização dos bancos
├── tests                   # Testes automatizados
```

Cada microserviço possui seu próprio banco de dados PostgreSQL e API independente.

## 🚀 Como Executar

### Pré-requisitos

- Docker
- Docker Compose
- Python 3.12

### Subir os serviços

```bash
docker compose up --build
```

Isso inicializa todos os serviços e bancos de dados. A aplicação estará disponível nos seguintes endpoints:

| Serviço      | Porta | Endereço Base         |
|--------------|-------|------------------------|
| Users        | 8001  | `http://localhost:8001` |
| Products     | 8002  | `http://localhost:8002` |
| Orders       | 8003  | `http://localhost:8003` |
| API Composer | 8000  | `http://localhost:8000` |

## 🔌 Endpoints

### API Composer

- `GET /composed-orders` → Lista de pedidos com detalhes de usuário e produto.

### Users

- `GET /users` - List users
- `GET /users/{user_id}` - Get user by user_id
- `POST /users` - Create user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Products

- `GET /products` - List products
- `GET /products/{product_id}` - Get product by product_id
- `POST /products` - Create product
- `PUT /products/{product_id}` - Update product
- `DELETE /products/{product_id}` - Delete product

### Orders

- `GET /orders` - List orders
- `GET /orders/{order_id}` - Get order by order_id
- `POST /orders` - Create order
- `PUT /orders/{order_id}` - Update order
- `DELETE /orders/{order_id}` - Delete oder

## 🧪 Testes

Para rodar os testes (fora do docker):

```bash
cd tests
pytest
```

## 📦 Tecnologias

- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker & Docker Compose
- Pydantic
- Pytest

## 🛠️ Arquitetura

- **API Composition**: Um serviço `api-composer` agrega dados de `users`, `products` e `orders`.
- **Per Service Database**: Cada microserviço possui seu próprio banco PostgreSQL.
- **Isolamento total**: Microserviços não compartilham modelos ou banco de dados.

## 📝 Licença

Este projeto está licenciado sob a licença MIT.

## 🧑‍💻 Autor

Desenvolvido por Dinah (https://github.com/dielias)
