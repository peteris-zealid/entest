# Entest
See `examples/example_test.py`.

To have a test implicitly depend on all other tests use `run_last` flag. This is the case for teardown of critical resources for example users.

To have all tests implicitly depend on a given test place it closer to the root of the graph.
Use `setup_setup` to take advantage of `depends_on` default behavior. (i.e. for the first decorated function in a module `TEST_ROOT` is taken do be the previous test)

To have a test depend on another test NOT being run use `without` flag. This is usefull for testing error flows.

## Install
Because I do not know how to package with poetry so that something ends up in the bin folder here are some ad-hoc instructions.

#### Just run entest
```
python3 -m entest.cli
```

#### Create an executable
```
THE_WAY=$(python3 -c "print('''$(which pip)'''.rsplit('p', 2)[0] + 'entest')")
echo '#!/usr/bin/env python3
import entest.cli
entest.cli.main()
' > $THE_WAY
chmod +x $THE_WAY
```

## Contributing
Please do not maintain a fork! Make a pull request and if it is not obviously bad I will merge it in a timely manner.

I would like to change a lot of things structure-wise, but API will stay the same. In particular:
- `depends_on` decorator with kwargs `previous`, `run_last` and `without`.
- `STATUS` classificator. I see how it can be misused easily, but I will still ship this footgun.

## Run tests
```
python3 -m entest.cli tests/onboarding_api/test_happy_path.py --graph
python3 -m entest.cli tests/onboarding_api/test_happy_path.py
python3 -m entest.cli tests/onboarding_api/test_happy_path.py --env env_name
```
