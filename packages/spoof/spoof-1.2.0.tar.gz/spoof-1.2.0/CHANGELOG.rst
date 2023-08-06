
1.2.0 (2018-03-05)
==================

- Refactor `spoof.HTTPUpstreamServer` to be a proper server, instead of
  simply wrapping the socket in the request handler.
- Add support for proxying HTTPS requests through an HTTPS server via
  CONNECT method.
- Add supporting tests

1.1.1 (2018-02-28)
==================

- Deconstruct `spoof.HTTPUpstreamServer.handleRequest` to allow more control
- Add `spoof.HTTPUpstreamServer` to handle proxy requests via CONNECT method
- Add `spoof.HTTPRequestHandler.do_CONNECT` to handle proxy requests
- Add `spoof.SSLContext.createOpenSSLConfig` to create self-signed
  certificates with subjectAlternativeName entries, so they can be trusted
  by `requests`, including IP addresses
- Add tests for new functionality
- Remove test code that disables SSL warnings!
- Change from nose to pytest for running tests
- Reformat code to pass Flake8
- Add `.python-version` pyenv file for testing convenience
- Re-run tests on latest versions of Python

1.0.5 (2018-02-19)
==================

- First public stable release
- Multiple Python version testing via `tox`
