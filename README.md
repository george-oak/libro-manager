# LibroManager

Sistema de gestión de inventario de libros con reposición automática mediante Celery y Redis.

## Estructura del Proyecto
```
libro-manager/
├── api/               # Endpoints API
├── books/             # App principal
├── libro_manager/     # Configuración Django
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
```

## Tecnologías Utilizadas
- Django 4.2
- Django REST Framework
- Celery + Redis (task queue)
- PostgreSQL
- Docker
- Pytest

## Configuración del Entorno

### Requisitos previos
- Docker 20.10+
- Docker Compose 2.0+
- Git

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/libro-manager.git
cd libro-manager
```

### 2. Construir y ejecutar contenedores
```bash
docker-compose up -d --build
```

### 3. Aplicar migraciones
```bash
docker-compose exec web python manage.py migrate
```


### 4. Crear Usuario
```bash
docker-compose exec web python manage.py createsuperuser
```

## Acceso
- Aplicación: http://localhost:8000

## Endpoints API
- POST /api/book/buy/<book_id>/ - Compra de libros
- Body:
```json
{
  "quantity": 3
}
```

## Ejecución de Tests
docker-compose run --rm web pytest