# Entest
## God is testing you
Most of the testing frameworks are pretty old and all of them (python or otherwise) treat unit tests as first class citizens.
The ideas of this lib are based on the Testing Trophy. This means that we consider integration tests to be more important.
This lib provides a convenient way to explicitly define dependency relationships between tests. Improves transparency of globally needed assets (think fixtures but better).

For how that would look like practically see `tests/example.py`. This code is referred to in my PyCon talk.
https://www.ganjing.com/video/1fic7807r1p1YVbLCkn4uytkJ1c11c

### Demo
[![asciicast](https://asciinema.org/a/594488.svg)](https://asciinema.org/a/594488)

## Installing
```
pip install entest[all]
```

## Documentation
See `tests/example.py`.

To have a test implicitly depend on all other tests use `run_last` flag. This is the case for teardown of critical resources for example users. To skip these tests use `--skip-teardown` or set `ENTEST_SKIP_TEARDOWN` environment variable.

To have all tests implicitly depend on a given test place it closer to the root of the graph.
Use `setup_setup` to take advantage of `depends_on` default behavior. (i.e. for the first decorated function in a module `TEST_ROOT` is taken do be the previous test)

To have a test depend on another test NOT being run use `without` flag. This is usefull for testing error flows.

## Contributing
Please do not maintain a fork! Make a pull request and if it is not obviously bad I will merge it in a timely manner.

```
python3 -m venv .venv
. .venv/bin/activate
pip install poetry
poetry install
echo "
export PYTHONPATH=$PWD
alias entest="python3 ./entest/cli.py"
" >> .venv/bin/activate
export PYTHONPATH=$PWD
alias entest="python3 ./entest/cli.py"
```

I would like to change a lot of things structure-wise, but API will stay the same. In particular:
- `depends_on` decorator with kwargs `previous`, `run_last` and `without`.
- `STATUS` classificator. I see how it can be misused easily, but I will still ship this footgun.

## Run tests
```
entest --graph
entest
entest --skip-teardown
entest --env env_name tests/example.py --snoop
```

## Roadmap
- Better error output with `stackprinter`.
- Verbose mode that automatically applies `pySnooper` or `cyberbrain`.
- An `init` command that sets up the tests folder with env subfolder.
