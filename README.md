# Microsoft Fabric MCP Server

An MCP (Model Context Protocol) server that lets you manage Microsoft Fabric/Power BI through natural language commands with Claude.

## Features

- List workspaces
- List datasets  
- Create datasets
- Create workspaces
- Manage user access
- Refresh datasets

## Prerequisites

- Python 3.8+
- Microsoft Azure account with Power BI/Fabric access
- Azure AD application registered with Power BI API permissions

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <your-repo>
   cd MCP_Git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

4. **Azure AD Setup**
   - Go to Azure Portal → Azure Active Directory → App registrations
   - Create a new application or use an existing one
   - Under "Certificates & secrets", create a new client secret
   - Under "API permissions", add the necessary Power BI API permissions
   - Fill in the variables in your .env file

## Usage

1. **Run the MCP server**
   ```bash
   python Fabric_server.py
   ```

2. **Connect with Claude**
   - Configure Claude to use this MCP server
   - Now you can ask things like:
     - "What workspaces do I have?"
     - "Refresh the sales dataset"
     - "Add user@company.com to the marketing workspace"

## Project Structure

```
MCP_Git/
├── Fabric_server.py           # Main MCP server
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── tutorial_fabric_server.md # Complete tutorial (optional)
└── README.md                 # This file
```

## Environment Variables

```bash
TENANT_ID=your-tenant-id-here
CLIENT_ID5=your-client-id-here  
CLIENT_SECRET5=your-client-secret-here
```

## Complete Tutorial

For a detailed implementation guide and real-world use cases, check out the `tutorial_fabric_server.md` file.

## Contributing

Contributions are welcome! If you find bugs or have ideas for improvements:

1. Open an issue to discuss the change
2. Fork the repository
3. Create a branch for your feature
4. Submit a pull request

## License

This project is under the MIT License. See the LICENSE file for details.

## Important Notes

- Never commit your `.env` file with real credentials to the repository
- Keep your Azure credentials secure
- This code is for educational and demonstration purposes
