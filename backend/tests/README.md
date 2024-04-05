# Testing the backend

To run every tests:

`pytest`

To run tests of a specific file:

`pytest -q tests/test_api.py`

## Running with coverage

Install coverage

`pip install coverage`

Run with coverage

`coverage run - m pytest`

If you want to see it in a more userfriendly way which is via html, then run this code afterwards, so the coverage is saved in a file called "index.html":

`coverage html`

