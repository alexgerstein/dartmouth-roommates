redis-server &

py.test --cov-report term-missing --cov-config .coveragerc --cov . --boxed -n5 tests/

redis-cli shutdown
