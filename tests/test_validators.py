import pytest

import validators


@pytest.mark.parametrize("email", ["a@example.com", "first.last+tag@sub.example.org"])
def test_is_valid_email_accepts_addresses(email):
    assert validators.is_valid_email(email)


@pytest.mark.parametrize("email", ["", "no-at-sign", "a@b", "a@example.c", None])
def test_is_valid_email_rejects_malformed_or_empty(email):
    assert not validators.is_valid_email(email)


def test_is_valid_url_requires_http_scheme_by_default():
    assert validators.is_valid_url("https://example.com/path")
    assert not validators.is_valid_url("ftp://example.com")
    assert not validators.is_valid_url("example.com")


def test_is_valid_url_accepts_other_schemes_when_scheme_not_required():
    assert validators.is_valid_url("ftp://example.com", require_scheme=False)


@pytest.mark.parametrize("phone", ["(555) 555-0100", "+1 555 555 0100", "555.555.0100"])
def test_is_valid_phone_accepts_us_formats(phone):
    assert validators.is_valid_phone(phone)


@pytest.mark.parametrize("phone", ["555-0100", "2 555 555 0100", "555-555-01ab", ""])
def test_is_valid_phone_rejects_bad_us_numbers(phone):
    assert not validators.is_valid_phone(phone)


def test_is_valid_phone_uses_length_range_outside_us():
    assert validators.is_valid_phone("0123456", country="DE")
    assert not validators.is_valid_phone("012345", country="DE")


@pytest.mark.parametrize(
    ("zipcode", "country"),
    [("12345", "US"), ("12345-6789", "US"), ("K1A 0B1", "CA"), ("SW1A 1AA", "UK")],
)
def test_is_valid_zip_accepts_country_formats(zipcode, country):
    assert validators.is_valid_zip(zipcode, country)


@pytest.mark.parametrize(("zipcode", "country"), [("1234", "US"), ("123456", "CA"), ("", "US")])
def test_is_valid_zip_rejects_wrong_formats(zipcode, country):
    assert not validators.is_valid_zip(zipcode, country)


def test_is_valid_ssn_accepts_well_formed_number():
    # Reason: a format-valid, made-up number; not a real person's.
    assert validators.is_valid_ssn("123-45-6789")


@pytest.mark.parametrize(
    "ssn",
    ["000-12-3456", "666-12-3456", "900-12-3456", "123-00-6789", "123-45-0000", "123-45-678", ""],
)
def test_is_valid_ssn_rejects_reserved_or_malformed(ssn):
    assert not validators.is_valid_ssn(ssn)


def test_is_valid_credit_card_accepts_luhn_valid_test_number():
    assert validators.is_valid_credit_card("4111 1111 1111 1111")


@pytest.mark.parametrize("number", ["4111 1111 1111 1112", "4111", "4111-1111-1111-111a", ""])
def test_is_valid_credit_card_rejects_bad_checksum_or_length(number):
    assert not validators.is_valid_credit_card(number)


@pytest.mark.parametrize(
    ("value", "expected"), [("x", True), ("  ", False), ("", False), (None, False)]
)
def test_is_not_empty(value, expected):
    assert validators.is_not_empty(value) is expected


def test_is_in_range_is_inclusive_and_open_ended():
    assert validators.is_in_range(5, 5, 10)
    assert validators.is_in_range(10, 5, 10)
    assert not validators.is_in_range(11, 5, 10)
    assert validators.is_in_range(-100, max_val=0)
    assert not validators.is_in_range(1, max_val=0)
