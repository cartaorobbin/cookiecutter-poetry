#!/usr/bin/env python
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath: str) -> None:
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath: str) -> None:
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == "__main__":
    if "{{cookiecutter.include_github_actions}}" != "y":
        remove_dir(".github")
    else:
        # Handle workflow cleanup based on publish_to setting
        publish_to = "{{cookiecutter.publish_to}}"

        # Keep only the correct publishing workflow
        if publish_to == "pypi":
            remove_file(".github/workflows/on-release-private-pypi.yml")
            remove_file(".github/workflows/on-release-codeartifact.yml")
            remove_dir(".github/actions/codeartifact-login")
        elif publish_to == "private_pypi":
            remove_file(".github/workflows/on-release-pypi.yml")
            remove_file(".github/workflows/on-release-codeartifact.yml")
            remove_dir(".github/actions/codeartifact-login")
        elif publish_to == "codeartifact":
            remove_file(".github/workflows/on-release-pypi.yml")
            remove_file(".github/workflows/on-release-private-pypi.yml")
        elif publish_to == "none":
            remove_file(".github/workflows/on-release-pypi.yml")
            remove_file(".github/workflows/on-release-private-pypi.yml")
            remove_file(".github/workflows/on-release-codeartifact.yml")
            remove_dir(".github/actions/codeartifact-login")
        else:  # artifactory or unknown
            remove_file(".github/workflows/on-release-pypi.yml")
            remove_file(".github/workflows/on-release-private-pypi.yml")
            remove_file(".github/workflows/on-release-codeartifact.yml")
            remove_dir(".github/actions/codeartifact-login")

    if "{{cookiecutter.mkdocs}}" != "y":
        remove_dir("docs")
        remove_file("mkdocs.yml")

    if "{{cookiecutter.dockerfile}}" != "y":
        remove_file("Dockerfile")

    if "{{cookiecutter.codecov}}" != "y":
        remove_file("codecov.yaml")
        if "{{cookiecutter.include_github_actions}}" == "y":
            remove_file(".github/workflows/validate-codecov-config.yml")

    if "{{cookiecutter.cursor_support}}" != "y":
        remove_dir(".cursor")
