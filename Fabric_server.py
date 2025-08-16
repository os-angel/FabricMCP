import requests
import os
import json
from fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Any, Dict

load_dotenv(override=True)

# Constructor for auth
class FabricApi:
    def __init__(self):
        self.tenant_id = os.getenv("TENANT_ID")
        self.client_id = os.getenv("CLIENT_ID5")
        self.client_secret = os.getenv("CLIENT_SECRET5")

        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise ValueError(f"Faltan las variables de entorno para autenticación")
        
        self.base_url = f"https://api.powerbi.com/v1.0/myorg/admin/"
        self.token = self.get_token()

    def get_token(self):
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {
            'grant_type':'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://analysis.windows.net/powerbi/api/.default'
        }
        response = requests.post(token_url, data=data, timeout=30)
        response.raise_for_status()
        return f"Bearer {response.json()['access_token']}"
    
    def make_request(self, method:str, endpoint:str, data=None):
        header = {
            'Authorization': self.token,
            'Content-Type':"application/json"
        }

        url = f"{self.base_url}{endpoint}"
        if method.upper() == 'GET':
            response = requests.get(url, headers=header, timeout=30)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=header, data = json.dumps(data) if data else None, timeout=30)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=header, timeout=30)
        elif method.upper() == 'PATCH':
            response = requests.patch(url, headers=header, data = json.dumps(data) if data else None, timeout=30)
        else:
            raise ValueError(f"Método no soportado {method}")
        
        response.raise_for_status()

        if response.status_code == 204:
            return {}
        
        try:
            return response.json()
        except:
            return {'status':"success"}

# Terminamos el contructor y lo instanciamos
fabricApi = FabricApi()
mcp = FastMCP("fabric-server2")

@mcp.tool()
def list_workspaces() -> Dict[str,Any]:
        """
        Devuelve la lista de servers dentro del tenant
        """

        try:
            result = fabricApi.make_request('GET', 'groups?$top=500')
            workspaces = result.get("value",[])

            if not workspaces:
                return "No hay workspaces en Fabric"
            return workspaces
        except Exception as e:
            return f"Error: {str(e)}"

@mcp.tool()
def list_datasets()->Dict[str, Any]:
    "Devuelve la lista de reportes dentro de power bi"

    try:
        result = fabricApi.make_request('GET', "datasets")
        datasets = result.get("value",[])

        if not datasets:
            return "No hay datasets en Fabric"
        return datasets
    except Exception as e:
        return f"Error: {str(e)}"
    
@mcp.tool()
def list_reports()->Dict[str, Any]:
    "Devuelve una lista de reportes publicados en Fabric"

    try:
        result = fabricApi.make_request('GET', "reports")
        reports = result.get("value", [])

        if not reports:
            return "No tienes reportes publicados en Fabric, Power BI"
        return reports
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_workspace_users(workspace_id:str)-> Dict[str, Any]:
    "Devuelve los usuarios con acceso a determinado workspace con información sobre el rol y correo"

    try:
        result = fabricApi.make_request('GET', f"groups/{workspace_id}/users")
        users = result.get("value", [])

        if not users:
            return "Este workspace no tiene usuarios asignados"
        return users
    except Exception as e:
        return f"Error del tipo {str(e)}"

@mcp.tool()
def create_workspace(name:str)->str:
    "Crea un nuevo workspace dándole solamente el nombre del mismo"
    try:
        data = {'name':name}
        result = fabricApi.make_request('POST', "groups",data = data)
        return f"Workspace creado con nombre {name} y ID: {result.get('id',[])}"
    except Exception as e:
        return f"Error al crear el workspace {str(e)}"
    
    
@mcp.tool()
def execute_dax_query(workspace_id:str, dataset_id:str, dax_query:str)->str:
    "Ejecuta una consulta dax en un dataset"

    try:
        data = {"queries":[{"query":dax_query}]}
        result = fabricApi.make_request('POST', f"groups/{workspace_id}/datasets/{dataset_id}/executeQueries", data=data)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error al ejecutar el DAX {str(e)}"

@mcp.tool()
def add_user_to_workspace(workspace_id:str, user_email:str, access_right:str="Viewer")->str:
    "Agrega un usuario a un workspace específico"
    try:
        data = {
            'identifier':user_email,
            'principalType': 'User',
            'groupUserAccessRight':access_right
        }
        fabricApi.make_request('POST', f"groups/{workspace_id}/users", data = data)
        return f"Usuario {user_email} agregado con rol {access_right} al workspace {workspace_id}"
    except Exception as e:
        return f"Error al agregar el usuario {str(e)}"

@mcp.tool()
def remove_user_from_workspace(workspace_id:str, user_email:str)->str:
    "Elimina a un usuario específico de un workspace"

    try:
        fabricApi.make_request('DELETE', f"groups/{workspace_id}/users/{user_email}")
        return f"Usuario {user_email} removido del workspace {workspace_id}"
    except Exception as e:
        return f"Error {str(e)}"
    

if __name__ == "__main__":
    mcp.run()
