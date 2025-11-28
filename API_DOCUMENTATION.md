# Listado de Endpoints API - BibliTech

API RESTful para la gestión de préstamo de libros.

**Prefijo de API:** `/api/v` (todos los endpoints llevan este prefijo)

**Ejemplo:** Para el endpoint `/libros`, la URL completa es: `GET /api/v/libros`

---

## Módulo 1 - Gestión de Préstamos

### Préstamos

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/prestamos` | Crear un nuevo préstamo | `201` | `"Préstamo creado exitosamente con el ejemplar {codigo_interno}."` |
| | | | `400` | `"No hay ejemplares disponibles para el libro solicitado."` |
| `GET` | `/api/v/prestamos` | Listar todos los préstamos (bibliotecario) | `200` | Lista de préstamos en JSON |
| `GET` | `/api/v/prestamos/lector` | Listar préstamos del lector actual | `200` | Lista de préstamos del usuario en JSON |
| `POST` | `/api/v/prestamos/confirmar-entrega` | Confirmar la entrega de un préstamo | `200` | `"Entrega confirmada. El ejemplar fue marcado como prestado."` |
| | | | `200` | `"No existe un préstamo reservado para este usuario y ejemplar."` |
| `POST` | `/api/v/prestamos/{codigo_interno}/confirmar-devolucion` | Registrar la devolución de un préstamo | `200` | `"Devolución registrada correctamente."` |
| | | | `200` | `"No existe un préstamo activo para este ejemplar."` |

### Ejemplares

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/ejemplares` | Crear un nuevo ejemplar | `201` | Objeto ejemplar creado en JSON |
| `GET` | `/api/v/ejemplares` | Listar todos los ejemplares | `200` | Lista de ejemplares en JSON |
| `GET` | `/api/v/ejemplares/codigo/{codigo_interno}` | Obtener ejemplar por código interno | `200` | Objeto ejemplar en JSON |
| | | | `404` | `"Ejemplar no encontrado"` |
| `GET` | `/api/v/ejemplares/{id}` | Obtener ejemplar por ID | `200` | Objeto ejemplar en JSON |
| | | | `404` | `"Ejemplar no encontrado"` |
| `PUT` | `/api/v/ejemplares/{id}` | Actualizar un ejemplar | `200` | Objeto ejemplar actualizado en JSON |
| | | | `404` | `"Ejemplar no encontrado"` |
| `PATCH` | `/api/v/ejemplares/{id}/estado` | Actualizar estado de un ejemplar | `200` | `"Estado del ejemplar actualizado correctamente"` |
| | | | `200` | `"El ejemplar ya tiene el estado especificado"` |
| | | | `400` | `"El estado no es válido para actualizar el ejemplar"` |
| | | | `404` | `"Ejemplar no encontrado"` |
| `DELETE` | `/api/v/ejemplares/{id}` | Eliminar un ejemplar | `200` | `"Ejemplar eliminado correctamente"` |
| | | | `404` | `"Ejemplar no encontrado"` |

---

## Módulo 2 - Gestión de Libros y Autores

### Libros

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/libros` | Crear un nuevo libro | `201` | Objeto libro creado en JSON |
| | | | `400` | `"Autores no encontrados: {ids}"` |
| `GET` | `/api/v/libros` | Listar todos los libros | `200` | Lista de libros en JSON |
| `GET` | `/api/v/libros/{id}` | Obtener libro por ID | `200` | Objeto libro en JSON |
| | | | `404` | `"Libro no encontrado"` |
| `PUT` | `/api/v/libros/{id}` | Actualizar un libro | `200` | Objeto libro actualizado en JSON |
| | | | `400` | `"Autores no encontrados: {ids}"` |
| | | | `404` | `"Libro no encontrado"` |
| `PATCH` | `/api/v/libros/{id}/imagen` | Actualizar imagen de un libro | `200` | Objeto con URL de imagen en JSON |
| | | | `404` | `"Libro no encontrado"` |
| `DELETE` | `/api/v/libros/{id}` | Eliminar un libro | `200` | `"Libro eliminado exitosamente"` |
| | | | `404` | `"Libro no encontrado"` |

### Autores

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/autores` | Crear un nuevo autor | `201` | Objeto autor creado en JSON |
| `GET` | `/api/v/autores` | Listar todos los autores | `200` | Lista de autores en JSON |
| `GET` | `/api/v/autores/{id}` | Obtener autor por ID | `200` | Objeto autor en JSON |
| | | | `404` | `"Autor no encontrado"` |
| `PUT` | `/api/v/autores/{id}` | Actualizar un autor | `200` | Objeto autor actualizado en JSON |
| | | | `404` | `"Autor no encontrado"` |
| `DELETE` | `/api/v/autores/{id}` | Eliminar un autor | `200` | `"Autor eliminado con éxito"` |
| | | | `404` | `"Autor no encontrado"` |

### Categorías

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/categorias` | Crear una nueva categoría | `201` | Objeto categoría creada en JSON |
| `GET` | `/api/v/categorias` | Listar todas las categorías | `200` | Lista de categorías en JSON |
| `GET` | `/api/v/categorias/{id}` | Obtener categoría por ID | `200` | Objeto categoría en JSON |
| | | | `404` | `"Categoría no encontrada"` |
| `PUT` | `/api/v/categorias/{id}` | Actualizar una categoría | `200` | Objeto categoría actualizada en JSON |
| | | | `404` | `"Categoría no encontrada"` |
| `DELETE` | `/api/v/categorias/{id}` | Eliminar una categoría | `200` | `"Categoría eliminada exitosamente"` |
| | | | `404` | `"Categoría no encontrada"` |

---

## Módulo 3 - Gestión de Usuarios y Roles

### Autenticación

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/auth/registro` | Registrar un nuevo usuario | `201` | Objeto usuario creado en JSON |
| `POST` | `/api/v/auth/inicio-sesion` | Iniciar sesión | `200` | `{"access_token": "...", "refresh_token": "...", "token_type": "bearer"}` |
| | | | `401` | `"Credenciales inválidas"` |
| `GET` | `/api/v/auth/yo` | Obtener usuario actual | `200` | Objeto usuario en JSON |
| | | | `401` | `"No autenticado"` |

