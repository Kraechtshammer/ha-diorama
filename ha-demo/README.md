# Demo Home Assistant

A Home Assistant in Docker with the demo flat already on a dashboard, so you can see the card working against real entities without setting anything up. The devices come from Home Assistant's own Demo integration: lights, covers, a vacuum, media players, a thermostat and the rest are all made up, and they respond when you use them.

## Run it

You need Node, pnpm and Docker. From the root of the repo, build the card once:

```bash
pnpm install
pnpm build
```

Then start Home Assistant from this folder:

```bash
cd ha-demo
docker compose up -d
```

Open http://localhost:8124. The first start takes a minute or two. There is no onboarding and no login: the owner `demo`, with the password `demo`, is created on the first start and a browser on this machine is logged in as it straight away. For that reason the port is only open to this machine. Once you are in, open Diorama in the sidebar.

It runs on port 8124, so it can sit next to another Home Assistant on the usual 8123.

## What is in it

- `compose.yaml` mounts the repo's `dist` folder, so the dashboard always runs the card you last built, and the `themes` folder, for the Diorama Glass theme the dashboard uses.
- `config/configuration.yaml` loads the Demo integration and registers the card and the dashboard in YAML. It adds a projector screen, which the Demo integration does not have, Projector scene, TV scene, All lights and Cleaning switches for the side panel's Home section, and sets the demo lights to a warm white and turns the living room TV off on every start.
- `config/diorama.yaml` is the dashboard. It is written by `pnpm demoflat` from `scripts/demoflat.plan.ts`, the same plan as `demoflat.yaml`, with each piece bound to its Demo integration entity. Do not edit it by hand.
- `seed/onboard.py` goes through the onboarding on the first start, and `config/configuration.yaml` logs the browser in without a password through Home Assistant's trusted networks login.
- `seed/editable.py` runs before Home Assistant on every start and adds Diorama (editable), a dashboard in storage mode with a copy of `config/diorama.yaml`, so the editor can be tried on the demo flat.
- `seed/core.config_entries` sets up the backyard camera on the first start, since that kind of camera can only be added from the UI. It loops `config/cameras/backyard.gif`, made from [a clip on Pexels](https://www.pexels.com/video/a-black-cat-on-the-backyard-9337775/).

Everything else Home Assistant writes into `config` while it runs stays out of git.

## Try your changes

Run `pnpm watch` in the repo root, or `pnpm build` after each change, and reload the page with the cache cleared.

The Diorama dashboard is kept in YAML, so it cannot be saved from the UI. To try the editor, open Diorama (editable) in the sidebar instead: it holds a copy of the same flat, bound to the same entities, and keeps what you change there. To start that copy again from the current `config/diorama.yaml`, delete `config/.storage/lovelace.diorama_editable` and restart the container.

## Start again

To throw everything away, including the owner account, stop it and clear what Home Assistant wrote:

```bash
docker compose down
git clean -fdX config
```
