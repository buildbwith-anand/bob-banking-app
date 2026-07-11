# GitHub MCP Setup for Demo Participants

This guide connects Bob to GitHub so you can use GitHub tools during the demo session.

## Prerequisites

**Node.js v18 or later** must be installed.

## Step 1 - Generate a GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens/new
2. **Token name:** `Bob Demo`
3. **Expiration:** `7 days`
4. **Scopes:** `repo`, `read:user`
5. Click **Generate token** and copy it immediately.

## Step 2 - Configure Bob

Create `.bob/mcp.json` in your project workspace:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<PASTE_YOUR_TOKEN_HERE>"
      }
    }
  }
}
```

> Keep your token private. Do not commit `.bob/mcp.json` to any repository.

## Step 3 - Verify the Connection

After saving `.bob/mcp.json`, check the MCP panel in Bob for a green connected status.
