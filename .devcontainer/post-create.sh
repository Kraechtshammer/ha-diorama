#!/usr/bin/env bash
# Runs once inside the container after it is created.
set -euo pipefail

# Named volumes are created owned by root; hand them to the dev user.
sudo chown -R node:node node_modules "${CLAUDE_CONFIG_DIR}"

# Interactive Claude Code ignores CLAUDE_CODE_OAUTH_TOKEN and asks to log in
# until its first-run onboarding is marked as done (anthropics/claude-code#46259).
# With CLAUDE_CONFIG_DIR set the file lives there; ~/.claude.json is a fallback.
for f in "${CLAUDE_CONFIG_DIR}/.claude.json" "${HOME}/.claude.json"; do
  node -e '
    const fs = require("fs"), f = process.argv[1];
    let c = {}; try { c = JSON.parse(fs.readFileSync(f, "utf8")); } catch {}
    if (c.hasCompletedOnboarding !== true) {
      c.hasCompletedOnboarding = true;
      fs.writeFileSync(f, JSON.stringify(c, null, 2));
    }
  ' "$f"
done

# pnpm at the exact version pinned in package.json's packageManager field.
sudo corepack enable
corepack install

# node_modules is its own volume, so pnpm would otherwise put its store in the
# repo folder, as thousands of untracked files.
pnpm config set store-dir "${HOME}/.local/share/pnpm/store"

pnpm install --config.confirmModulesPurge=false

# Report whether Claude Code will find a token.
echo
if [[ "${CLAUDE_CODE_OAUTH_TOKEN:-}${ANTHROPIC_API_KEY:-}" == *$'\r'* ]]; then
  echo "WARNING: the token in .devcontainer/claude.env.local ends in a Windows line break (CRLF)."
  echo "         Switch the file to LF in VS Code's status bar, save, and rebuild the container."
elif [[ "${ANTHROPIC_API_KEY:-}" == sk-ant-oat* ]]; then
  echo "WARNING: ANTHROPIC_API_KEY in .devcontainer/claude.env.local holds a token from \`claude setup-token\`."
  echo "         Put it on the CLAUDE_CODE_OAUTH_TOKEN= line instead and rebuild the container."
elif [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "Claude Code: using ANTHROPIC_API_KEY from .devcontainer/claude.env.local."
elif [[ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]]; then
  echo "Claude Code: using CLAUDE_CODE_OAUTH_TOKEN from .devcontainer/claude.env.local."
else
  echo "Claude Code: no token set yet. Add one to .devcontainer/claude.env.local and rebuild the container,"
  echo "             or sign in once from the Claude panel (the login is kept across rebuilds)."
fi
