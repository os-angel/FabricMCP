# From YouTube Video to MCP Server: Automating Microsoft Fabric Administration

A few days ago, I was browsing YouTube when I stumbled across a video about Model Context Protocol (MCP). I watched it out of curiosity, thinking it would just be another tech experiment... but 10 minutes in, I was already taking notes.

The concept hooked me: an MCP is like having an assistant that not only understands what you're saying, but can actually act on your tools — from databases to dashboards and APIs.

That's when I thought: "What if I applied this to Microsoft Fabric for admin tasks?"

Spoiler: it worked.

## Not just administration: MCP as your data analyst

While my first experiment was creating functions to manage workspaces and datasets in Fabric, I quickly saw the possibilities went way beyond that:

- Generate reports without opening the interface
- Query metrics like you're asking a real analyst
- Even build a "personal data scientist" that understands your context and data

But let's go step by step...

## What I built with my Fabric MCP server

Inspired by that video, I created a Python server (`Fabric_server.py`) that takes natural language instructions and translates them into Fabric API calls.

This first version includes functions for:

✅ List all workspaces  
✅ List all datasets  
✅ Create datasets  
✅ Create workspaces  
✅ Grant user access  
✅ Refresh datasets

## MCP: The Perfect Bridge Between Your AI Assistant and Your Fabric Data

To better understand what we're building, imagine you have a personal assistant who speaks your language, but also knows how to communicate perfectly with all your systems: Power BI, databases, APIs, whatever. That's basically what an MCP server does. Technically, an MCP is a standardized interface that allows tools like Claude to connect directly with your external systems, but what's interesting isn't the academic definition — it's what you can do with it.

### The Flow in Action
```
You: "Update the Q2 sales dataset"
     ↓
MCP Server: Translates your request
     ↓
Fabric API: Executes the action
     ↓
MCP: ✅ Dataset refreshed successfully in 3.2 seconds
```

## My first test: asking it to list my workspaces

After setting up the server, the first thing I did was connect Claude and ask for something simple: "What workspaces do I have in Fabric?". Seeing how it translated that casual question into a perfect API call and returned an ordered list of all my workspaces confirmed I was on the right track. No more navigating through menus, no more trying to remember where I put that workspace from last week's project, no more frustrations with slow web interfaces.

But it didn't stop there. Once I verified the basic communication worked, I started asking for more complex tasks: refresh specific datasets, add users to workspaces, execute DAX queries against my semantic models. Every time I asked for something new, the server translated my natural language request into the precise API calls that Fabric needed.

## How to Set Up Your Fabric MCP Server in Minutes

Before starting, you need three basic ingredients you probably already have if you work with Azure. Azure AD credentials are the first step: your TENANT_ID, CLIENT_ID, and CLIENT_SECRET that you get when you register an application in Azure (I use CLIENT_ID5 as a personal convention to differentiate applications, but you can use whatever name you prefer). The Python dependencies are minimal: requests for HTTP calls, fastmcp for the MCP protocol, and python-dotenv to handle environment variables securely.

```bash
# Environment variables
TENANT_ID=your-tenant-id-here
CLIENT_ID5=your-client-id-here  
CLIENT_SECRET5=your-client-secret-here

# Quick installation
pip install requests fastmcp python-dotenv
```

The setup is intentionally simple because after years of building tools that nobody used due to complicated setups, I learned that initial friction kills any project, no matter how good it is.

## The functions that have most changed my daily routine

Once you have the server running, these are the four functions that will really transform your day-to-day work with Fabric. They're not the only ones included in the code, but they're the ones that have most simplified my work since I implemented them.

### 1. Instant exploration: no more workspace hunting

This started from pure frustration. I had spent twenty minutes looking for a workspace called "Analytics_Q3" when I swore it was "Analytics Q3" (without the underscore). While navigating page by page in Power BI Service, I thought there had to be a better way to do this. The `list_workspaces()` function was born from that frustration and is now probably what I use most from the server. I ask Claude "what workspaces do I have?" and get a complete list with exact names and IDs, no drama. It's especially useful when you work with multiple clients where each project has its workspace and the names are similar.

```python
@mcp.tool()
def list_workspaces() -> str:
    """Lists all available workspaces."""
```

### 2. Automatic refreshes: no more "outdated data" excuses

