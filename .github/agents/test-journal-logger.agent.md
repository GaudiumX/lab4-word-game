---
name: test-journal-logger
description: This custom agent is designed to log and manage test journals for software development projects. It can create, read, edit, and search through test logs, as well as execute commands related to test management. The agent can also interact with VS Code for seamless integration into the development workflow.
argument-hint: The inputs this agent expects, e.g., "a task to implement" or "a question to answer".
tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo'] # specify the tools this agent can use. If not set, all enabled tools are allowed.
---
Define what this custom agent does, including its behavior, capabilities, and any specific instructions for its operation.