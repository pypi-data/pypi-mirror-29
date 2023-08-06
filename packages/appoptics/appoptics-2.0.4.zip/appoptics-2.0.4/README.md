[![Build Status](https://travis-ci.com/librato/python-appoptics.svg?token=hJPGuB4cPyioy5R8LBV9&branch=ci)](https://travis-ci.com/librato/python-appoptics)

# python-appoptics

The 'appoptics' module provides automatic instrumentation and metrics/tracing SDK hooks for use with [AppOptics](https://appoptics.com).

The appoptics module provides middleware and other instrumentation for popular web frameworks such as Django, Tornado, Pyramid, and WSGI, as well as commonly used libraries like SQLAlchemy, httplib, redis, memcached.  Read more at [our full documentation](https://docs.appoptics.com/kb/apm_tracing/python/).


## Installing

The Python instrumentation for AppOptics uses a module named `appoptics`, which is distributed via pypi.

```sh
pip install appoptics
```

Alternately, you can use this repository to build a local copy.

## Configuring

See our documentation on [configuring AppOptics for python](https://docs.appoptics.com/kb/apm_tracing/python/configure/).

# Upgrading

To upgrade an existing installation, you simply need to run:

```sh
pip install appoptics --upgrade
```

## Running the Tests

### Test dependencies

The test suite depends on the presence of several database and cache servers; consequently, the easiest way to get up and running is to use the included Dockerfile and `run_docker_dev.sh`.

To build the development container image:
```
docker build -f Dockerfile -t ptdev:py27 .
```

Then run an interactive shell to run test suite:
```
./run_docker_dev.sh
```

To run tests, in the container's shell, against the current version of Python:
````sh
./run_tests.sh
```

### Test directory layout

Tests in test/unit are actually functional tests; naming is for historic
reasons.  Tests in test/manual are for manual verification of certain
behaviors.

## Support

If you find a bug or would like to request an enhancement, feel free to file
an issue. For all other support requests, please email support@appoptics.com.

## Contributing

You are obviously a person of great sense and intelligence. We happily
appreciate all contributions to the appoptics module whether it is documentation,
a bug fix, new instrumentation for a library or framework or anything else
we haven't thought of.

We welcome you to send us PRs. We also humbly request that any new
instrumentation submissions have corresponding tests that accompany
them. This way we don't break any of your additions when we (and others)
make changes after the fact.

## Developer Resources

We have made a large effort to expose as much technical information
as possible to assist developers wishing to contribute to the AppOptics module.
Below are the three major sources for information and help for developers:

* The [AppOptics Knowledge Base](https://docs.appoptics.com/)
has a large collection of technical articles or, if needed, you can submit a
support request directly to the team.

If you have any questions or ideas, don't hesitate to contact us anytime.

To see the code related to the C++ extension, take a look in `appoptics/swig`.

## License

Copyright (c) 2017 SolarWinds, LLC

Released under the [Librato Open License](http://docs.appoptics.com/Instrumentation/librato-open-license.html)
