# 🌍 ConwayBox

A **worldbox-style world simulator built entirely on Conway's Game of Life.**
Everything in the world is a Conway-family cellular automaton (a totalistic
neighbour-count rule) — there is no other engine underneath.

Open [`index.html`](index.html) in any modern browser. No build step, no install.

## The CA layers

| Layer | Rule | Meaning |
|-------|------|---------|
| **Life** | literal Conway **B3/S23** | living matter / civilizations |
| **Terrain** | majority-smoothing CA | continents grown from noise |
| **Water** | Conway-variant flood CA | seas, lakes, coastal flooding |
| **Forest** | slow birth/survival CA | vegetation life feeds on |
| **Fire** | spreading CA | burns forest & life, then dies out |
| **Temperature** | diffusion CA + latitude source | climate field, swings with seasons |
| **Humidity** | diffusion CA, water-sourced | drives wet/dry biomes |
| **Ice** | threshold CA (hysteresis) | polar caps & glaciers |

**Biomes** (snow, tundra, desert, grassland, forest, swamp, ice, sea) are read
off the temperature + humidity fields each frame and steer where life can grow.

## Civilizations

Living cells carry a **faction** identity. Birth/death stay pure Conway B3/S23;
faction is decided by a strength-weighted neighbour vote (still a totalistic
rule). Empires:

- **expand** — strong factions colonise empty fertile land at their edge;
- **conquer** — border cells flip to a neighbouring faction that out-musters them;
- **develop** — cells that survive a long time age into bright "city" cores.

The world is seeded as a Voronoi map of bordering nations, so empires share
frontiers and go to war from the start. A live leaderboard tracks each
civilization's population and trend.

## God tools

Every tool works by writing cells into a CA grid — the player never escapes
Conway either: Life, Colony, Raise land, Water, Forest, Fire, Meteor, Erase.

## Controls

- **Drag** to paint with the selected tool
- `Space` play/pause · `S` step · `1–9` select tool
- `[` `]` brush size · `C` clear life · `N` new world
- **Detail** slider sets the pixel size (resolution); the grid auto-fits the screen.
