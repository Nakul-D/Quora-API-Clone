# How to run the tests

>Note : Finish setting up the project before running the tests (Steps documented in the project readme)

- Create a database named **quora-api-test** in postgres
- Use `pytest . -v -s` to run all the tests
- Use `pytest tests\auth_test.py -v -s` to run individual test
