# Listado de Endpoints API - BibliTech

API RESTful para la gestión de préstamo de libros.

**Prefijo de API:** `/api/v` (todos los endpoints llevan este prefijo)

**Ejemplo:** Para el endpoint `/libros`, la URL completa es: `GET /api/v/libros`

---

## Módulo 1 - Gestión de Préstamos

### Préstamos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/prestamos` | Crear un nuevo préstamo |
| `GET` | `/api/v/prestamos` | Listar todos los préstamos (bibliotecario) |
| `GET` | `/api/v/prestamos/lector` | Listar préstamos del lector actual |
| `POST` | `/api/v/prestamos/confirmar-entrega` | Confirmar la entrega de un préstamo |
| `POST` | `/api/v/prestamos/{codigo_interno}/confirmar-devolucion` | Registrar la devolución de un préstamo |

### Ejemplares

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/ejemplares` | Crear un nuevo ejemplar |
| `GET` | `/api/v/ejemplares` | Listar todos los ejemplares |
| `GET` | `/api/v/ejemplares/codigo/{codigo_interno}` | Obtener ejemplar por código interno |
| `GET` | `/api/v/ejemplares/{id}` | Obtener ejemplar por ID |
| `PUT` | `/api/v/ejemplares/{id}` | Actualizar un ejemplar |
| `PATCH` | `/api/v/ejemplares/{id}/estado` | Actualizar estado de un ejemplar |
| `DELETE` | `/api/v/ejemplares/{id}` | Eliminar un ejemplar |

---

## Módulo 2 - Gestión de Libros y Autores

### Libros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/libros` | Crear un nuevo libro |
| `GET` | `/api/v/libros` | Listar todos los libros |
| `GET` | `/api/v/libros/{id}` | Obtener libro por ID |
| `PUT` | `/api/v/libros/{id}` | Actualizar un libro |
| `PATCH` | `/api/v/libros/{id}/imagen` | Actualizar imagen de un libro |
| `DELETE` | `/api/v/libros/{id}` | Eliminar un libro |

### Autores

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/autores` | Crear un nuevo autor |
| `GET` | `/api/v/autores` | Listar todos los autores |
| `GET` | `/api/v/autores/{id}` | Obtener autor por ID |
| `PUT` | `/api/v/autores/{id}` | Actualizar un autor |
| `DELETE` | `/api/v/autores/{id}` | Eliminar un autor |

### Categorías

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/categorias` | Crear una nueva categoría |
| `GET` | `/api/v/categorias` | Listar todas las categorías |
| `GET` | `/api/v/categorias/{id}` | Obtener categoría por ID |
| `PUT` | `/api/v/categorias/{id}` | Actualizar una categoría |
| `DELETE` | `/api/v/categorias/{id}` | Eliminar una categoría |

---

## Módulo 3 - Gestión de Usuarios y Roles

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/auth/registro` | Registrar un nuevo usuario |
| `POST` | `/api/v/auth/inicio-sesion` | Iniciar sesión |
| `GET` | `/api/v/auth/yo` | Obtener usuario actual |

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/usuarios` | Crear un nuevo usuario (admin) |
| `GET` | `/api/v/usuarios` | Listar todos los usuarios |
| `GET` | `/api/v/usuarios/{id}` | Obtener usuario por ID |
| `GET` | `/api/v/usuarios/{documento}/prestamo` | Obtener usuario por documento |
| `PUT` | `/api/v/usuarios/{id}/perfil` | Actualizar perfil de usuario |
| `PUT` | `/api/v/usuarios/{id}/admin` | Actualizar usuario por admin |
| `PUT` | `/api/v/usuarios/{id}/contrasena` | Actualizar contraseña |
| `POST` | `/api/v/usuarios/resetear-contrasena` | Solicitar restablecimiento de contraseña |
| `POST` | `/api/v/usuarios/verificar-token` | Verificar token y restablecer contraseña |
| `DELETE` | `/api/v/usuarios/{id}/suave` | Eliminar usuario (soft delete) |
| `DELETE` | `/api/v/usuarios/{id}` | Eliminar usuario permanentemente |

### Roles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/roles` | Crear un nuevo rol |
| `GET` | `/api/v/roles` | Listar todos los roles |
| `GET` | `/api/v/roles/{id}` | Obtener rol por ID |
| `PUT` | `/api/v/roles/{id}` | Actualizar un rol |
| `DELETE` | `/api/v/roles/{id}` | Eliminar un rol |

### Estados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/estados` | Crear un nuevo estado |
| `GET` | `/api/v/estados` | Listar todos los estados |
| `GET` | `/api/v/estados/tipo` | Listar estados por tipo |
| `GET` | `/api/v/estados/{id}` | Obtener estado por ID |
| `PUT` | `/api/v/estados/{id}` | Actualizar un estado |
| `DELETE` | `/api/v/estados/{id}` | Eliminar un estado |

### Tipos de Documento

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v/tipos-documento` | Crear un nuevo tipo de documento |
| `GET` | `/api/v/tipos-documento` | Listar todos los tipos de documento |
| `GET` | `/api/v/tipos-documento/{id}` | Obtener tipo de documento por ID |
| `PUT` | `/api/v/tipos-documento/{id}` | Actualizar un tipo de documento |
| `DELETE` | `/api/v/tipos-documento/{id}` | Eliminar un tipo de documento |

### Auditorías

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v/auditorias` | Listar registros de auditoría |
| `GET` | `/api/v/auditorias/{id}` | Obtener registro de auditoría por ID |

---

## Códigos de Respuesta HTTP

| Código | Descripción |
|--------|-------------|
| `200` | OK - Operación exitosa |
| `201` | Created - Recurso creado exitosamente |
| `204` | No Content - Eliminación exitosa |
| `400` | Bad Request - Datos inválidos |
| `401` | Unauthorized - No autenticado |
| `403` | Forbidden - Sin permisos |
| `404` | Not Found - Recurso no encontrado |
| `500` | Internal Server Error - Error del servidor |

---

## Parámetros de Consulta (Query Parameters)

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `page` | `int` | Número de página (mínimo: 1) |
| `page_size` | `int` | Items por página (1-100) |
| `normalizado` | `bool` | Formato normalizado de respuesta |

---

## Autenticación

Todos los endpoints (excepto `/auth/registro` y `/auth/inicio-sesion`) requieren autenticación JWT.

**Header requerido:**
```
Authorization: Bearer {access_token}
```
