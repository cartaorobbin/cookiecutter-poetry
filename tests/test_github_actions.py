"""
GitHub Actions workflow tests for cookiecutter-poetry generated projects.

This module replaces the test_generated_actions.sh script with proper pytest tests
that validate GitHub Actions workflows in generated projects.
"""

import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import List

import pytest
import yaml


@contextmanager
def run_within_dir(path: str):
    """Context manager to run code within a specific directory."""
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def file_contains_text(file: str, text: str) -> bool:
    """Check if a file contains specific text."""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return text in f.read()
    except FileNotFoundError:
        return False


def validate_yaml_file(file_path: str) -> bool:
    """Validate that a file contains valid YAML syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return True
    except (yaml.YAMLError, FileNotFoundError):
        return False


def validate_toml_file(file_path: str) -> bool:
    """Validate that a file contains valid TOML syntax."""
    try:
        # Try multiple ways to validate TOML
        try:
            import tomllib
            with open(file_path, 'rb') as f:
                tomllib.load(f)
            return True
        except ImportError:
            pass

        try:
            import tomli
            with open(file_path, 'rb') as f:
                tomli.load(f)
            return True
        except ImportError:
            pass

        # Fallback to poetry check if available
        with run_within_dir(os.path.dirname(file_path)):
            result = subprocess.run(['poetry', 'check'],
                                    capture_output=True, text=True)
            return result.returncode == 0

    except Exception:
        return False


class TestWorkflowFiles:
    """Test GitHub Actions workflow files."""

    def _get_workflows_dir(self, project_path: Path) -> Path:
        """Get the .github/workflows directory path."""
        return project_path / ".github" / "workflows"

    def _get_workflow_files(self, project_path: Path) -> List[Path]:
        """Get all workflow files in the project."""
        workflows_dir = self._get_workflows_dir(project_path)
        if not workflows_dir.exists():
            return []
        return list(workflows_dir.glob("*.yml"))

    def test_workflow_files_exist(self, cookies, tmp_path):
        """Test that required workflow files exist."""
        with run_within_dir(tmp_path):
            result = cookies.bake(
                extra_context={"project_name": "test-workflows"})

            workflows_dir = self._get_workflows_dir(result.project_path)
            assert workflows_dir.exists(), ".github/workflows directory should exist"

            # Check that main workflow exists
            main_workflow = workflows_dir / "on-release-main.yml"
            assert main_workflow.exists(), "on-release-main.yml should exist"

    def test_workflow_yaml_syntax(self, cookies, tmp_path):
        """Test that all workflow files contain valid YAML."""
        with run_within_dir(tmp_path):
            result = cookies.bake(
                extra_context={"project_name": "test-yaml-syntax"})

            workflow_files = self._get_workflow_files(result.project_path)
            assert len(
                workflow_files) > 0, "Should have at least one workflow file"

            for workflow_file in workflow_files:
                assert validate_yaml_file(str(workflow_file)), \
                    f"Invalid YAML in {workflow_file.name}"

    @pytest.mark.parametrize("publish_to,expected_workflow", [
        ("pypi", "on-release-pypi.yml"),
        ("private_pypi", "on-release-private-pypi.yml"),
        ("codeartifact", "on-release-codeartifact.yml"),
    ])
    def test_publishing_workflow_selection(self, cookies, tmp_path, publish_to, expected_workflow):
        """Test that correct publishing workflow is included based on publish_to setting."""
        with run_within_dir(tmp_path):
            # Use valid project name (no underscores)
            project_name = f"test-{publish_to.replace('_', '-')}"
            result = cookies.bake(extra_context={
                "project_name": project_name,
                "publish_to": publish_to
            })

            workflows_dir = self._get_workflows_dir(result.project_path)
            expected_file = workflows_dir / expected_workflow

            assert expected_file.exists(), \
                f"{expected_workflow} should exist for publish_to={publish_to}"

    def test_workflow_cleanup_logic(self, cookies, tmp_path):
        """Test that incorrect publishing workflows are removed."""
        with run_within_dir(tmp_path):
            # Test PyPI project doesn't have other publishing workflows
            result = cookies.bake(extra_context={
                "project_name": "test-pypi-cleanup",
                "publish_to": "pypi"
            })

            workflows_dir = self._get_workflows_dir(result.project_path)

            # Should have PyPI workflow
            assert (workflows_dir / "on-release-pypi.yml").exists()

            # Should NOT have other publishing workflows
            assert not (workflows_dir / "on-release-private-pypi.yml").exists()
            assert not (workflows_dir / "on-release-codeartifact.yml").exists()


class TestConditionalFeatures:
    """Test conditional features in workflows."""

    def test_codecov_integration(self, cookies, tmp_path):
        """Test codecov integration in workflows."""
        # Test with codecov enabled
        with run_within_dir(tmp_path):
            result = cookies.bake(extra_context={
                "project_name": "test-codecov-enabled",
                "codecov": "y"
            })

            main_workflow = result.project_path / ".github" / \
                "workflows" / "on-release-main.yml"
            assert file_contains_text(str(main_workflow), "codecov"), \
                "Codecov integration should be present when enabled"

            # Should have codecov config files
            assert (result.project_path / "codecov.yaml").exists()
            assert (result.project_path / ".github" / "workflows" /
                    "validate-codecov-config.yml").exists()

    def test_codecov_disabled(self, cookies, tmp_path):
        """Test that codecov is properly excluded when disabled."""
        with run_within_dir(tmp_path):
            result = cookies.bake(extra_context={
                "project_name": "test-codecov-disabled",
                "codecov": "n"
            })

            # Should not have codecov files
            assert not (result.project_path / "codecov.yaml").exists()
            assert not (result.project_path / ".github" /
                        "workflows" / "validate-codecov-config.yml").exists()

    def test_mkdocs_integration(self, cookies, tmp_path):
        """Test MkDocs integration in workflows."""
        # Test with mkdocs enabled
        with run_within_dir(tmp_path):
            result = cookies.bake(extra_context={
                "project_name": "test-mkdocs-enabled",
                "mkdocs": "y"
            })

            main_workflow = result.project_path / ".github" / \
                "workflows" / "on-release-main.yml"
            assert file_contains_text(str(main_workflow), "mkdocs"), \
                "MkDocs integration should be present when enabled"

            # Should have docs directory and mkdocs.yml
            assert (result.project_path / "docs").is_dir()
            assert (result.project_path / "mkdocs.yml").exists()

    def test_mkdocs_disabled(self, cookies, tmp_path):
        """Test that MkDocs is properly excluded when disabled."""
        with run_within_dir(tmp_path):
            result = cookies.bake(extra_context={
                "project_name": "test-mkdocs-disabled",
                "mkdocs": "n"
            })

            main_workflow = result.project_path / ".github" / \
                "workflows" / "on-release-main.yml"
            assert not file_contains_text(str(main_workflow), "check-docs"), \
                "MkDocs check-docs job should not be present when disabled"

            # Should not have docs directory or mkdocs.yml
            assert not (result.project_path / "docs").exists()
            assert not (result.project_path / "mkdocs.yml").exists()


class TestProjectInitialization:
    """Test that generated projects can be properly initialized."""

    def test_pyproject_toml_validity(self, cookies, tmp_path):
        """Test that generated pyproject.toml files are valid."""
        with run_within_dir(tmp_path):
            result = cookies.bake(
                extra_context={"project_name": "test-pyproject"})

            pyproject_file = result.project_path / "pyproject.toml"
            assert pyproject_file.exists(), "pyproject.toml should exist"
            assert validate_toml_file(str(pyproject_file)), \
                "pyproject.toml should be valid TOML"

    def test_poetry_lock_consistency(self, cookies, tmp_path):
        """Test that Poetry configuration is consistent."""
        with run_within_dir(tmp_path):
            result = cookies.bake(
                extra_context={"project_name": "test-poetry-consistency"})

            with run_within_dir(str(result.project_path)):
                # Initialize git (required for some checks)
                subprocess.run(['git', 'init'], capture_output=True)
                subprocess.run(['git', 'config', 'user.email',
                               'test@example.com'], capture_output=True)
                subprocess.run(['git', 'config', 'user.name',
                               'Test User'], capture_output=True)

                # Check poetry configuration
                result_poetry = subprocess.run(['poetry', 'check'],
                                               capture_output=True, text=True)
                assert result_poetry.returncode == 0, \
                    f"Poetry check failed: {result_poetry.stderr}"


class TestWorkflowSecurity:
    """Test security-related aspects of workflows."""

    def test_workflow_permissions(self, cookies, tmp_path):
        """Test that workflows have appropriate permissions set."""
        with run_within_dir(tmp_path):
            result = cookies.bake(extra_context={
                "project_name": "test-permissions",
                "publish_to": "pypi"
            })

            workflow_file = result.project_path / ".github" / \
                "workflows" / "on-release-pypi.yml"
            assert file_contains_text(str(workflow_file), "permissions:"), \
                "Workflow should have permissions section"
            assert file_contains_text(str(workflow_file), "id-token: write"), \
                "Workflow should have id-token write permission for OIDC"

    def test_secret_references(self, cookies, tmp_path):
        """Test that workflows properly reference secrets."""
        with run_within_dir(tmp_path):
            result = cookies.bake(extra_context={
                "project_name": "test-secrets",
                "publish_to": "pypi"
            })

            workflow_file = result.project_path / ".github" / \
                "workflows" / "on-release-pypi.yml"
            assert file_contains_text(str(workflow_file), "secrets."), \
                "Workflow should reference secrets properly"


class TestIntegrationScenarios:
    """Test complex integration scenarios."""

    def test_full_feature_integration(self, cookies, tmp_path):
        """Test a project with all features enabled."""
        with run_within_dir(tmp_path):
            result = cookies.bake(extra_context={
                "project_name": "test-full-integration",
                "codecov": "y",
                "mkdocs": "y",
                "dockerfile": "y",
                "cursor_support": "y",
                "publish_to": "pypi"
            })

            # Should have all expected files
            assert (result.project_path / ".github" /
                    "workflows" / "on-release-main.yml").exists()
            assert (result.project_path / ".github" /
                    "workflows" / "on-release-pypi.yml").exists()
            assert (result.project_path / "codecov.yaml").exists()
            assert (result.project_path / "docs").is_dir()
            assert (result.project_path / "Dockerfile").exists()
            assert (result.project_path / ".cursor").is_dir()

            # All workflow files should be valid YAML
            workflow_files = list(
                (result.project_path / ".github" / "workflows").glob("*.yml"))
            for workflow_file in workflow_files:
                assert validate_yaml_file(str(workflow_file)), \
                    f"Invalid YAML in {workflow_file.name}"

    def test_minimal_configuration(self, cookies, tmp_path):
        """Test a minimal project configuration."""
        with run_within_dir(tmp_path):
            result = cookies.bake(extra_context={
                "project_name": "test-minimal",
                "codecov": "n",
                "mkdocs": "n",
                "dockerfile": "n",
                "cursor_support": "n",
                "publish_to": "none"
            })

            # Should have minimal set of files
            assert (result.project_path / ".github" /
                    "workflows" / "on-release-main.yml").exists()
            assert not (result.project_path / "codecov.yaml").exists()
            assert not (result.project_path / "docs").exists()
            assert not (result.project_path / "Dockerfile").exists()
            assert not (result.project_path / ".cursor").exists()

            # Workflow should be valid YAML
            main_workflow = result.project_path / ".github" / \
                "workflows" / "on-release-main.yml"
            assert validate_yaml_file(str(main_workflow)), \
                "Main workflow should be valid YAML"


class TestExecutionSummary:
    """Summary tests to validate overall functionality."""

    def test_all_configurations_generate_successfully(self, cookies, tmp_path):
        """Test that all major configuration combinations work."""
        configurations = [
            {"codecov": "y", "mkdocs": "y", "publish_to": "pypi"},
            {"codecov": "n", "mkdocs": "y", "publish_to": "private_pypi"},
            {"codecov": "y", "mkdocs": "n", "publish_to": "codeartifact"},
            {"codecov": "n", "mkdocs": "n", "publish_to": "none"},
        ]

        for i, config in enumerate(configurations):
            with run_within_dir(tmp_path):
                config["project_name"] = f"test-config-{i}"
                result = cookies.bake(extra_context=config)

                assert result.exit_code == 0, \
                    f"Configuration {config} failed: {result.exception}"
                assert result.project_path.is_dir()

                # Validate all workflow files are valid YAML
                workflows_dir = result.project_path / ".github" / "workflows"
                if workflows_dir.exists():
                    for workflow_file in workflows_dir.glob("*.yml"):
                        assert validate_yaml_file(str(workflow_file)), \
                            f"Invalid YAML in {workflow_file.name} for config {config}"
