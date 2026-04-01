#!/usr/bin/env node
// Buddy Reroll — brute-force a SALT that produces a buddy matching the user's criteria.
// Usage: node buddy_reroll.mjs [--species X] [--rarity X] [--shiny] [--eye X] [--hat X] [--apply] [--limit N]

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import { homedir } from 'os';
import { join } from 'path';

// ── Roll algorithm (mirrors src/buddy/companion.ts exactly) ──────────────────

function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function hashString(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function pick(rng, arr) { return arr[Math.floor(rng() * arr.length)]; }

const RARITIES = ['common','uncommon','rare','epic','legendary'];
const RARITY_WEIGHTS = { common:60, uncommon:25, rare:10, epic:4, legendary:1 };
const SPECIES = ['duck','goose','blob','cat','dragon','octopus','owl','penguin',
  'turtle','snail','ghost','axolotl','capybara','cactus','robot','rabbit','mushroom','chonk'];
const EYES = ['·','✦','×','◉','@','°'];
const HATS = ['none','crown','tophat','propeller','halo','wizard','beanie','tinyduck'];
const STAT_NAMES = ['DEBUGGING','PATIENCE','CHAOS','WISDOM','SNARK'];
const RARITY_FLOOR = { common:5, uncommon:15, rare:25, epic:35, legendary:50 };
const RARITY_STARS = { common:'★', uncommon:'★★', rare:'★★★', epic:'★★★★', legendary:'★★★★★' };

function rollRarity(rng) {
  let roll = rng() * 100;
  for (const r of RARITIES) { roll -= RARITY_WEIGHTS[r]; if (roll < 0) return r; }
  return 'common';
}

function rollStats(rng, rarity) {
  const floor = RARITY_FLOOR[rarity];
  const peak = pick(rng, STAT_NAMES);
  let dump = pick(rng, STAT_NAMES);
  while (dump === peak) dump = pick(rng, STAT_NAMES);
  const stats = {};
  for (const name of STAT_NAMES) {
    if (name === peak) stats[name] = Math.min(100, floor + 50 + Math.floor(rng() * 30));
    else if (name === dump) stats[name] = Math.max(1, floor - 10 + Math.floor(rng() * 15));
    else stats[name] = floor + Math.floor(rng() * 40);
  }
  return stats;
}

function rollFrom(rng) {
  const rarity = rollRarity(rng);
  const species = pick(rng, SPECIES);
  const eye = pick(rng, EYES);
  const hat = rarity === 'common' ? 'none' : pick(rng, HATS);
  const shiny = rng() < 0.01;
  const stats = rollStats(rng, rarity);
  return { rarity, species, eye, hat, shiny, stats };
}

function roll(userId, salt) {
  return rollFrom(mulberry32(hashString(userId + salt)));
}

// ── Config helpers ───────────────────────────────────────────────────────────

function findConfigPath() {
  const legacy = join(homedir(), '.claude', '.config.json');
  if (existsSync(legacy)) return legacy;
  const standard = join(homedir(), '.claude.json');
  if (existsSync(standard)) return standard;
  return null;
}

function readConfig() {
  const p = findConfigPath();
  if (!p) { console.error('ERROR: Cannot find Claude config file.'); process.exit(1); }
  return { path: p, data: JSON.parse(readFileSync(p, 'utf8')) };
}

function getUserId() {
  const { data } = readConfig();
  return data.oauthAccount?.accountUuid ?? data.userID ?? 'anon';
}

function findCliJs() {
  // Method 1: resolve from `which claude`
  try {
    const bin = execSync('which claude', { encoding: 'utf8' }).trim();
    const real = execSync(`readlink -f "${bin}" 2>/dev/null || realpath "${bin}" 2>/dev/null || echo "${bin}"`, { encoding: 'utf8' }).trim();
    // Walk up to find cli.js — typically in the same package
    const dir = real.replace(/\/bin\/claude(\.js)?$/, '');
    const candidate = join(dir, 'cli.js');
    if (existsSync(candidate)) return candidate;
    // npm global layout: .../node_modules/@anthropic-ai/claude-code/bin/claude → ../cli.js
    const candidate2 = join(dir, '..', 'cli.js');
    if (existsSync(candidate2)) return candidate2;
  } catch {}
  // Method 2: common npm global paths
  const npmPaths = [
    execSync('npm root -g 2>/dev/null', { encoding: 'utf8' }).trim(),
  ].filter(Boolean);
  for (const root of npmPaths) {
    const p = join(root, '@anthropic-ai', 'claude-code', 'cli.js');
    if (existsSync(p)) return p;
  }
  return null;
}

// ── Parse args ───────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const opts = { apply: false, limit: 500000, maxResults: 10 };
  let i = 2;
  while (i < argv.length) {
    const a = argv[i];
    if (a === '--species' && argv[i+1]) { opts.species = argv[++i].toLowerCase(); }
    else if (a === '--rarity' && argv[i+1]) { opts.rarity = argv[++i].toLowerCase(); }
    else if (a === '--shiny') { opts.shiny = true; }
    else if (a === '--eye' && argv[i+1]) { opts.eye = argv[++i]; }
    else if (a === '--hat' && argv[i+1]) { opts.hat = argv[++i].toLowerCase(); }
    else if (a === '--apply' && argv[i+1]) { opts.apply = argv[++i]; }
    else if (a === '--limit' && argv[i+1]) { opts.limit = parseInt(argv[++i], 10); }
    else if (a === '--max-results' && argv[i+1]) { opts.maxResults = parseInt(argv[++i], 10); }
    else if (a === '--show-current') { opts.showCurrent = true; }
    i++;
  }
  return opts;
}

