# Documentación de Endpoints API - BibliTech

API RESTful para la gestión de préstamo de libros.

**Prefijo de API:** `/api/v`

---

## Módulo 1 - Gestión de Préstamos

### Préstamos

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/prestamos` | Crear un nuevo préstamo | `201` | `"Préstamo creado exitosamente con el ejemplar {codigo_interno}."` |
| | | Error: No hay ejemplares disponibles | `400` | `"No hay ejemplares disponibles para el libro solicitado."` |
| `GET` | `/prestamos` | Listar todos los préstamos (bibliotecario) | `200` | Lista de préstamos |
| `GET` | `/prestamos/lector` | Listar préstamos del lector actual | `200` | Lista de préstamos del usuario |
| `POST` | `/prestamos/confirmar-entrega` | Confirmar la entrega de un préstamo | `200` | `"Entrega confirmada. El ejemplar fue marcado como prestado."` |
| | | Error: Préstamo no encontrado | `200` | `"No existe un préstamo reservado para este usuario y ejemplar."` |
| `POST` | `/prestamos/{codigo_interno}/confirmar-devolucion` | Registrar la devolución de un préstamo | `200` | `"Devolución registrada correctamente."` |
| | | Error: Préstamo no encontrado | `200` | `"No existe un préstamo activo para este ejemplar."` |

### Ejemplares

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/ejemplares` | Crear un nuevo ejemplar | `201` | Objeto EjemplarView |
| `GET` | `/ejemplares` | Listar todos los ejemplares | `200` | Lista de ejemplares |
| `GET` | `/ejemplares/codigo/{codigo_interno}` | Obtener ejemplar por código interno | `200` | Objeto EjemplarReaderNormalized |
| | | Error: No encontrado | `404` | `"Ejemplar no encontrado"` |
| `GET` | `/ejemplares/{id}` | Obtener ejemplar por ID | `200` | Objeto EjemplarView o EjemplarReaderNormalized |
| | | Error: No encontrado | `404` | `"Ejemplar no encontrado"` |
| `PUT` | `/ejemplares/{id}` | Actualizar un ejemplar | `200` | Objeto EjemplarView |
| | | Error: No encontrado | `404` | `"Ejemplar no encontrado"` |
| `PATCH` | `/ejemplares/{id}/estado` | Actualizar estado de un ejemplar | `200` | `"Estado del ejemplar actualizado correctamente"` |
| | | Estado ya asignado | `200` | `"El ejemplar ya tiene el estado especificado"` |
| | | Error: Estado inválido | `400` | `"El estado no es válido para actualizar el ejemplar"` |
| | | Error: No encontrado | `404` | `"Ejemplar no encontrado"` |
| `DELETE` | `/ejemplares/{id}` | Eliminar un ejemplar | `200` | `"Ejemplar eliminado correctamente"` |
| | | Error: No encontrado | `404` | `"Ejemplar no encontrado"` |

---

## Módulo 2 - Gestión de Libros y Autores

### Libros

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/libros` | Crear un nuevo libro | `201` | Objeto LibroView |
| | | Error: Datos inválidos | `400` | `"Error al procesar los datos del libro: {error}"` |
| | | Error: Autores no encontrados | `400` | `"Autores no encontrados: {ids}"` |
| | | Error: Imagen muy grande | `400` | Mensaje de validación de tamaño |
| | | Error: Imagen inválida | `400` | Mensaje de validación de imagen |
| | | Error: Subida a S3 | `500` | `"Error al subir la imagen a S3: {error}"` |
| `GET` | `/libros` | Listar todos los libros | `200` | Lista de libros |
| `GET` | `/libros/{id}` | Obtener libro por ID | `200` | Objeto LibroView o LibroViewNormalized |
| | | Error: No encontrado | `404` | `"Libro no encontrado"` |
| `PUT` | `/libros/{id}` | Actualizar un libro | `200` | Objeto LibroView |
| | | Error: No encontrado | `404` | `"Libro no encontrado"` |
| | | Error: Autores no encontrados | `400` | `"Autores no encontrados: {ids}"` |
| `PATCH` | `/libros/{id}/imagen` | Actualizar imagen de un libro | `200` | Objeto LibroURLUpdate |
| | | Error: Imagen muy grande | `400` | Mensaje de validación de tamaño |
| | | Error: Imagen inválida | `400` | Mensaje de validación de imagen |
| | | Error: No encontrado | `404` | `"Libro no encontrado"` |
| | | Error: Subida a S3 | `500` | `"Error al subir la imagen a S3: {error}"` |
| `DELETE` | `/libros/{id}` | Eliminar un libro | `200` | `"Libro eliminado exitosamente"` |
| | | Error: No encontrado | `404` | `"Libro no encontrado"` |

### Autores

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/autores` | Crear un nuevo autor | `201` | Objeto AutorView |
| `GET` | `/autores` | Listar todos los autores | `200` | Lista de autores |
| `GET` | `/autores/{id}` | Obtener autor por ID | `200` | Objeto AutorView |
| | | Error: No encontrado | `404` | `"Autor no encontrado"` |
| `PUT` | `/autores/{id}` | Actualizar un autor | `200` | Objeto AutorView |
| | | Error: No encontrado | `404` | `"Autor no encontrado"` |
| `DELETE` | `/autores/{id}` | Eliminar un autor | `200` | `"Autor eliminado con éxito"` |
| | | Error: No encontrado | `404` | `"Autor no encontrado"` |

