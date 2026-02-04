# Copilot instructions for TaskManager

Purpose: help AI coding assistants be productive in this repository by summarizing architecture, workflows, conventions, and quick examples.

- **Big picture**: This is a single-process CLI task manager. The entrypoint is `main.py` which constructs a `TaskManager` and a `Controller` and then reads commands from stdin.
- **Primary responsibilities**:
  - `src/manager.py` — orchestrates two data structures: a B-Tree (`src/core/BTree.py`) for fast lookup by task id, and an Interval Tree (`src/core/intervalTree.py`) for interval overlap queries.
  - `src/controller.py` — maps CLI commands to manager operations; validates and parses string arguments into integers.
  - `src/core/task.py` — the `Task` dataclass (id, start_time, end_time, value).

- **Why this structure**: the project separates identity-based operations (B-Tree) from temporal overlap operations (Interval Tree). The `TaskManager` composes both to maintain consistency: insert/remove calls update both structures.

- **Key conventions & patterns**:
  - CLI commands are case-sensitive strings like `InsertTask`, `DeleteTask`, `UpdateTask`, `QueryTaskId`, `QueryTaskSum` (see `src/controller.py`). AI edits should preserve these names unless updating all callers.
  - Controller functions accept `args: list` (strings); they convert to `int` and call `TaskManager` methods.
  - `TaskManager` methods return or print minimal information; side effects are expected (print for errors). Keep modifications consistent with current I/O style.
  - Data structures operate on `Task` objects, not raw tuples. Use `Task(id, start, end, value)` when interacting with trees.

- **Examples of usage (interactive)**:
  - Insert: `InsertTask 1 10 20 5`
  - Delete: `DeleteTask 1`
  - Update: `UpdateTask 1 15 25 7`
  - Query by id: `QueryTaskId 1`
  - Query sum (note: implementation incomplete): `QueryTaskSum 10 20`

- **Files to inspect when making changes**:
  - `main.py` — CLI loop and wiring
  - `src/controller.py` — argument parsing and dispatch table
  - `src/manager.py` — composition of `BTree` + `IntervalTree`
  - `src/core/BTree.py` and `src/core/intervalTree.py` — algorithms and invariants
  - `src/printer.py` — currently empty; used by contributors for output formatting if needed

- **Known gaps and quirks discovered from source**:
  - `TaskManager.task_sum` is unimplemented (empty). Avoid depending on it until implemented.
  - `TaskManager.display_all` references `self._tree` and `self._tree.traverse()` but the manager stores `self._Btree` and no wrapper `_tree` — watch for naming mistakes when changing traversal logic.
  - `src/printer.py` is empty; printing responsibilities are currently inline in controller/manager.
  - `controller.sum()` has a bug: it indexes `args[2]` while expecting two args; be cautious when editing.

- **Developer workflows (how to run & debug)**:
  - Run the app interactively from the repository root:

    ```bash
    python main.py
    ```

  - The codebase has no test suite or requirements file. Use the interpreter available in your environment (project uses only the standard library and dataclasses).
  - To inspect tree state, call B-Tree `traverse()` or add debug prints to `IntervalTree` nodes.

- **When modifying core data structures**:
  - Preserve API shapes used by `TaskManager` (e.g., `BTree.insert(task)`, `BTree.search(id)`, `IntervalTree.add(task)`, `IntervalTree.search_overlap(start, end)`, `IntervalTree.delete(task)`).
  - If you change `Task` fields, update serialization or any printing code in `controller.py`.

- **Quick heuristics for PRs**:
  - Small fixes: prefer localized edits (controller validation, off-by-one index fixes) and run `python main.py` to smoke-test interactive behavior.
  - Larger changes (data-structure refactor): include migration in `TaskManager` to keep both structures consistent and add unit tests (not present currently) demonstrating invariants.

If anything here is unclear or you want extra detail (examples, tests, or a suggested fix for `task_sum`/`display_all`), tell me which area to expand. 
