# Tulpar CLI Development Log

## 2022.04.05
I've finished a very basic version of Tulpar, so the next item will be to create the cli tool for working with, and creating tulpar applications. For that, I have chosen to use Typer and Rich as the primary tools by which a project will be initialized. 

### Layout of the Cli
In the past I've created a separate file for nearly every command. I think that's a little redundant and wasteful. As such, I think I'd be better served by creating files for command *groups* instead. This is a more logical separation as well.

In relation to the commands, there are 3 major groups, plus one command:
- Manage
    - Lint
    - Format
    - Test 
    - Audit
- New
- Generate
    - Page
    - Resource
    - Model
    - Hook
    - Middleware
- Run
    - Dev

So my plan is for a module for generate, a module for manage, a module for run (I might change the name), and new will be on the main application file.

### Structure of a Tulpar Application
```
pyproject.toml
README.md
.gitignore
tests/
<app>/
  | config.py
  | app.py
  | __init__.py
  services/
  pages/
  resources/
  orm/
  middleware/
  hooks/
```