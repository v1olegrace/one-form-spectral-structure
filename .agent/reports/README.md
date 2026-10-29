# Verification records

Each file records one task: what was asked, what was run, and what came out.
P0–P14 are the 22–23 October plan, and R0–R11 are the review rounds of
23–24 October.

The evidence a record cites is of two kinds.

- **Computation evidence** is tracked in `.agent/evidence/`. It includes
  scripts with their outputs, such as `R8-windows.py` and `R8-windows.json`,
  and literature reads with SHA-256 hashes. A record's numbers can be
  recomputed from these files.
- **Test-run records** are not tracked. These are the `*-full-tests`,
  `*-verify`, `*-bib` and similar files, with their `.log` files. They hold
  the command, exit code and pytest summary of one local run, and absolute
  local paths. A record quotes the count it relied on. To reproduce one, run
  `python -m pytest tests` on the same tree.
