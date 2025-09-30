import requests

BASE_URL = "http://127.0.0.1:5000"

def validar_contrasena_usuario(token, datos=None):
    url = f"{BASE_URL}/api/validar_contrasena_usuario"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.post(url, headers=headers, json=datos if datos else {})
        try:
            return response.json()
        except Exception:
            return {"success": False, "message": f"Respuesta no válida del servidor: {response.text}"}
    except Exception as e:
        return {"success": False, "message": f"Error de conexión: {e}"}
