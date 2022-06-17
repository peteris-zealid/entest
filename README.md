# Entest
See `tests/example.py`.

To have a test implicitly depend on all other tests use `run_last` flag. This is the case for teardown of critical resources for example users. To skip these tests use `--skip-teardown` or set `ENTEST_SKIP_TEARDOWN` environment variable.

To have all tests implicitly depend on a given test place it closer to the root of the graph.
Use `setup_setup` to take advantage of `depends_on` default behavior. (i.e. for the first decorated function in a module `TEST_ROOT` is taken do be the previous test)

To have a test depend on another test NOT being run use `without` flag. This is usefull for testing error flows.

Optionally install `rich` for nicer output.

## Contributing
Please do not maintain a fork! Make a pull request and if it is not obviously bad I will merge it in a timely manner.

I would like to change a lot of things structure-wise, but API will stay the same. In particular:
- `depends_on` decorator with kwargs `previous`, `run_last` and `without`.
- `STATUS` classificator. I see how it can be misused easily, but I will still ship this footgun.

## Run tests
```
entest --graph
entest
entest --skip-teardown
entest --env env_name tests/spam_users.py
```
