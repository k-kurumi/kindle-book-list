from .converter import datetime_to_date


def test_datetime_to_date() -> None:
    assert "2022-04-18" == datetime_to_date("2022-04-18T02:58:03+0000")
    assert "" == datetime_to_date("")