### Usuarios

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/usuarios` | Crear un nuevo usuario (admin) | `201` | Objeto usuario creado en JSON |
| `GET` | `/api/v/usuarios` | Listar todos los usuarios | `200` | Lista de usuarios en JSON |
| `GET` | `/api/v/usuarios/{id}` | Obtener usuario por ID | `200` | Objeto usuario en JSON |
| | | | `404` | `"Usuario no encontrado"` |
| `GET` | `/api/v/usuarios/{documento}/prestamo` | Obtener usuario por documento | `200` | Objeto usuario en JSON o `null` |
| `PUT` | `/api/v/usuarios/{id}/perfil` | Actualizar perfil de usuario | `200` | Objeto usuario actualizado en JSON |
| | | | `404` | `"Usuario no encontrado"` |
| `PUT` | `/api/v/usuarios/{id}/admin` | Actualizar usuario por admin | `200` | Objeto usuario actualizado en JSON |
| | | | `404` | `"Usuario no encontrado"` |
| `PUT` | `/api/v/usuarios/{id}/contrasena` | Actualizar contraseña | `200` | `"Contraseña actualizada exitosamente"` |
| | | | `400` | `"Contraseña actual incorrecta"` |
| | | | `404` | `"Usuario no encontrado"` |
| `POST` | `/api/v/usuarios/resetear-contrasena` | Solicitar restablecimiento de contraseña | `200` | `"Correo de restablecimiento enviado"` |
| | | | `404` | `"Usuario no encontrado"` |
| `POST` | `/api/v/usuarios/verificar-token` | Verificar token y restablecer contraseña | `200` | `"Contraseña restablecida exitosamente"` |
| | | | `400` | `"Token inválido"` |
| | | | `400` | `"Token expirado"` |
| | | | `404` | `"Usuario no encontrado"` |
| `DELETE` | `/api/v/usuarios/{id}/suave` | Eliminar usuario (soft delete) | `200` | `"Usuario eliminado suavemente exitosamente"` |
| | | | `404` | `"Usuario no encontrado"` |
| `DELETE` | `/api/v/usuarios/{id}` | Eliminar usuario permanentemente | `200` | `"Usuario eliminado exitosamente"` |
| | | | `404` | `"Usuario no encontrado"` |

### Roles

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/roles` | Crear un nuevo rol | `201` | Objeto rol creado en JSON |
| `GET` | `/api/v/roles` | Listar todos los roles | `200` | Lista de roles en JSON |
| `GET` | `/api/v/roles/{id}` | Obtener rol por ID | `200` | Objeto rol en JSON |
| | | | `404` | `"Rol no encontrado"` |
| `PUT` | `/api/v/roles/{id}` | Actualizar un rol | `200` | Objeto rol actualizado en JSON |
| | | | `404` | `"Rol no encontrado"` |
| `DELETE` | `/api/v/roles/{id}` | Eliminar un rol | `204` | Sin contenido |
| | | | `404` | `"Rol no encontrado"` |

### Estados

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/estados` | Crear un nuevo estado | `201` | Objeto estado creado en JSON |
| `GET` | `/api/v/estados` | Listar todos los estados | `200` | Lista de estados en JSON |
| `GET` | `/api/v/estados/tipo` | Listar estados por tipo | `200` | Lista de estados filtrados en JSON |
| `GET` | `/api/v/estados/{id}` | Obtener estado por ID | `200` | Objeto estado en JSON |
| | | | `404` | `"Estado no encontrado"` |
| `PUT` | `/api/v/estados/{id}` | Actualizar un estado | `200` | Objeto estado actualizado en JSON |
| | | | `404` | `"Estado no encontrado"` |
| `DELETE` | `/api/v/estados/{id}` | Eliminar un estado | `204` | Sin contenido |
| | | | `404` | `"Estado no encontrado"` |

### Tipos de Documento

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/api/v/tipos-documento` | Crear un nuevo tipo de documento | `201` | Objeto tipo de documento creado en JSON |
| `GET` | `/api/v/tipos-documento` | Listar todos los tipos de documento | `200` | Lista de tipos de documento en JSON |
| `GET` | `/api/v/tipos-documento/{id}` | Obtener tipo de documento por ID | `200` | Objeto tipo de documento en JSON |
| | | | `404` | `"Tipo de documento no encontrado"` |
| `PUT` | `/api/v/tipos-documento/{id}` | Actualizar un tipo de documento | `200` | Objeto tipo de documento actualizado en JSON |
| | | | `404` | `"Tipo de documento no encontrado"` |
| `DELETE` | `/api/v/tipos-documento/{id}` | Eliminar un tipo de documento | `204` | Sin contenido |
| | | | `404` | `"Tipo de documento no encontrado"` |

### Auditorías

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `GET` | `/api/v/auditorias` | Listar registros de auditoría | `200` | Lista de auditorías en JSON |
| `GET` | `/api/v/auditorias/{id}` | Obtener registro de auditoría por ID | `200` | Objeto auditoría en JSON |

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
