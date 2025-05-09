.PHONY: install
install: ## Install the poetry environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install	
	@ poetry run pre-commit install
	@poetry shell


.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock"
	@poetry lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy
{%- if cookiecutter.deptry == 'y' %}
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run deptry .
{%- endif %}

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
{%- if cookiecutter.codecov == "y"%}
	@poetry run pytest --cov --cov-config=pyproject.toml --cov-report=xml
{%- else %}
	@poetry run pytest --doctest-modules
{%- endif%}

.PHONY: build
build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean-build
clean-build: ## clean build artifacts
	@rm -rf dist

{%- if cookiecutter.publish_to in ["pypi", "private_pypi"] %}

.PHONY: publish
publish: ## publish a release to pypi.
	@echo "🚀 Publishing: Dry run."
	{% if cookiecutter.publish_to == "pypi" -%}
	@poetry config pypi-token.pypi $(PYPI_TOKEN)
	{%- elif cookiecutter.publish_to == "private_pypi" -%}
	@poetry config repositories.private $(PRIVATE_PYPI_URL)
	@poetry config http-basic.private $(PRIVATE_PYPI_USERNAME) $(PRIVATE_PYPI_PASSWORD)
	{%- endif %}
	@poetry publish --dry-run
	@echo "🚀 Publishing."
	{% if cookiecutter.publish_to == "pypi" -%}
	@poetry publish
	{%- elif cookiecutter.publish_to == "private_pypi" -%}
	@poetry publish --repository private
	{%- endif %}

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.
{%- elif cookiecutter.publish_to == "artifactory" %}

.PHONY: publish
publish: ## Publish to the Artifactory repository using poetry. Requires ARTIFACTORY_TOKEN for DPS-FF-ILO to be set.
	@echo "🚀 Publishing: Dry run."
	@poetry config repositories.artifactory $(ARTIFACTORY_URL)
	@poetry publish --repository artifactory --username $(ARTIFACTORY_USERNAME) --password $(ARTIFACTORY_PASSWORD) --dry-run
	@echo "🚀 Publishing."
	@poetry publish --repository artifactory --username $(ARTIFACTORY_USERNAME) --password $(ARTIFACTORY_PASSWORD)

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.
{%- endif%}

{%- if cookiecutter.mkdocs == "y" %}

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@poetry run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@poetry run mkdocs serve

{%- endif %}

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help