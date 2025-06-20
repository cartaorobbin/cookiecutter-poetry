# Cursor Support Integration Plan

## Overview
Add Cursor IDE support as an optional feature to the cookiecutter-poetry template. When enabled, this will create a `.cursor/rules` directory structure with development guidelines and rules specific to the generated project.

## Task List

### 1. Configuration Setup
- [x] **Update cookiecutter.json**
  - Add new configuration option: `"cursor_support": ["y", "n"]`
  - Position it appropriately among other optional features

### 2. Template Structure Creation
- [x] **Create .cursor directory in template**
  - Create `{{cookiecutter.project_name}}/.cursor/` directory
  - Create `{{cookiecutter.project_name}}/.cursor/rules/` subdirectory

### 3. Development Rules File
- [x] **Create development.mdc template**
  - Create `{{cookiecutter.project_name}}/.cursor/rules/development.mdc`
  - Include comprehensive development rules covering:
    - **Core Development Principles** (Plan Before Coding ⭐, Task Management with Planning Files ⭐)
    - Code style and formatting guidelines
    - Poetry-specific workflows
    - Testing conventions
    - Documentation standards
    - Git workflow rules
    - Project structure guidelines
    - Dependencies management rules
    - Planning directory structure and workflow
  - Use cookiecutter variables where appropriate (project name, etc.)

### 4. Conditional Logic Implementation
- [x] **Update post_gen_project.py hook**
  - Add logic to remove `.cursor` directory when `cursor_support != "y"`
  - Follow existing pattern used for other optional features
  - Ensure proper cleanup of the entire `.cursor` directory structure

### 5. Documentation Updates
- [x] **Update README.md**
  - Add description of the new `cursor_support` option
  - Explain what gets created when Cursor support is enabled
  - Add section about Cursor IDE integration benefits

### 6. Testing
- [x] **Test the new Cursor feature**
  - Test cookiecutter generation with `cursor_support: "y"`
  - Test cookiecutter generation with `cursor_support: "n"`
  - Verify `.cursor` directory is created/removed correctly
  - Verify `development.mdc` content is properly templated
- [x] **Test devcontainer for cookiecutter development**
  - Test devcontainer builds successfully
  - Test development workflow inside devcontainer
  - Verify all development tools work correctly

### 7. Integration Validation
- [x] **Ensure Cursor feature compatibility**
  - Verify the new cursor_support option doesn't conflict with existing features
  - Test with various combinations of other options (dockerfile, mkdocs, codecov, etc.)
  - Ensure proper behavior in CI/CD workflows

### 8. Devcontainer for Cookiecutter Development
- [x] **Create devcontainer for cookiecutter-poetry development**
  - Create `.devcontainer/devcontainer.json` in the root of the cookiecutter-poetry repository
  - Configure Python environment with Poetry
  - Include all necessary development tools (pytest, black, ruff, mypy, etc.)
  - Add pre-commit hooks configuration
  - Include cookiecutter and testing dependencies
- [x] **Enhance development experience**
  - Add VS Code extensions for Python development
  - Configure debugging settings
  - Set up proper environment variables
  - Include documentation tools (MkDocs, etc.)
- [x] **Update development documentation**
  - Add instructions for using devcontainer for development
  - Update CONTRIBUTING.md with devcontainer workflow
  - Document how to test cookiecutter generation inside devcontainer

### 9. Cursor Rules for Cookiecutter-Poetry Development
- [x] **Create Cursor development rules for this project**
  - Create `.cursor/rules/cookiecutter-development.mdc` for cookiecutter-poetry development
  - Include Core Development Principles (Plan Before Coding ⭐, Task Management ⭐)
  - Document cookiecutter-specific development workflows
  - Include testing guidelines for template development
  - Document devcontainer usage and common commands
  - Provide troubleshooting guides for template development

## Implementation Notes

### File Structure After Implementation:

**Cookiecutter-poetry repository structure:**
```
cookiecutter-poetry/
├── .devcontainer/              # NEW: For developing cookiecutter-poetry itself
│   └── devcontainer.json      # Devcontainer configuration for development
├── {{cookiecutter.project_name}}/
│   ├── .cursor/               # Created when cursor_support == "y"
│   │   └── rules/
│   │       └── development.mdc # Cursor development rules with Core Development Principles
│   └── ... (existing template structure)
├── ... (existing cookiecutter structure)
```

**Generated project structure (when cursor_support == "y"):**
```
{{cookiecutter.project_name}}/
├── .cursor/                    # Created when cursor_support == "y"
│   └── rules/
│       └── development.mdc     # Cursor development rules with Core Development Principles
├── planning/                   # Recommended directory structure for task management
│   ├── general.md             # Current active tasks (1-3 task groups max)
│   ├── backlog.md            # Future planned tasks
│   └── done.md               # Completed tasks archive
├── ... (existing structure)
```

### Key Considerations:
1. The `.cursor/rules/development.mdc` file should be comprehensive but project-agnostic
2. Use cookiecutter templating for project-specific content (project name, etc.)
3. Follow existing patterns in the codebase for conditional feature implementation
4. Ensure the features are well-documented for users
5. Consider what development rules would be most valuable for Poetry-based projects
6. **Include Core Development Principles**: Emphasize planning before coding and task management workflows
7. **Planning directory structure**: Include guidelines for using `planning/` directory with `general.md`, `backlog.md`, and `done.md` files
8. **Devcontainer for cookiecutter development**: Ensure devcontainer makes it easy to develop the cookiecutter-poetry project itself
9. **Development tool consistency**: Include all tools needed for cookiecutter development (Poetry, pytest, cookiecutter, etc.)
10. **Performance considerations**: Devcontainer should include all necessary development tools without being bloated

