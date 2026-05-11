import pytest
from src.a_maze_ing import read_file, fill_the_dict


REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}

VALID_CONFIG = (
    "WIDTH=20\n"
    "HEIGHT=15\n"
    "ENTRY=0,0\n"
    "EXIT=19,14\n"
    "OUTPUT_FILE=maze.txt\n"
    "PERFECT=True\n"
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def write_config(tmp_path, content: str) -> str:
    """Write content to a temporary config file and return its path."""
    config_file = tmp_path / "config.txt"
    config_file.write_text(content)
    return str(config_file)


# ── read_file ──────────────────────────────────────────────────────────────────

class TestReadFile:

    def test_valid_file_returns_content(self, tmp_path):
        path = write_config(tmp_path, VALID_CONFIG)
        assert read_file(path) == VALID_CONFIG

    def test_missing_file_returns_none(self):
        assert read_file("does_not_exist.txt") is None

    def test_directory_path_returns_none(self, tmp_path):
        assert read_file(str(tmp_path)) is None

    def test_empty_file_returns_empty_string(self, tmp_path):
        path = write_config(tmp_path, "")
        assert read_file(path) == ""

    def test_file_with_comments_returns_full_content(self, tmp_path):
        content = "# this is a comment\n" + VALID_CONFIG
        path = write_config(tmp_path, content)
        result = read_file(path)
        assert result is not None
        assert "# this is a comment" in result


# ── fill_the_dict ──────────────────────────────────────────────────────────────

class TestFillTheDict:

    # --- valid file ---

    def test_valid_config_returns_dict(self):
        assert isinstance(fill_the_dict(VALID_CONFIG), dict)

    def test_valid_config_has_all_required_keys(self):
        result = fill_the_dict(VALID_CONFIG)
        assert result is not None
        assert REQUIRED_KEYS.issubset(result.keys())

    def test_valid_config_correct_values(self):
        result = fill_the_dict(VALID_CONFIG)
        assert result is not None
        assert result["WIDTH"] == "20"
        assert result["HEIGHT"] == "15"
        assert result["ENTRY"] == "0,0"
        assert result["EXIT"] == "19,14"
        assert result["OUTPUT_FILE"] == "maze.txt"
        assert result["PERFECT"] == "True"

    # --- missing keys ---

    def test_missing_one_key_not_in_result(self):
        content = (
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=19,14\n"
            "OUTPUT_FILE=maze.txt\n"
            # PERFECT is missing
        )
        result = fill_the_dict(content)
        assert result is not None
        assert "PERFECT" not in result

    def test_all_keys_missing_returns_empty_dict(self):
        result = fill_the_dict("")
        assert result == {} or result is None

    # --- bad syntax ---

    def test_line_without_equals_returns_none(self):
        content = "WIDTH20\nHEIGHT=15\n"
        assert fill_the_dict(content) is None

    def test_key_only_no_value_returns_none(self):
        # "WIDTH=" splits fine — "WIDTH" alone (no =) does not
        content = "WIDTH\nHEIGHT=15\n"
        assert fill_the_dict(content) is None

    def test_value_containing_equals_is_preserved(self):
        # split("=", 1) keeps "some=file.txt" intact as the value
        content = (
            "WIDTH=20\nHEIGHT=15\nENTRY=0,0\n"
            "EXIT=19,14\nOUTPUT_FILE=some=file.txt\nPERFECT=True\n"
        )
        result = fill_the_dict(content)
        assert result is not None
        assert result["OUTPUT_FILE"] == "some=file.txt"

    # --- comments ---

    def test_comment_lines_are_ignored(self):
        content = "# this is a comment\n" + VALID_CONFIG
        result = fill_the_dict(content)
        assert result is not None
        assert REQUIRED_KEYS.issubset(result.keys())
        assert any(k.startswith("#") for k in result.keys()) is False

    def test_multiple_comments_are_ignored(self):
        content = (
            "# comment 1\n"
            "WIDTH=20\n"
            "# comment 2\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=19,14\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
        )
        result = fill_the_dict(content)
        assert result is not None
        assert REQUIRED_KEYS.issubset(result.keys())

    # --- empty lines ---

    def test_empty_lines_between_keys_are_skipped(self):
        content = (
            "WIDTH=20\n"
            "\n"
            "HEIGHT=15\n"
            "\n"
            "ENTRY=0,0\n"
            "EXIT=19,14\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
        )
        result = fill_the_dict(content)
        assert result is not None
        assert REQUIRED_KEYS.issubset(result.keys())

    def test_trailing_newline_does_not_break_parsing(self):
        # config.txt files typically end with \n
        result = fill_the_dict(VALID_CONFIG)
        assert result is not None
        assert REQUIRED_KEYS.issubset(result.keys())

    def test_only_empty_lines_returns_empty_dict(self):
        result = fill_the_dict("\n\n\n")
        assert result == {} or result is None
