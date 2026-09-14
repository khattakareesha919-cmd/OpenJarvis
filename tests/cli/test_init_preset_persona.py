"""Tests for what ``jarvis init --preset`` leaves on disk.

A preset that names a persona is only half installed without the persona
file it names, and a config directory with no SOUL.md falls back to a stock
introduction that has nothing to do with the preset. Both used to happen
silently, so both are pinned here.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from openjarvis.cli.init_cmd import init


@pytest.fixture
def home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    config_dir = tmp_path / ".openjarvis"
    config_path = config_dir / "config.toml"
    monkeypatch.setattr("openjarvis.cli.init_cmd.DEFAULT_CONFIG_DIR", config_dir)
    monkeypatch.setattr("openjarvis.cli.init_cmd.DEFAULT_CONFIG_PATH", config_path)
    monkeypatch.setattr("openjarvis.core.config.DEFAULT_CONFIG_DIR", config_dir)
    monkeypatch.setattr("openjarvis.core.config.DEFAULT_CONFIG_PATH", config_path)
    return config_dir


def _install(preset: str) -> None:
    result = CliRunner().invoke(
        init, ["--preset", preset, "--force"], obj={"quiet": True}
    )
    assert result.exit_code == 0, result.output


class TestPresetPersona:
    def test_aston_preset_installs_the_persona_it_names(self, home: Path) -> None:
        _install("aston")

        persona = home / "prompts" / "personas" / "aston.md"
        assert persona.exists(), "preset names persona 'aston' but never installed it"
        assert "You are Aston" in persona.read_text(encoding="utf-8")

    def test_morning_digest_preset_installs_its_persona_too(self, home: Path) -> None:
        # The fix is not Aston-specific: the three shipped digest presets all
        # name 'jarvis' and had the same gap.
        _install("morning-digest-minimal")

        personas = home / "prompts" / "personas"
        assert (personas / "jarvis.md").exists()
        # The default is installed alongside it, not instead of it.
        assert (personas / "aston.md").exists()

    def test_aston_is_installed_even_when_a_preset_names_no_persona(
        self, home: Path
    ) -> None:
        # digest.persona defaults to "aston", so aston.md has to be on disk
        # whether or not the chosen preset asked for it.
        _install("chat-simple")

        assert (home / "prompts" / "personas" / "aston.md").exists()

    def test_preset_seeds_the_memory_files(self, home: Path) -> None:
        # The preset branch returns early, well before the seeding the normal
        # path does, so it used to leave no SOUL.md at all.
        _install("aston")

        assert (home / "MEMORY.md").exists()
        assert (home / "USER.md").exists()
        assert "You are Aston" in (home / "SOUL.md").read_text(encoding="utf-8")

    def test_aston_speaks_to_a_ma_am(self, home: Path) -> None:
        _install("aston")

        config = (home / "config.toml").read_text(encoding="utf-8")
        assert 'honorific = "ma\'am"' in config
        assert 'persona = "aston"' in config
