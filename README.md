## Latch Sandbox

This repository contains some examples of Latch DSL patterns.

The workflow is currently loosely based on the template workflow produced with `latch init --template subprocess`.

### Patterns

- [Unit testing a task](https://github.com/msto/latch_sandbox/blob/main/tests/test_sort.py)  
    Use `{task}.task_function` (similar to Airflow's `{task}.function`) to call the task's underlying Python function without invoking the Flyte execution context.

    **Note**: `LatchFile`s may be passed into and out of the tested task, so long as the local path already exists. 

