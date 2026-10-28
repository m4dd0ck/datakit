from datetime import date, datetime

import dt_utils


def test_parse_date_reads_iso_string():
    assert dt_utils.parse_date("2026-03-04T05:06:07") == datetime(2026, 3, 4, 5, 6, 7)


def test_parse_date_returns_datetime_unchanged():
    value = datetime(2026, 3, 4, 5, 6)
    assert dt_utils.parse_date(value) is value


def test_parse_date_turns_date_into_midnight_datetime():
    assert dt_utils.parse_date(date(2026, 3, 4)) == datetime(2026, 3, 4)


def test_parse_date_returns_default_for_none():
    fallback = datetime(2000, 1, 1)
    assert dt_utils.parse_date(None, default=fallback) == fallback


def test_parse_date_returns_default_for_unparseable_string():
    assert dt_utils.parse_date("not a date") is None


def test_format_date_uses_given_format():
    assert dt_utils.format_date(date(2026, 3, 4), fmt="%d/%m/%Y") == "04/03/2026"


def test_format_date_returns_default_for_none():
    assert dt_utils.format_date(None, default="n/a") == "n/a"


def test_date_range_includes_both_ends():
    assert dt_utils.date_range(date(2026, 1, 1), date(2026, 1, 3)) == [
        date(2026, 1, 1),
        date(2026, 1, 2),
        date(2026, 1, 3),
    ]


def test_date_range_accepts_datetimes_and_step():
    result = dt_utils.date_range(datetime(2026, 1, 1, 9), datetime(2026, 1, 5, 9), step_days=2)
    assert result == [date(2026, 1, 1), date(2026, 1, 3), date(2026, 1, 5)]


def test_date_range_is_empty_when_end_is_before_start():
    assert dt_utils.date_range(date(2026, 1, 2), date(2026, 1, 1)) == []


def test_start_and_end_of_day_bound_the_same_day():
    value = datetime(2026, 3, 4, 13, 14, 15, 16)
    assert dt_utils.start_of_day(value) == datetime(2026, 3, 4)
    assert dt_utils.end_of_day(value) == datetime(2026, 3, 4, 23, 59, 59, 999999)


def test_is_weekend_is_true_only_for_saturday_and_sunday():
    # 2026-10-23 is a Friday.
    assert not dt_utils.is_weekend(date(2026, 10, 23))
    assert dt_utils.is_weekend(date(2026, 10, 24))
    assert dt_utils.is_weekend(date(2026, 10, 25))


def test_business_days_between_counts_weekdays_inclusive():
    # Friday 2026-10-23 to Monday 2026-10-26: Friday and Monday.
    assert dt_utils.business_days_between(date(2026, 10, 23), date(2026, 10, 26)) == 2


def test_add_business_days_skips_the_weekend():
    assert dt_utils.add_business_days(date(2026, 10, 23), 1) == date(2026, 10, 26)


def test_add_business_days_counts_backwards_for_negative_days():
    assert dt_utils.add_business_days(date(2026, 10, 26), -1) == date(2026, 10, 23)
