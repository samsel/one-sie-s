#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ToolSchema,
} from "@modelcontextprotocol/sdk/types.js";

import { execSync } from "child_process";

// Server setup
const server = new Server(
    {
      name: "mac-volume-controller",
      version: "0.1.0",
    },
    {
      capabilities: {
        tools: {},
      },
    },
  );

// Tool implementations
function muteComputer() {
    execSync('osascript -e "set volume with output muted"');
}

function unMuteComputer() {
    execSync('osascript -e "set volume without output muted"');
}

// Tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: "mute_computer",
          description:
            "Mute the computer. " +
            "Turn OFF the volume in MAC. " +
            "Mutes the laptop and volume is set to zero. ",
            inputSchema: {
                type: "object",
                properties: {},
                required: [],
            },
        },
        {
            name: "unmute_computer",
            description:
              "Unmute the computer. " +
              "Turn ON the volume in MAC. " +
              "unMutes the laptop and volume is not set to zero. ",
              inputSchema: {
                  type: "object",
                  properties: {},
                  required: [],
              },
          },        
      ],
    };
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
      const { name, arguments: args } = request.params;
  
      switch (name) {
        case "mute_computer": {
            muteComputer();
            return {
                content: [{ type: "text", text: "you mac is muted now" }],
          };
        }

        case "unmute_computer": {
            unMuteComputer();
            return {
                content: [{ type: "text", text: "you mac is unmuted now" }],
          };
        }        
  
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text", text: `Error: ${errorMessage}` }],
        isError: true,
      };
    }
  });

// Start server
async function runServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("MCP Volume Controller Server running on stdio");
  }
  
  runServer().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
  });
