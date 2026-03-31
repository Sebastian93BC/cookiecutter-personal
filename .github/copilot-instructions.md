# universal-ide-agents — Repository Guidance

## Scope

This repository is the canonical source of reusable VS Code customization assets.

Current scope:
- `.github/agents/*.agent.md`
- `.github/instructions/*.instructions.md`
- `.github/prompts/*.prompt.md`
- `.github/hooks/*.json`
- `.github/skills/*/SKILL.md`
- `scripts/*.sh`
- `docs/*.md`

Out of scope for `v0.1.0`:
- JetBrains, Zed, Cursor, Windsurf, or other editor-specific layouts
- Project-specific business rules or domain assumptions
- Non-portable hook or script implementations

## Authoring Rules

- Keep all reusable AI assets in English.
- Write frontmatter as valid YAML and make `description` specific enough to trigger correctly.
- Prefer small, composable assets over large monolithic files.
- Keep prompts, agents, hooks, instructions, and skills VS Code-first and project-agnostic.
- Treat scripts as helper tooling for setup, sync, and context injection, not as product code.
- Document any new asset in the README or asset catalog when it changes discoverability.

## Naming Conventions

- Agents: `Name.agent.md`
- Instructions: `Name.instructions.md`
- Prompts: `Name.prompt.md`
- Skills: `.github/skills/<skill-name>/SKILL.md`
- Hooks: descriptive `.json` files under `.github/hooks/`
- Shell tooling: kebab-case under `scripts/`

## Quality Bar

- README and CHANGELOG should feel editorial, but still render cleanly on GitHub without custom CSS.
- Hook commands must point to scripts that exist in this repository.
- Scripts should be POSIX-friendly where practical and avoid unnecessary dependencies.
- Do not describe unsupported editor integrations as if they already exist.
- Use Semantic Versioning and update the CHANGELOG whenever shared assets change meaningfully.

## Contribution Focus

When you extend this repository, prioritize one of these outcomes:
- Make an existing VS Code asset easier to reuse across projects.
- Improve discoverability of the asset catalog.
- Add safe automation for installing, syncing, or validating shared assets.
- Strengthen documentation for teams consuming the repository as a secondary configuration source.