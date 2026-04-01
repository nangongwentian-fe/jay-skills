---
name: buddy-reroll
description: >
  Reroll your Claude Code buddy (companion) to get a specific species, rarity, or shiny variant.
  Use when the user says "reroll buddy", "change my buddy", "I want a shiny buddy",
  "give me a legendary dragon", "/buddy-reroll", or any request to customize their Claude Code companion pet.
---

# Buddy Reroll

Reroll the Claude Code `/buddy` companion by brute-forcing the internal SALT constant to find a seed that produces the desired buddy for the user's account.

## How it works

Buddy generation is deterministic: `hash(userId + SALT)` seeds a PRNG that decides species, rarity, shiny, etc. Changing SALT changes the outcome. The script tries up to 500k SALT values to find matches.

## Available attributes

- **species** (18): duck, goose, blob, cat, dragon, octopus, owl, penguin, turtle, snail, ghost, axolotl, capybara, cactus, robot, rabbit, mushroom, chonk
- **rarity**: common (60%), uncommon (25%), rare (10%), epic (4%), legendary (1%)
- **shiny**: 1% chance per roll
- **eye**: `·` `✦` `×` `◉` `@` `°`
- **hat**: none, crown, tophat, propeller, halo, wizard, beanie, tinyduck (common rarity always gets none)

## Workflow

### Step 1: Ask what the user wants

If the user didn't specify, ask which attributes matter to them (species, rarity, shiny, etc.). Not all combinations are findable within 500k iterations — rarer combos (e.g. legendary + shiny + specific species) may have 0-3 results.

### Step 2: Search for matching SALTs

Run the bundled script with the user's criteria:

```bash
node <skill-dir>/scripts/buddy_reroll.mjs --species dragon --rarity legendary --shiny --max-results 10
```

Flags: `--species X`, `--rarity X`, `--shiny`, `--eye X`, `--hat X`, `--max-results N`, `--show-current`

The script auto-detects the user's userId from their Claude config. Output is JSON.

### Step 3: Present results

Show a table of matching buddies with salt, rarity, species, eye, hat, shiny, and stats. Let the user pick one.

### Step 4: Apply the chosen SALT

Run with `--apply <salt>` to patch cli.js and clear the old companion:

```bash
node <skill-dir>/scripts/buddy_reroll.mjs --species dragon --shiny --apply "friend-2026-1578"
```

This will:
1. Replace the SALT in the installed `cli.js` (auto-detected via `which claude`)
2. Delete the `companion` field from the user's Claude config

### Step 5: Instruct user

Tell the user to **restart Claude Code** and run `/buddy` to hatch their new companion.

Warn: upgrading Claude Code (`npm update`) will reset the SALT — they'll need to reroll again.
