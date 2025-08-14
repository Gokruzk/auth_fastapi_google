from fastapi import status

APP_MESSAGES = {
    "get_users_error": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "Ocurrió un error obteniendo los datos",
    },
    "no_users_found": {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": "No hay usuarios registrados",
    },
    "no_users_online": {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": "No hay usuarios conectados",
    },
    "no_coachs_online": {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": "No hay entrenadores conectados",
    },
    "get_memberships_error": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "Ocurrió un error obteniendo las membresías",
    },
    "no_memberships_found": {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": "No hay membresías registradas",
    },
    "unexpected_error": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "Ocurrió un error inesperado",
    },
    "user_not_found": {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": "El usuario no existe",
    },
    "username_exists": {
        "status_code": status.HTTP_409_CONFLICT,
        "detail": "El nombre de usuario ya existe",
    },
    "dni_exists": {
        "status_code": status.HTTP_409_CONFLICT,
        "detail": "Ya existe una cuenta con la misma cédula",
    },
    "email_exists": {
        "status_code": status.HTTP_409_CONFLICT,
        "detail": "El correo ya existe",
    },
    "incorrect_email_psw": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Correo o contraseña incorrecta",
    },
    "user_data_inconsistent": {
        "status_code": status.HTTP_409_CONFLICT,
        "detail": "Los datos del usuario son inconsistentes",
    },
    "token_expired": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Su sesión ha expirado",
    },
    "invalid_token": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Token inválido",
    },
    "invalid_credentials": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Credenciales inválidas",
    },
    "could_not_valid_credentials": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "No se pudieron validar las credenciales",
    },
    "need_auth": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "No autenticado",
    },
    "need_memb": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Su membresía no está activa, contáctese con el administrador",
    },
    "invalid_dni": {
        "status_code": status.HTTP_406_NOT_ACCEPTABLE,
        "detail": "La cédula ingresada no es válida",
    },
    "update_psw_fail": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "Ocurrió un error actualizando la contraseña",
    },
    "invalid_psw": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Las contraseña actual es incorrecta",
    },
    "account_disabled": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Su cuenta está inactiva, comúniquese con el administrador",
    },
    "condition_created": {
        "status_code": status.HTTP_201_CREATED,
        "detail": "La condición médica fue registrada",
    },
    "successfully_retrieved": {
        "status_code": status.HTTP_200_OK,
        "detail": "Datos obtenidos exitosamente",
    },
    "successfully_created": {
        "status_code": status.HTTP_201_CREATED,
        "detail": "Usuario registrado exitosamente",
    },
    "successfully_created_coach": {
        "status_code": status.HTTP_201_CREATED,
        "detail": "Entrenador registrado exitosamente",
    },
    "successfully_updated": {
        "status_code": status.HTTP_200_OK,
        "detail": "Usuario actualizado exitosamente",
    },
    "successfully_updated_coach": {
        "status_code": status.HTTP_200_OK,
        "detail": "Entrenador actualizado exitosamente",
    },
    "successfully_deleted": {
        "status_code": status.HTTP_200_OK,
        "detail": "Se eliminó correctamente",
    },
    "successfully_memb_assigned": {
        "status_code": status.HTTP_200_OK,
        "detail": "Membresía asignada exitosamente",
    },
    "successfully_updated_psw": {
        "status_code": status.HTTP_200_OK,
        "detail": "La contraseña se actualizó correctamente",
    },
    "client_not_found": {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": "Cliente no encontrado",
    },
    "not_a_client": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "El usuario no es un cliente",
    },
    # Mensajes de autenticación y autorización
    "unauthorized": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "No autorizado",
    },
    "forbidden": {
        "status_code": status.HTTP_403_FORBIDDEN,
        "detail": "Acceso denegado",
    },
    "invalid_token": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Token inválido",
    },
    "token_expired": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Token expirado",
    },
    "invalid_role": {
        "status_code": status.HTTP_403_FORBIDDEN,
        "detail": "No es un usuario válido del sistema",
    },
    "admin_required": {
        "status_code": status.HTTP_403_FORBIDDEN,
        "detail": "Se requieren permisos de administrador",
    },
}