You know that feeling when you're in an important meeting and someone points out that the dashboard numbers don't match what they see in the main system? I've lived that moment more times than I'd like to admit. Dataset refreshes have always been my Achilles heel - they're those tasks you mentally schedule but inevitably forget until it's too late. Now I simply tell Claude "refresh the sales dataset" and it handles everything, including showing me the refresh history so I can see if there have been issues. The first time I tried it, I didn't believe it had worked because I didn't see immediate changes, until I learned that refreshes run in the background and the server only confirms they started correctly.

```python
@mcp.tool()
def refresh_dataset(workspace_id: str, dataset_id: str) -> str:
    """Initiates a dataset refresh."""
```

### 3. Direct DAX queries: my new superpower for validating numbers

This functionality changed my perspective on what it means to work with Power BI. Before, when I needed a specific number, I had to open Power BI Desktop or navigate to the correct report in the service, wait for it to load (and have updated data), then find the visualization that gave me exactly what I needed. Now I ask Claude "show me total sales for August" and it executes a DAX query directly against the semantic model. The moment that most convinced me was when I was minutes away from a presentation with the CEO and needed to confirm a figure: instead of panicking looking for reports, I simply executed the query and got the exact number I needed, with confidence that it came directly from the data engine.

```python
@mcp.tool()
def execute_dax_query(workspace_id: str, dataset_id: str, dax_query: str) -> str:
    """Executes a DAX query on a dataset."""
```

### 4. User management: no more afternoons lost adding people

If you manage more than two workspaces, you know exactly what I'm talking about. User management in Power BI is one of those tasks that seems simple until you have to do the same thing for ten workspaces and five different users. I've lost entire afternoons copying emails, navigating menus, selecting permissions, confirming changes, and then discovering I forgot someone or put incorrect permissions. The moment of inspiration came when I had to set up access for a new project with six people across four different workspaces - I calculated it would take me almost an hour of manual work. Now I tell Claude "add these users to the marketing workspace with editor permissions" and it handles everything. What used to be a lost afternoon is now literally thirty seconds.

```python
@mcp.tool()
def add_user_to_workspace(workspace_id: str, user_email: str, access_right: str = "Viewer") -> str:
```

## The moments where the MCP server really shines

After a few months using the server in my daily work, there are three specific situations where the difference is dramatically noticeable. These aren't theoretical cases - they're real situations that have happened to me where the server literally saved me hours of manual work.

### 1. The urgent project that arrived Friday afternoon

It was Friday at 4 PM when my boss walked into my office with that expression that says "I have something you won't like". An important client had decided to start a data analysis project the following Monday (of course) and needed me to create a complete workspace with access for their team of five people, each with specific permissions according to their role in the project. In the past, this would have meant staying late manually configuring everything - create the workspace, look up each person's corporate emails, assign individual permissions, verify everything worked. This time I simply opened my terminal and asked Claude to handle everything. In less than a minute I had the workspace created with all users correctly configured.

```python
# Complete project setup in seconds
create_workspace("Marketing_Project_Q4")
add_user_to_workspace(workspace_id, "ana@company.com", "Admin")
add_user_to_workspace(workspace_id, "carlos@company.com", "Member")
add_user_to_workspace(workspace_id, "sofia@company.com", "Viewer")
```

### 2. The Monday when everything broke (and how I fixed it in five minutes)

Monday 8:30 AM, my first coffee of the day still steaming, when I receive a WhatsApp message from the sales director: "The sales dashboard numbers look weird, they don't match what we see in the CRM". My stomach contracted because I knew the Monday report was always critical for the weekly management meeting. Before I would have panicked opening Power BI Service, looking for the sales workspace, navigating to the correct dataset, manually reviewing the refresh history, trying to interpret error messages that seemed written in hieroglyphics. This time I asked Claude what had happened with the sales dataset. In seconds I had the complete diagnosis: the overnight refresh had failed due to a database timeout. I asked it to start a manual refresh and in five minutes the problem was solved.

```python
# Complete diagnosis in two lines
get_dataset_refresh_history(workspace_id, dataset_id)
refresh_dataset(workspace_id, dataset_id)
```

### 3. The surprise audit they asked for "yesterday"

