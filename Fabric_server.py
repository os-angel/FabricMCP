import requests
import os
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

class FabricApi:
    def __init__(self):
        self.tenant_id = os.getenv('TENANT_ID')
        self.client_id = os.getenv('CLIENT_ID5')
        self.client_secret = os.getenv('CLIENT_SECRET5')
        
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise ValueError("Faltan variables de entorno: TENANT_ID, CLIENT_ID5, CLIENT_SECRET5")
        
        self.base_url = "https://api.powerbi.com/v1.0/myorg/admin/"
        
    def get_token(self):
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://analysis.windows.net/powerbi/api/.default'
        }
        
        response = requests.post(token_url, data=data, timeout=30)
        response.raise_for_status()
        return f"Bearer {response.json()['access_token']}"
    
    def make_request(self, endpoint):
        headers = {
            "Authorization": self.get_token(),
            "Content-Type": "application/json"
        }
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

mcp = FastMCP("powerbi-server")
fabric_api = FabricApi()

@mcp.tool()
def list_workspaces() -> str:
    """Lista los workspaces disponibles en Power BI/Fabric"""
    try:
        result = fabric_api.make_request(f"{fabric_api.base_url}groups/?$top=100")
        workspaces = result.get("value", [])
        
        if not workspaces:
            return "No se encontraron workspaces"
        
        output = f"Workspaces encontrados: {len(workspaces)}\n"
        for ws in workspaces:
            output += f"• {ws.get('name', 'Sin nombre')} - ID: {ws.get('id', 'Sin ID')}\n"
        
        return output
        
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_datasets() -> str:
    """Lista los datasets disponibles dentro del tenant"""
    try:
        result = fabric_api.make_request(f"{fabric_api.base_url}datasets")
        datasets = result.get('value', [])

        if not datasets:
            return "No se encontraron datasets creados en el tentant"
        
        output = datasets
        return output
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()