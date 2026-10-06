# dwrap

**D**irectory **wrap**. Media files often live in eponymous directories
(`movie (2001)/movie (2001).mkv`), but sometimes arrive "naked". `dwrap` wraps
each file you give it in a directory of the same name.

```
dwrap [--dry-run] [--strip-extensions] PATH...
```

Pass files via your shell's glob, e.g. `dwrap --strip-extensions *.mkv`.
Arguments that are directories are ignored.

```
$ dwrap --dry-run --strip-extensions "movie (2001).mkv"
movie (2001).mkv -> movie (2001)/movie (2001).mkv
```

## Options

- `--dry-run` – show what would happen without changing anything.
- `--strip-extensions` – name the directory after the file without its
  extension (`movie (2001).mkv` → `movie (2001)/`). Without it, the directory
  has the file's full name (`movie (2001).mkv/movie (2001).mkv`).

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
