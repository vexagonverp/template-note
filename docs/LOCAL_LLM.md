# Using a local model

The rules in `AGENTS.md` work with any agent, including a local model through Ollama and
the VS Code Copilot agent in `.github/agents/notes.agent.md`.

A long sheet needs a big context window. Make one Modelfile per model and put the context
size in the file name, e.g. `.github/ollama/<model>-48k.Modelfile`:

```
FROM <model:tag>
PARAMETER num_ctx 49152
```

```bash
ollama create <model>-48k -f .github/ollama/<model>-48k.Modelfile
```

Pick the largest context your memory allows. If answers start ignoring the rules, the
context is too small for the sheet: work on one section at a time.
