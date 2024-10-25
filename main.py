from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from swarm import Swarm
from agents import triage_agent

app = FastAPI()

# Inicializar el cliente Swarm
client = Swarm()

# Definir un modelo de datos usando Pydantic para recibir el prompt y el historial de mensajes
class Message(BaseModel):
    role: str
    content: str

class PromptWithHistory(BaseModel):
    prompt: str
    messages: List[Message]  # Lista de mensajes previos
    context_variables: dict = None  # Opcional: puedes agregar más contexto

# Ruta POST que recibe el prompt y genera una respuesta del agente
@app.post("/agente")
def create_response(data: PromptWithHistory):
    try:
        # Crear el mensaje actual basado en el nuevo prompt
        new_message = {"role": "user", "content": data.prompt}
        
        # Convertir los mensajes previos a diccionarios
        messages = [msg.dict() for msg in data.messages]
        messages.append(new_message)  # Agregar el nuevo mensaje

        # Incluir explícitamente el contexto del usuario en el mensaje inicial
        if data.context_variables and "user_context" in data.context_variables:
            messages.insert(0, {"role": "system", "content": data.context_variables["user_context"]})
        
        # Ejecutar el agente con el cliente Swarm y pasar los mensajes y variables de contexto
        response = client.run(
            agent=triage_agent,
            messages=messages,
            context_variables=data.context_variables or {}
        )
        
        # Verificar si la respuesta contiene mensajes
        if not response.messages:
            return {"error": "No response messages found from the agent."}
        
        # Retornar la última respuesta generada por el agente
        return {"response": response.messages[-1]["content"]}
    
    except Exception as e:
        # Capturar cualquier error y devolver un mensaje detallado
        return {"error": str(e)}

