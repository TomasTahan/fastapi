import openai
import requests
from settings import OPENAI_API_KEY, SUPABASE_API_KEY

openai.api_key = OPENAI_API_KEY

def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def store_data_in_supabase(categoria, context_variables):
    print("Storing data in Supabase...", "categoryId:", categoria)
    userId = context_variables.get("userId", None)
    user_input = context_variables.get("user_input", None)
    descripcion = context_variables.get("descripcion", None)

    url = "https://xttiyjbpfzextsjmlwad.supabase.co/rest/v1/rpc/guardar_informacion"
    
    headers = {
        "Content-Type": "application/json",
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
    }

    # Obtener el embedding del input del usuario
    embedding = get_embedding(user_input)
    
    # Estructura de los datos que quieres almacenar
    data = {
        "p_userid": userId,
        "p_descripcion": descripcion,
        "p_categoria_nombre": categoria,
        "p_embedding": embedding,
        "p_user_input": user_input
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        # Mostrar la respuesta completa de Supabase
        print("Response:", result)

        # Verificar si Supabase retornó 'status': true
        if result.get("status") == True:
            return {"status": True, "mensaje": "Información guardada con éxito"}
        else:
            error_message = result.get("error", "Error desconocido")
            print("Error al guardar la información:", error_message)
            return {"status": False, "mensaje": f"Error al guardar la información: {error_message}"}

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Supabase: {str(e)}")
        return {"status": False, "mensaje": f"Error al conectar con Supabase: {str(e)}"}

