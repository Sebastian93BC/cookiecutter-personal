# Cookiecutter Data Science Template — AI Agent Guidelines

## What this repo is

A **Cookiecutter template** for reproducible data science projects. Running
`cookiecutter .` (or `cookiecutter <repo-url>`) generates a fully structured
Python project with conda environment, src layout, notebooks, tests, and
optional CI/CD.

**Do not confuse with the generated project.** All files inside
`{{ cookiecutter.project_slug }}/` are the *template* for the generated
project — Jinja2 expressions are rendered at generation time.

---

## Repository layout

```
cookiecutter.json                  # Template variables & defaults
hooks/
  pre_gen_project.py               # Validation before generation
  post_gen_project.py              # Cleanup + git init after generation
{{ cookiecutter.project_slug }}/   # Template directory (rendered by cookiecutter)
  environment.yml
  pyproject.toml
  tasks.py
  src/
    data/        make_dataset.py
    features/    build_features.py, feature_diagnostics.py
    models/      models.py, train_model.py, predict_model.py
    utils/       paths.py, general_functions.py
    visualization/ visualize.py
  notebooks/
  tests/
  config/config.yml
environment.yml                    # Dev env for template contributors
CHANGELOG.md
```

---

## Development environment (template contributors)

```bash
# Create / activate the template development environment
conda env create --file environment.yml   # creates platzi_machine_learning
conda activate platzi_machine_learning
```

The `.vscode/settings.json` at the root auto-selects this interpreter.

---

## Testing a change end-to-end

```bash
# From the PARENT directory of this repo:
cookiecutter template-data-science-base --no-input

# With custom values:
cookiecutter template-data-science-base --no-input \
  project_name="My Project" \
  remote_url="https://github.com/user/repo"

# Verify generated project
cd my_project
conda env create --file environment.yml
conda activate my_project
python -c "from src.utils.paths import data_raw_dir; print(data_raw_dir())"
```

---

## Jinja2 patterns used in this template

| Pattern | Where | Purpose |
|---|---|---|
| `{{ cookiecutter.project_slug }}` | directory name, env name, settings | Rendered to project slug |
| `{{ cookiecutter.python_version }}` | `environment.yml` | Python version |
| `{% if cookiecutter.use_dvc == "yes" %}` | `environment.yml`, hooks | Conditional deps / files |
| `{% if cookiecutter.project_scope == "production" %}` | `environment.yml` | CI/CD deps |
| `{{ cookiecutter.remote_url }}` | `post_gen_project.py` | Optional git remote |

**Rules:**
- Jinja2 expressions inside `hooks/` are rendered at generation time — they evaluate to plain strings.
- Files inside `{{ cookiecutter.project_slug }}/` keep their Jinja2 syntax until rendered.
- Never add logic to template files that depends on runtime Python imports — use hooks instead.

---

## cookiecutter.json fields

| Field | Type | Notes |
|---|---|---|
| `project_name` | string | Human-readable name |
| `project_slug` | derived | Auto-computed from `project_name` |
| `project_author_name` | string | |
| `project_author_email` | string | |
| `project_description` | string | |
| `project_open_source_license` | choice | `No license file`, `MIT`, `BSD-3-Clause` |
| `project_packages` | choice | `All` (full deps) or `Minimal` |
| `python_version` | string | Default `3.11` |
| `project_version` | string | SemVer, default `0.1.0` |
| `project_scope` | choice | `exploratory` (no CI) or `production` (adds pre-commit, pytest) |
| `use_dvc` | choice | `no` / `yes` — adds DVC dep and `.dvcignore` |
| `use_uv` | choice | `no` / `yes` |
| `remote_url` | string | Empty = no remote; non-empty = `git remote add origin <url>` |

---

## Hook logic (post_gen_project.py)

```
Remove LICENSE          if project_open_source_license == "No license file"
Remove .dvcignore       if use_dvc == "no"
Remove .github/, .pre-commit-config.yaml  if project_scope == "exploratory"
git init && git add . && git commit -m "Initial commit"
git remote add origin <remote_url>  if remote_url is not empty
```

---

## Common tasks

### Add a new template variable

1. Add the field and default to `cookiecutter.json`
2. Reference `{{ cookiecutter.new_field }}` in the relevant template files
3. Add conditional removal logic in `post_gen_project.py` if needed
4. Document the field in this file and in `CHANGELOG.md`
5. Test: `cookiecutter . --no-input` + `cookiecutter . --no-input new_field=value`

### Add a new source module

1. Create the file under `{{ cookiecutter.project_slug }}/src/<subpackage>/`
2. Update `{{ cookiecutter.project_slug }}/src/<subpackage>/__init__.py` if needed
3. Add a demo section to `notebooks/00-manual-src.ipynb`
4. Add/update tests in `tests/`

### Update the project environment

Edit `{{ cookiecutter.project_slug }}/environment.yml`.
Remember: `name:` must stay as `{{ cookiecutter.project_slug }}` (rendered at generation).

### Update the development environment (this repo)

Edit the **root** `environment.yml` (env name: `platzi_machine_learning`).

---

## Code style

- Python: follow `ruff` defaults (configured in `pyproject.toml` of generated projects)
- Hooks: plain Python stdlib + `subprocess`, no third-party imports
- Template files: 4-space indentation for Python, 2-space for YAML
- Comments in Spanish or English are both acceptable (mixed is fine)

---

## What NOT to do

