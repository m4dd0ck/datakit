import gc
import os

from openpyxl import Workbook

import excel_utils


def count_open_files() -> int:
    return len(os.listdir("/dev/fd"))


def test_read_excel_closes_the_workbook_when_the_sheet_is_empty(tmp_path):
    path = tmp_path / "empty.xlsx"
    Workbook().save(path)

    # Reason: the workbook sits in a reference cycle, so only an explicit close (not
    # refcounting) frees its file handle while the cyclic collector is paused.
    gc.disable()
    try:
        before = count_open_files()
        assert excel_utils.read_excel(path) == []
        after = count_open_files()
    finally:
        gc.enable()

    assert after == before
