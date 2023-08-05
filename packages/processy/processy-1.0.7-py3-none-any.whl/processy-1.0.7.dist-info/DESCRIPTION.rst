
# processy

### Description

*Processy* is a wrapper around `Popen` similar to the now built-in `subprocess.run()` function, which was added in Python3.5. Prior to 3.5 there was no simple sane function to run subprocesses. This is why I made *processy*.  The current implementation of `subprocess.run()` still won't let you print and return stdout at the same time. *Processy*  remains useful for that.

### `processy.run()`
```python
def run(
    cmd: Union[list, str],
    verbose: bool = True,
    return_stdout: bool = False,
    raise_err: bool = False,
    **popen_kwargs
) -> CompletedProcess:
    """
    @cmd: The Popen command. If it's a string shlex is used to split it.
    @return_stdout: Returns the output from stdout.
    @verbose: Print the output to stdout if True. If False call runs quite.
    @raise_error: If subprocess return code is not 0.
    """
    # ...
```

### `CompletedProcess`

Since Python3.5 *processy* uses the return object `CompletedProcess` that was added to the subprocess module. It's almost identical to processy's old `ProcResult` object.'

```python
CompletedProcess(
    args: Union[str, list]
    returncode: int
    stdout: Optiona[Union[str, bytes]]
    stderr: Optiona[Union[str, bytes]]
)
```


