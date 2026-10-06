import pytest

from dwrap import main


@pytest.fixture
def cd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_wraps_file_in_directory_named_without_extension(cd):
    (cd / "movie.mkv").write_text("x")
    assert main(["movie.mkv"]) == 0
    assert (cd / "movie" / "movie.mkv").read_text() == "x"


def test_preserve_extensions(cd):
    (cd / "movie.mkv").write_text("x")
    assert main(["--preserve-extensions", "movie.mkv"]) == 0
    assert (cd / "movie.mkv" / "movie.mkv").read_text() == "x"
    assert (cd / "movie.mkv").is_dir()


def test_parenthesised_name(cd):
    (cd / "movie (2001).mkv").write_text("x")
    main(["movie (2001).mkv"])
    assert (cd / "movie (2001)" / "movie (2001).mkv").read_text() == "x"
    assert not (cd / "movie (2001).mkv").exists()


def test_directories_are_ignored(cd):
    (cd / "already").mkdir()
    (cd / "already" / "f.mkv").write_text("x")
    assert main(["already"]) == 0
    assert [p.name for p in (cd / "already").iterdir()] == ["f.mkv"]


def test_dry_run_changes_nothing(cd, capsys):
    (cd / "a.mkv").write_text("x")
    main(["--dry-run", "a.mkv"])
    assert (cd / "a.mkv").is_file()
    assert not (cd / "a").exists()
    assert "a.mkv -> a/a.mkv" in capsys.readouterr().out


def test_clash_with_existing_directory_is_numbered(cd, capsys):
    (cd / "a").mkdir()
    (cd / "a.mkv").write_text("x")
    main(["a.mkv"])
    assert (cd / "a (1)" / "a.mkv").read_text() == "x"
    assert "warning" in capsys.readouterr().err


def test_clash_numbering_continues(cd):
    (cd / "a").mkdir()
    (cd / "a (1)").mkdir()
    (cd / "a.mkv").write_text("x")
    main(["a.mkv"])
    assert (cd / "a (2)" / "a.mkv").exists()


def test_clash_between_items_in_same_run(cd):
    (cd / "a.mkv").write_text("1")
    (cd / "a.mp4").write_text("2")
    main(["a.mkv", "a.mp4"])
    assert (cd / "a" / "a.mkv").read_text() == "1"
    assert (cd / "a (1)" / "a.mp4").read_text() == "2"


def test_dry_run_simulates_clash_between_items(cd, capsys):
    (cd / "a.mkv").write_text("1")
    (cd / "a.mp4").write_text("2")
    main(["--dry-run", "a.mkv", "a.mp4"])
    assert "a.mp4 -> a (1)/a.mp4" in capsys.readouterr().out


def test_missing_path_reports_error_and_continues(cd, capsys):
    (cd / "a.mkv").write_text("x")
    assert main(["nope", "a.mkv"]) == 1
    assert (cd / "a.mkv" / "a.mkv").exists()
    assert "nope" in capsys.readouterr().err


def test_files_in_subdirectories(cd):
    (cd / "sub").mkdir()
    (cd / "sub" / "m.mkv").write_text("x")
    main(["sub/m.mkv"])
    assert (cd / "sub" / "m" / "m.mkv").read_text() == "x"


def test_no_temp_dirs_left_behind(cd):
    (cd / "a.mkv").write_text("x")
    main(["--preserve-extensions", "a.mkv"])
    assert [p.name for p in cd.iterdir()] == ["a.mkv"]