"I need a complete inventory of everything we have in Power BI by tomorrow morning" - the email arrived on Thursday at 5 PM, signed by the CFO. He wanted to know exactly what workspaces we had, who had access to each one, how many datasets were active, what reports were actually being used, and basically a complete x-ray of our data infrastructure. My first reaction was to calculate how many hours this would take me manually: navigate workspace by workspace, note users in an Excel sheet, count resources, verify I wasn't missing anything important. Easily a full day of tedious work. Instead of resigning myself to a long night, I wrote a script using the MCP server to do the entire audit automatically. The next day I delivered a complete Excel report with everything he had asked for.

```python
# Complete automated audit
for workspace in list_workspaces():
    users = get_workspace_users(workspace_id)
    datasets = list_datasets(workspace_id)
    reports = list_reports(workspace_id)
    # Compile everything into a structured report
```

## The technical details that make the difference

After months refining the code, there are three technical aspects that really separate a functional script from a tool you can use daily without frustrations.

### 1. Errors that actually help instead of confusing you

If you've worked with Microsoft APIs, you know the error messages can be... creative. I remember once spending two hours trying to understand what "HTTP 400 Bad Request" meant when I was trying to refresh a dataset. Turns out the problem was that the dataset was being used by another process, but the error didn't give me a hint about that. In the MCP server, when something fails, the error message tells you exactly what happened and what you can do to fix it. Instead of incomprehensible stack traces, you get messages like "Dataset not found in workspace" or "User lacks permissions for this operation". It's the difference between spending hours debugging and fixing the problem immediately.

### 2. Authentication that simply works

OAuth2 authentication with Azure AD is one of those topics that can quickly become a nightmare. Tokens that expire, scopes that change depending on the endpoint, HTTP headers that have to be exact or everything fails silently. I've lost entire days fighting with authentication when all I really wanted was to make a simple query to a dataset. The `FabricApi` class encapsulates all this complexity - you provide the credentials once in environment variables and the server handles getting tokens, renewing them when they expire, building the correct headers, and even handling the difference between regular and administrative endpoints that require different permissions. It's the difference between spending half a day configuring authentication and starting to use the tool immediately.

### 3. A simple switch between normal and admin permissions

One of the most confusing things about the Power BI API is that some functions require administrative permissions and others don't, but that's not always clear in the documentation. Functions like `get_capacities()` or `get_tenant_workspaces()` only work with elevated privileges, while operations like refreshing your own dataset work with regular permissions. The `use_admin=True` parameter lets you switch between these modes without having to understand the internal complexities of the API. If you have admin permissions, you can access information from the entire tenant; if not, the server automatically uses the regular endpoints available to any user.

## What comes next: the automation I still need to implement

Once the server is running in your environment, you'll start to see automation opportunities that never occurred to you before. I'm already working on a second version that includes automatic monitoring of my datasets' health (that sends me a notification if any refresh fails), integration with our ticketing system to automatically create cases when there are data issues, and even an internal chatbot that answers business metrics questions by executing DAX queries in real time. The fundamental difference is that you go from thinking about individual tasks to thinking about complete workflows that orchestrate themselves.

## Why you should try it (even if it's a Friday afternoon)

The most valuable thing about this tool isn't the lines of code or specific functions, but how it completely changes your relationship with Microsoft Fabric. You stop being someone who opens browser tabs to do repetitive administrative tasks and become someone who asks an intelligent assistant to do the work for you. The next time you find yourself doing the same tedious sequence of clicks in Power BI for the third time in a week, instead of resigning yourself thinking "that's just how things are", you'll be able to ask yourself if there's a way to automate that process - and almost always the answer will be yes.

If you have Microsoft Fabric and fifteen minutes free on a Friday afternoon (the best time to try new things without pressure), I challenge you to set up your own MCP server and try at least the workspace listing function. The experience of writing "show me all my workspaces" and seeing how Claude understands exactly what you want and returns the information perfectly formatted will change your perspective on what's possible when you combine AI with the tools you already use every day.

Have you built something similar to automate your daily data work? What repetitive tasks would you like to delegate to an intelligent assistant? I'm fascinated to learn how different people tackle the same challenges in creative ways, especially in this Microsoft Fabric world where every month seems to bring new possibilities that were previously unthinkable.

---

**To get started:** All the code is in the `Fabric_server.py` file - you just need your Azure credentials and five minutes to set up the environment. If you find any bugs or think of improvements, it's always a good time to contribute. After all, the best tools are born when someone shares an idea and the community adopts and collectively improves it.