### Dependencies:
- No additional dependencies required
- Uses existing cookiecutter templating mechanisms
- Leverages existing post-generation hook infrastructure

## Review Criteria:
- [x] Cursor support configuration option works correctly
- [x] Generated `.cursor/rules/development.mdc` contains useful, project-relevant rules
- [x] Devcontainer for cookiecutter-poetry development is properly set up and functional
- [x] Documentation is clear and complete for both features
- [x] No regression in existing functionality
- [x] Follows established patterns in the codebase
- [x] Devcontainer includes all necessary tools for developing cookiecutter-poetry
- [x] Performance of devcontainer is acceptable (reasonable build time and resource usage)
- [x] Development workflow inside devcontainer is smooth and efficient

## New Task: GitHub Actions Testing

### 10. GitHub Actions Testing Strategy
- [x] **Test Main Repository Workflows**
  - Test `main.yml` workflow with PR and push triggers
  - Verify quality checks (pre-commit, deptry, poetry lock consistency)
  - Test tox matrix across Python versions (3.8, 3.9, 3.10, 3.11)
  - Verify codecov integration works
  - Test MkDocs documentation building
- [x] **Test Template GitHub Actions**
  - Generate test projects with various configurations ✅
  - Test template workflows run successfully in generated projects ❌ **YAML Issues Found**
  - Verify conditional workflows (codecov, mkdocs) work correctly ✅
  - Test publishing workflows with dry-run configurations ❌ **Template Inheritance Issues**
- [x] **Test Custom GitHub Actions**
  - Verify `setup-poetry-env` action works correctly ✅
  - Test Python version matrix compatibility ✅
  - Test caching mechanisms work properly ✅

### ✅ **COMPLETED: GitHub Actions Template Issues FIXED!**
- [x] **Fix YAML Indentation in Template Inheritance**
  - [x] Fix `{{cookiecutter.project_name}}/.github/workflows/on-release-private-pypi.yml`
  - [x] Fix `{{cookiecutter.project_name}}/.github/workflows/on-release-codeartifact.yml` 
  - [x] Fix `{{cookiecutter.project_name}}/.github/workflows/on-release-pypi.yml`
  - [x] Replace problematic template inheritance with standalone workflow files
  - [x] Fix post-generation hook logic for workflow cleanup
- [x] **Test Fixed Templates** 
  - [x] Re-run `./test_generated_actions.sh` to verify fixes ✅ ALL TESTS PASSING!
  - [x] Validate YAML syntax across all workflow combinations ✅
  - [x] Test conditional features (codecov, mkdocs) ✅
  - [x] Test publishing workflow configurations ✅

### 11. GitHub Actions Testing Implementation
- [x] **Create testing procedures**
  - [x] Document how to test workflows locally with act ✅
  - [x] Create comprehensive pytest test suite ✅ `tests/test_github_actions.py`
  - [x] Set up workflow testing validation ✅
  - [x] Replace bash script with maintainable pytest tests ✅
- [x] **Validate workflow compatibility**
  - [x] Test with different cookiecutter option combinations ✅
  - [x] Verify workflows work with latest GitHub Actions versions ✅
  - [x] Test security and permissions ✅
  - [x] Test conditional features (codecov, mkdocs) ✅
  - [x] Test publishing workflow selection and cleanup ✅
- [ ] **Advanced testing (Optional)**
  - [ ] Install `act` and test workflows locally
  - [ ] Create real GitHub test repository for live CI validation
  - [ ] Performance monitoring and reliability testing
  - [ ] Test with different Python versions and OS matrices

## 🎯 **Next Development Priorities**

### 12. Advanced GitHub Actions Features
- [ ] **Enhanced Security Features**
  - Add dependency review workflow
  - Add security scanning (CodeQL, Dependabot)
  - Implement proper secrets management examples
- [ ] **Performance Optimizations**
  - Optimize caching strategies across workflows
  - Add parallel job execution where possible
  - Minimize workflow execution time
- [ ] **Advanced Publishing Options**
  - Add support for GitHub Packages
  - Add Docker image publishing (when dockerfile=y)
  - Add pre-release and beta publishing workflows

### 13. Template Enhancement Opportunities  
- [ ] **Additional Optional Features**
  - Add support for Jupyter notebooks
  - Add support for CLI applications (Click/Typer)
  - Add database integration options (SQLAlchemy, etc.)
- [ ] **Development Experience Improvements**
  - Enhanced VS Code settings and extensions
  - Pre-configured debugging setups
  - Better task automation (more Makefile targets)
- [ ] **Documentation Enhancements**
  - Auto-generated API documentation
  - Enhanced README templates
  - Contributing guidelines templates

### 14. Quality Assurance Expansion
- [ ] **Extended Testing Framework**
  - Integration testing examples
  - Performance testing setups
  - Security testing automation
- [ ] **Code Quality Tools**
  - Additional linting tools (bandit, safety)
  - Type checking enhancements
  - Code complexity analysis 