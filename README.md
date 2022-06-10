# Entest
See `examples/example_test.py`.

## Install
Because I do not know how to package with poetry so that something ends up in the bin folder here are some ad-hoc instructions.

#### Just run entest
```
python3 -m entest.cli
```

## Contributing
Please do not fork! Make a pull request and if it is not obviously bad I will merge it.

I would like to change a lot of things structure-wise, but API will stay the same.

## Run tests
```
python3 -m entest.cli tests/onboarding_api/test_happy_path.py --graph
python3 -m entest.cli tests/onboarding_api/test_happy_path.py
python3 -m entest.cli tests/onboarding_api/test_happy_path.py --env env_name
```