### Categorías

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/categorias` | Crear una nueva categoría | `201` | Objeto CategoriaView |
| `GET` | `/categorias` | Listar todas las categorías | `200` | Lista de categorías |
| `GET` | `/categorias/{id}` | Obtener categoría por ID | `200` | Objeto CategoriaView |
| | | Error: No encontrado | `404` | `"Categoría no encontrada"` |
| `PUT` | `/categorias/{id}` | Actualizar una categoría | `200` | Objeto CategoriaView |
| | | Error: No encontrado | `404` | `"Categoría no encontrada"` |
| `DELETE` | `/categorias/{id}` | Eliminar una categoría | `200` | `"Categoría eliminada exitosamente"` |
| | | Error: No encontrado | `404` | `"Categoría no encontrada"` |

---

## Módulo 3 - Gestión de Usuarios y Roles

### Autenticación

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/auth/registro` | Registrar un nuevo usuario | `201` | Objeto UsuarioReadNormalized |
| `POST` | `/auth/inicio-sesion` | Iniciar sesión | `200` | Objeto Token (access_token, refresh_token, token_type) |
| | | Error: Credenciales inválidas | `401` | `"Credenciales inválidas"` |
| `GET` | `/auth/yo` | Obtener usuario actual | `200` | Objeto UsuarioReadNormalized |

### Usuarios

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/usuarios` | Crear un nuevo usuario (admin) | `201` | Objeto UsuarioReadNormalized |
| `GET` | `/usuarios` | Listar todos los usuarios | `200` | Lista de usuarios |
| `GET` | `/usuarios/{id}` | Obtener usuario por ID | `200` | Objeto UsuarioView o UsuarioReadNormalized |
| | | Error: No encontrado | `404` | `"Usuario no encontrado"` |
| `GET` | `/usuarios/{documento}/prestamo` | Obtener usuario por documento | `200` | Objeto UsuarioViewPrestamoNormalizado |
| | | Error: No encontrado | `200` | `null` |
| `PUT` | `/usuarios/{id}/perfil` | Actualizar perfil de usuario | `200` | Objeto UsuarioReadNormalized |
| | | Error: No encontrado | `404` | `"Usuario no encontrado"` |
| `PUT` | `/usuarios/{id}/admin` | Actualizar usuario por admin | `200` | Objeto UsuarioReadNormalized |
| | | Error: No encontrado | `404` | `"Usuario no encontrado"` |
| `PUT` | `/usuarios/{id}/contrasena` | Actualizar contraseña | `200` | `"Contraseña actualizada exitosamente"` |
| | | Error: No encontrado | `404` | `"Usuario no encontrado"` |
| | | Error: Contraseña incorrecta | `400` | `"Contraseña actual incorrecta"` |
| `POST` | `/usuarios/resetear-contrasena` | Solicitar restablecimiento de contraseña | `200` | `"Correo de restablecimiento enviado"` |
| | | Error: No encontrado | `404` | `"Usuario no encontrado"` |
| `POST` | `/usuarios/verificar-token` | Verificar token y restablecer contraseña | `200` | `"Contraseña restablecida exitosamente"` |
| | | Error: No encontrado | `404` | `"Usuario no encontrado"` |
| | | Error: Token inválido | `400` | `"Token inválido"` |
| | | Error: Token expirado | `400` | `"Token expirado"` |
| `DELETE` | `/usuarios/{id}/suave` | Eliminar usuario (soft delete) | `200` | `"Usuario eliminado suavemente exitosamente"` |
| | | Error: No encontrado | `404` | `"Usuario no encontrado"` |
| `DELETE` | `/usuarios/{id}` | Eliminar usuario permanentemente | `204` | Sin contenido |
| | | Error: No encontrado | `404` | `"Usuario no encontrado"` |

### Roles

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/roles` | Crear un nuevo rol | `201` | Objeto RolView |
| `GET` | `/roles` | Listar todos los roles | `200` | Lista de roles |
| `GET` | `/roles/{id}` | Obtener rol por ID | `200` | Objeto RolView |
| | | Error: No encontrado | `404` | `"Rol no encontrado"` |
| `PUT` | `/roles/{id}` | Actualizar un rol | `200` | Objeto RolView |
| | | Error: No encontrado | `404` | `"Rol no encontrado"` |
| `DELETE` | `/roles/{id}` | Eliminar un rol | `204` | Sin contenido |
| | | Error: No encontrado | `404` | `"Rol no encontrado"` |