- Do not import from `src/` inside `hooks/` — hooks run in a fresh Python process
- Do not hardcode the project slug anywhere outside `cookiecutter.json`
- Do not add `.vscode/` to version control of *generated* projects (machine-specific)
- Do not push directly to `main` — use feature branches and PRs
- **Styling**: Pure CSS with theme support. Light/dark mode toggle in [style.css](../style.css) uses `data-theme` attribute.
- **Database**: SQLite with `better-sqlite3`. Schema in [server/index.js](../server/index.js) lines 16–26.
- **Formatting**: Use 2-space indentation, semicolons, camelCase for variables/functions.

## Architecture

**Frontend** (`index.html`, `script.js`, `style.css`):
- Client-side rendering with state variables: `todos`, `currentFilter`, `currentCategoryFilter`
- Offline-first: localStorage fallback when server unavailable
- Auto-sync on every save with `POST /api/sync` endpoint
- Health check via periodic `GET /api/health` (every 10 seconds if `needsSync`)

**Backend** (`server/`):
- Express server with SQLite persistence
- Data lifecycle: todos table (id, text, state, category, created_at, updated_at)
- CORS enabled for cross-origin requests from frontend
- Three sync strategies: `POST /api/sync` (full state), `POST /api/migrate` (import), GET `/api/todos` (load)

**Data Flow**:
1. User action (add/edit/delete) → `script.js` modifies `todos` array
2. `saveTodos()` → localStorage immediately, then async `POST /api/sync` to server
3. Server sync fails → `needsSync = true`, retry every 10 seconds
4. App startup → `loadTodosFromServerOrLocal()` attempts server, falls back to localStorage

## Build and Test

**Frontend**: No build step required.
```bash
# Serve locally
python3 -m http.server 8000
# Or: npx http-server
# Visit http://localhost:8000
```

**Backend**:
```bash
cd server
npm install
npm run dev
# Starts on http://localhost:3000 with auto-reload via nodemon
```

**Testing Endpoints** (with curl):
```bash
# Get all todos
curl http://localhost:3000/api/todos

# Create new todo
curl -X POST http://localhost:3000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"text":"Buy milk","state":"plan","category":"personal"}'

# Update a todo
curl -X PUT http://localhost:3000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"text":"Buy milk and eggs","state":"done"}'

# Health check
curl http://localhost:3000/api/health
```

## Project Conventions

**Task State Lifecycle** (see [script.js](../script.js) line ~190):
- States: `plan` → `todo` → `done` → back to `plan` (cycles)
- UI shows as badge; click to cycle state
- State changes trigger `saveTodos()`

**Categories** (three fixed values):
- `trabajo`, `personal`, `estudio`
- Default: `personal` for new tasks
- Inline select dropdown in task row

**Filtering** (both filters are independent):
- State filter: All, Plan, To Do, Done (affects `currentFilter`)
- Category filter: All categories, Trabajo, Personal, Estudio (affects `currentCategoryFilter`)
- `renderTodos()` applies both filters together (see [script.js](../script.js) line ~250)

**Inline Editing**:
- Task text: `contentEditable` span, saved on blur or Enter key
- Category: Dropdown select, saves on change
- Updates call `saveTodos()` immediately

## Integration Points

**Client-Server Communication**:
1. **Load**: `GET /api/todos` — Initialize `todos` array on startup
2. **Sync**: `POST /api/sync` — Push complete state (bulk replace), include all todos in body
3. **Migrate**: `POST /api/migrate` — One-time import from localStorage (409 if data exists)
4. **Create**: `POST /api/todos` — Single task creation (alternative to sync)
5. **Update/Delete**: `PUT /api/todos/:id`, `DELETE /api/todos/:id` — Per-item operations

**API URL Configuration**:
- Client: `const API_URL = 'http://localhost:3000/api'` (see [script.js](../script.js) line 11)
- Server: `const PORT = process.env.PORT || 3000` (see [server/index.js](../server/index.js) line 211)

**CORS**: Enabled server-wide (see [server/index.js](../server/index.js) line 11). Restrict in production with specific origin.

## Documentation

In addition to this instruction file, the repository includes several
supporting documents for different audiences:

- `ARCHITECTURE.md` – high-level system architecture and data flow overview.
- `PRODUCT.md` – concise feature summary written for product/stakeholder review.
- `CONTRIBUTING.md` – developer guidelines, workflows, and best practices.

Refer to these files when you need context beyond code or setup.

## Common Tasks

**Adding a feature (e.g., priority levels)**:
1. **Client**: Add `priority` field to todo objects (default: 'medium') in state initialization
2. **UI**: Add priority selector in `renderTodos()` alongside category select
3. **Server**: Add migration SQL to schema (ALTER TABLE) and include field in INSERT/SELECT queries
4. **Endpoints**: Update all API endpoints to accept and return priority field
5. **Test**: Create task with priority, edit it, refresh browser—verify localStorage and server sync

**Debugging offline/sync issues**:
- Check `serverAvailable` flag: should be `true` if server is reachable
- Check `needsSync` flag: should be `false` after successful sync
- DevTools Console: logs indicate "Loaded from server" or "offline mode"
- Open DevTools → Application → Local Storage → inspect `todos` JSON

**Migrating data**:
- Automatic: Start server first, app auto-migrates on load if server is empty
- Manual: Use `POST /api/migrate` endpoint or browser console script (see [MIGRATION.md](../MIGRATION.md))
