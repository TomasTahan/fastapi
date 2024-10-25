from utils import get_embedding, store_data_in_supabase
from settings import SUPABASE_API_KEY
import requests

####### Agente Principal #######

def transfer_to_ask_agent():
    from agents import ask_agent
    print("Se ha transferido al ask_agent.")
    return ask_agent

def transfer_to_store_agent():
    from agents import store_agent
    print("Se ha transferido al store_agent.")
    return store_agent

####### Agentes Secundarios #######

def transfer_to_triage():
    from agents import triage_agent
    print("Se ha transferido al trige_agent.")
    return triage_agent

## Store Agent ##

def transfer_Finanzas():
    from agents import finanzas_agent
    print("Se ha transferido al finanzas_agent.")
    return finanzas_agent

def transfer_Salud():
    from agents import salud_agent
    print("Se ha transferido al salud_agen.")
    return salud_agent

def transfer_Mantenimiento():
    from agents import mantenimiento_agent
    print("Se ha transferido al mantenimiento_agent.")
    return mantenimiento_agent

def transfer_General():
    from agents import general_agent
    print("Se ha transferido al general_agent.")
    return general_agent

def set_description(descripcion, context_variables):
    print("Guardando descripción en context_variables...", "descripcion:", descripcion)
    context_variables["descripcion"] = descripcion
    return "Descripción almacenada en context_variables. Puedes continuar."


## Ask Agent ##

def search_information(context_variables):
    print("Buscando información en la base de datos...")
    user_input = context_variables.get("user_input", None)
    embedding = get_embedding(user_input)
    userId = context_variables.get("userId", None)

    url = "https://xttiyjbpfzextsjmlwad.supabase.co/rest/v1/rpc/match_informacion"
    
    headers = {
        "Content-Type": "application/json",
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
    }

    data = {
        "user_id": userId,
        "query_embedding": embedding,
        "match_count": 5,  # Máximo de coincidencias
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print("Response:", response.json())

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "message": "Error inesperado en la consulta."}

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}



####### Agentes Terciarios #######

def store_data(categoria, context_variables):
    print("categoria:", categoria)
    return store_data_in_supabase(categoria, context_variables)



##############

def search_category(context_variables):
    userId = context_variables.get("userId", None)
    print("Buscando categorías en la base de datos...", "userId: ",userId)
    url = f"https://xttiyjbpfzextsjmlwad.supabase.co/rest/v1/Categorias?userId=eq.{userId}&select=*"

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
    }

    response = requests.get(url, headers=headers)
    categories = response.json()

    # Verificamos si la respuesta es una lista vacía
    if isinstance(categories, list) and len(categories) == 0:
        return {"success": True, "message": "Sin categorías, crea una nueva llamando a create_category"}

    formatted_categories = [
        {
            "categoriaId": category["categoriaId"],
            "nombre": category["nombre"],
            "descripcion": category["descripcion"]
        }
        for category in categories
    ]

    print("Categorías encontradas:", formatted_categories)

    return {"success": True, "data": formatted_categories}

def create_category(context_variables, nombre, descripcion):
    userId = context_variables.get("userId", None)
    print(nombre, descripcion)
    
    url = "https://xttiyjbpfzextsjmlwad.supabase.co/rest/v1/Categorias"
    
    headers = {
        "Content-Type": "application/json",
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh0dGl5amJwZnpleHRzam1sd2FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk0NDc2MzIsImV4cCI6MjA0NTAyMzYzMn0.0NVWF2HYldKUNss15bUys4JoOyPOPtIERfqX98ptiiE",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh0dGl5amJwZnpleHRzam1sd2FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk0NDc2MzIsImV4cCI6MjA0NTAyMzYzMn0.0NVWF2HYldKUNss15bUys4JoOyPOPtIERfqX98ptiiE",
        "Prefer": "return=representation"
    }

    data = {
        "userId": userId,
        "nombre": nombre,
        "descripcion": descripcion
    }

    # Hacer la solicitud POST
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Verificar si la solicitud fue exitosa

    # Obtener la respuesta JSON
    response_data = response.json()

    # Asegurarnos de que haya al menos un resultado en la respuesta
    if isinstance(response_data, list) and len(response_data) > 0:
        # Extraer el `categoriaId` del primer objeto
        categoria_id = response_data[0].get("categoriaId")
        return {"success": True, "data": f"Categoría creada exitosamente. categoriaId: {categoria_id}"}
    else:
        return {"success": False, "message": "No se pudo crear la categoría."}
    


