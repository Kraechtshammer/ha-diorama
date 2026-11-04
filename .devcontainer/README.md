# Dev container (local setup)

This folder lives on the fork only, not in the upstream repo. Only
`claude.env.local`, which holds the token, stays out of git.

## Needs on the host

- Docker Desktop (with the WSL 2 backend on Windows)
- VS Code with the Dev Containers extension

## Open it

Open the repo folder in VS Code, then run **Dev Containers: Reopen in Container**.
The first build takes a few minutes. It installs pnpm and the project's
packages and the extensions listed in `devcontainer.json`.

## Claude Code token

1. In the container's terminal run `claude setup-token` and follow the login.
   This needs a Pro, Max, Team or Enterprise plan. The token is valid for a year.
2. Paste it into `claude.env.local` on the `CLAUDE_CODE_OAUTH_TOKEN=` line and
   remove the leading `# `. You can use `ANTHROPIC_API_KEY=` instead.
3. Run **Dev Containers: Rebuild Container**. The env file is only read when
   the container is created, so a plain restart does not pick it up.

`claude.env.local` is ignored by git through the repo's `*.local` rule.
Check it with `git check-ignore -v .devcontainer/claude.env.local`.

## Working on the card

- `pnpm dev` starts Vite on port 5173. VS Code forwards it to the same port
  on your machine, so Home Assistant can load
  `http://localhost:5173/src/dev/entry.ts` as described in `docs/DEVELOPMENT.md`.
- `pnpm build` writes `dist/` into the repo folder on your disk.
- The demo Home Assistant (`ha-demo`) runs from a terminal on your host,
  not from inside the container: `cd ha-demo` and `docker compose up -d`.
  Then open http://localhost:8124.
