# Docker - Guía de Uso de BibliTech

Esta guía explica cómo usar Docker para ejecutar la aplicación BibliTech.

## Requisitos Previos

- Docker Engine (versión 20.10 o superior)
- Docker Compose (versión 2.0 o superior)

## Configuración Rápida

### 1. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura las variables necesarias:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus valores específicos. Las variables más importantes son:

- `POSTGRES_USER`: Usuario de PostgreSQL
- `POSTGRES_PASSWORD`: Contraseña de PostgreSQL
- `POSTGRES_DB`: Nombre de la base de datos
- `JWT_SECRET`: Clave secreta para JWT (cambiar en producción)
- Configuración de correo electrónico (MAIL_*)
- Configuración de Cloudflare R2 (R2_*)

### 2. Iniciar los Servicios

Para iniciar la aplicación y la base de datos:

```bash
docker-compose up -d
```

Esto iniciará dos contenedores:
- `biblitech-db`: Base de datos PostgreSQL
- `biblitech-api`: Aplicación FastAPI

### 3. Verificar el Estado

Verifica que los contenedores estén corriendo:

```bash
docker-compose ps
```

Ver los logs de la aplicación:

```bash
docker-compose logs -f app
```

Ver los logs de la base de datos:

```bash
docker-compose logs -f db
```

### 4. Acceder a la Aplicación

- API: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

## Comandos Útiles

### Detener los Servicios

```bash
docker-compose down
```

### Detener y Eliminar Volúmenes (Base de Datos)

⚠️ **Advertencia**: Este comando eliminará todos los datos de la base de datos.

```bash
docker-compose down -v
```

### Reconstruir las Imágenes

Si realizas cambios en el código o en requirements.txt:

```bash
docker-compose up -d --build
```

### Ejecutar Comandos en el Contenedor

Acceder al contenedor de la aplicación:

```bash
docker-compose exec app bash
```

Acceder a la base de datos PostgreSQL:

```bash
docker-compose exec db psql -U biblitech -d biblitech
```

### Ver Logs en Tiempo Real

```bash
docker-compose logs -f
```

### Reiniciar un Servicio Específico

```bash
docker-compose restart app
```

## Uso Solo con Dockerfile

Si prefieres usar solo el Dockerfile sin docker-compose:

### 1. Construir la Imagen

```bash
docker build -t biblitech-api .
```

### 2. Ejecutar el Contenedor

```bash
docker run -d \
  --name biblitech-api \
  -p 8000:8000 \
  --env-file .env \
  biblitech-api
```

**Nota**: Necesitarás tener PostgreSQL ejecutándose y accesible desde el contenedor.

## Modo Producción

Para ejecutar en producción, considera los siguientes cambios:

### 1. Modificar el docker-compose.yml

En el servicio `app`, cambia el comando para no usar `--reload`:

```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2. Variables de Entorno Críticas

Asegúrate de cambiar:
- `JWT_SECRET`: Usa un valor aleatorio y seguro
- `POSTGRES_PASSWORD`: Usa una contraseña fuerte
- No expongas puertos innecesarios

### 3. Usar un Proxy Reverso

Se recomienda usar Nginx o Traefik como proxy reverso para:
- SSL/TLS
- Balanceo de carga
- Cache
- Seguridad adicional

## Migraciones de Base de Datos

Si la aplicación usa migraciones (Alembic u otro):

```bash
docker-compose exec app alembic upgrade head
```

## Respaldo de la Base de Datos

### Crear Backup

```bash
docker-compose exec db pg_dump -U biblitech biblitech > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restaurar Backup

```bash
cat backup.sql | docker-compose exec -T db psql -U biblitech biblitech
```

## Solución de Problemas

### El contenedor no inicia

1. Verifica los logs: `docker-compose logs app`
2. Verifica que todas las variables de entorno estén configuradas correctamente
3. Asegúrate de que los puertos no estén en uso

### Error de conexión a la base de datos

1. Verifica que el servicio de base de datos esté corriendo: `docker-compose ps db`
2. Verifica la salud de la base de datos: `docker-compose logs db`
3. Asegúrate de que las credenciales en `.env` sean correctas

### Cambios en el código no se reflejan

1. Reconstruye la imagen: `docker-compose up -d --build`
2. O usa volúmenes de desarrollo (ya configurado en docker-compose.yml)

## Seguridad

- **Nunca** commits el archivo `.env` al repositorio
- Cambia `JWT_SECRET` a un valor único y seguro en producción
- Usa contraseñas fuertes para la base de datos
- Mantén Docker y las imágenes actualizadas
- Revisa regularmente las vulnerabilidades con `docker scan biblitech-api`

## Recursos Adicionales

- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/docker/)
