# dwrap

**D**irectory **wrap**. Media files often live in eponymous directories
(`movie (2001)/movie (2001).mkv`), but sometimes arrive "naked". `dwrap` wraps
each file you give it in a directory of the same name.

```
dwrap [--dry-run] [--preserve-extensions] PATH...
```

Pass files via your shell's glob, e.g. `dwrap *.mkv`.
Arguments that are directories are ignored.

```
$ dwrap --dry-run "movie (2001).mkv"
movie (2001).mkv -> movie (2001)/movie (2001).mkv
```

## Options

- `--dry-run` – show what would happen without changing anything.
- `--preserve-extensions` – name the directory after the full file name,
  including its extension (`movie (2001).mkv/movie (2001).mkv`). By default
  the extension is dropped (`movie (2001).mkv` → `movie (2001)/`).

## Name clashes

If the directory name is already taken (by an existing item, or by an earlier
file in the same run), `dwrap` warns and numbers the new directory:
`movie (2001) (1)`, `movie (2001) (2)`, and so on. Nothing is overwritten.

## Install

```
pipx install dwrap
```

## Development

```
pip install -e . pytest
pytest
```