### Estados

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/estados` | Crear un nuevo estado | `201` | Objeto EstadoView |
| `GET` | `/estados` | Listar todos los estados | `200` | Lista de estados |
| `GET` | `/estados/tipo` | Listar estados por tipo | `200` | Lista de estados filtrados |
| `GET` | `/estados/{id}` | Obtener estado por ID | `200` | Objeto EstadoView |
| | | Error: No encontrado | `404` | `"Estado no encontrado"` |
| `PUT` | `/estados/{id}` | Actualizar un estado | `200` | Objeto EstadoView |
| | | Error: No encontrado | `404` | `"Estado no encontrado"` |
| `DELETE` | `/estados/{id}` | Eliminar un estado | `204` | Sin contenido |
| | | Error: No encontrado | `404` | `"Estado no encontrado"` |

### Tipos de Documento

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `POST` | `/tipos-documento` | Crear un nuevo tipo de documento | `201` | Objeto TipoDocumentoView |
| `GET` | `/tipos-documento` | Listar todos los tipos de documento | `200` | Lista de tipos de documento |
| `GET` | `/tipos-documento/{id}` | Obtener tipo de documento por ID | `200` | Objeto TipoDocumentoView |
| | | Error: No encontrado | `404` | `"Tipo de documento no encontrado"` |
| `PUT` | `/tipos-documento/{id}` | Actualizar un tipo de documento | `200` | Objeto TipoDocumentoView |
| | | Error: No encontrado | `404` | `"Tipo de documento no encontrado"` |
| `DELETE` | `/tipos-documento/{id}` | Eliminar un tipo de documento | `204` | Sin contenido |
| | | Error: No encontrado | `404` | `"Tipo de documento no encontrado"` |

### Auditorías

| Método | Endpoint | Descripción | Código | Mensaje de Respuesta |
|--------|----------|-------------|--------|----------------------|
| `GET` | `/auditorias` | Listar registros de auditoría | `200` | Lista de registros de auditoría |
| | | Error: Parámetros de paginación incompletos | `400` | `"Los parámetros 'page' y 'page_size' deben proporcionarse juntos o no usarse"` |
| `GET` | `/auditorias/{id}` | Obtener registro de auditoría por ID | `200` | Objeto AuditoriaView |

---

## Parámetros de Paginación

Los endpoints que soportan paginación aceptan los siguientes parámetros de consulta:

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `page` | `int` | Número de página (mínimo: 1) |
| `page_size` | `int` | Número de items por página (mínimo: 1, máximo: 100) |
| `normalizado` | `bool` | Retornar datos en formato normalizado (cuando está disponible) |

---

## Códigos de Error Comunes

| Código | Descripción |
|--------|-------------|
| `400` | Bad Request - Datos inválidos o solicitud malformada |
| `401` | Unauthorized - No autenticado o token inválido |
| `403` | Forbidden - Sin permisos para realizar la acción |
| `404` | Not Found - Recurso no encontrado |
| `500` | Internal Server Error - Error del servidor |

---

## Autenticación

La API utiliza autenticación JWT (JSON Web Token). Para acceder a endpoints protegidos:

1. Obtener token mediante `POST /auth/inicio-sesion`
2. Incluir el token en el header de las solicitudes:
   ```
   Authorization: Bearer {access_token}
   ```

### Roles y Permisos

- **Administrador**: Acceso completo a todos los endpoints
- **Bibliotecario**: Gestión de préstamos, libros, autores, categorías y ejemplares
- **Lector**: Acceso a sus propios préstamos y consulta de libros
