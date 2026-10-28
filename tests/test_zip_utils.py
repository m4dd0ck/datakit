import zipfile

import zip_utils


def test_create_zip_leaves_out_its_own_output_when_inside_the_directory(tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    output = tmp_path / "archive.zip"
    zip_utils.create_zip(output, directory=tmp_path)
    with zipfile.ZipFile(output) as zf:
        assert zf.namelist() == ["a.txt"]