// ── Main ─────────────────────────────────────────────────────────────────────

const opts = parseArgs(process.argv);
const userId = getUserId();

// Show current buddy
if (opts.showCurrent) {
  const current = roll(userId, 'friend-2026-401');
  const { data } = readConfig();
  console.log(JSON.stringify({
    current_salt: 'friend-2026-401',
    bones: current,
    soul: data.companion ?? null,
    userId_prefix: userId.slice(0, 12) + '...',
  }, null, 2));
  if (!opts.species && !opts.rarity && !opts.shiny) process.exit(0);
}

// Search
function matches(buddy) {
  if (opts.species && buddy.species !== opts.species) return false;
  if (opts.rarity && buddy.rarity !== opts.rarity) return false;
  if (opts.shiny && !buddy.shiny) return false;
  if (opts.eye && buddy.eye !== opts.eye) return false;
  if (opts.hat && buddy.hat !== opts.hat) return false;
  return true;
}

const results = [];
for (let i = 0; i < opts.limit && results.length < opts.maxResults; i++) {
  const salt = `friend-2026-${i}`;
  const buddy = roll(userId, salt);
  if (matches(buddy)) {
    results.push({ salt, ...buddy });
  }
}

// Output results as JSON for Claude to parse
console.log(JSON.stringify({
  userId_prefix: userId.slice(0, 12) + '...',
  criteria: { species: opts.species, rarity: opts.rarity, shiny: opts.shiny, eye: opts.eye, hat: opts.hat },
  searched: opts.limit,
  found: results.length,
  results: results.map(r => ({
    salt: r.salt,
    rarity: r.rarity,
    stars: RARITY_STARS[r.rarity],
    species: r.species,
    eye: r.eye,
    hat: r.hat,
    shiny: r.shiny,
    stats: r.stats,
  })),
}, null, 2));

// Apply if requested
if (opts.apply && results.length > 0) {
  const target = typeof opts.apply === 'string' && opts.apply !== 'true'
    ? results.find(r => r.salt === opts.apply) ?? results[0]
    : results[0];

  const cliJs = findCliJs();
  if (!cliJs) {
    console.error('\nERROR: Cannot find installed cli.js. Provide path manually.');
    process.exit(1);
  }

  // Patch SALT
  const content = readFileSync(cliJs, 'utf8');
  const saltRegex = /friend-2026-\d+/g;
  const matchCount = (content.match(saltRegex) || []).length;
  if (matchCount === 0) {
    console.error('\nERROR: Cannot find SALT pattern in cli.js');
    process.exit(1);
  }
  const newSalt = target.salt;
  const patched = content.replace(saltRegex, newSalt);
  writeFileSync(cliJs, patched);

  // Delete companion from config
  const cfg = readConfig();
  delete cfg.data.companion;
  writeFileSync(cfg.path, JSON.stringify(cfg.data, null, 2) + '\n');

  console.log(JSON.stringify({
    applied: true,
    salt: newSalt,
    cli_js: cliJs,
    config: cfg.path,
    buddy: { rarity: target.rarity, species: target.species, shiny: target.shiny },
    next_step: 'Restart Claude Code and run /buddy to hatch your new buddy!',
  }, null, 2));
}
