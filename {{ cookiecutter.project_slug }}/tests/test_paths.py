from src.utils.paths import (
    project_dir,
    data_dir,
    data_raw_dir,
    data_processed_dir,
    data_interim_dir,
    data_external_dir,
    models_dir,
    notebooks_dir,
    references_dir,
    reports_dir,
    reports_figures_dir,
    config_dir,
)


class TestPaths:
    def test_project_dir_exists(self):
        assert project_dir.exists()

    def test_data_subdirs_return_paths(self):
        for fn in (
            data_dir,
            data_raw_dir,
            data_processed_dir,
            data_interim_dir,
            data_external_dir,
        ):
            path = fn()
            assert path.name  # non-empty path

    def test_models_dir(self):
        assert models_dir().name == "models"

    def test_reports_figures_dir(self):
        path = reports_figures_dir()
        assert "figures" in str(path)

    def test_config_dir(self):
        assert config_dir().name == "config"
