# AGENTS.md

## Project

Early-stage Python project. Boilerplate PyCharm `main.py`, one placeholder stub (`proxmox.py`), one working module (`my_nmap.py`). Intended purpose likely Proxmox + Nmap automation or integration.

## Toolchain

- **Python** >= 3.13
- **uv** for package management (`uv.lock` present)
- **Dependencies** (`pyproject.toml`): `proxmoxer==2.3.0`, `requests==2.34.2`, `python-nmap`
- **System dep:** `nmap` binary at `/usr/bin/nmap` (v7.98)
- Virtual env at `.venv/` (already populated)

## Commands

```sh
uv sync          # install dependencies from lockfile
uv add <pkg>     # add new dependency
uv run python main.py  # run a script with venv active
```

## Notes

- No tests, no CI, no linter/formatter/typechecker configured.
- Not a git repository.
- `my_nmap.py` provides `scan_network(network, timeout, ports, arguments)` — uses `python-nmap` with a `ping` fallback.
- If you add real code in `proxmox.py`, consider configuring pytest, ruff, and mypy.
