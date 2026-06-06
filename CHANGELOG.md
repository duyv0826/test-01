# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository setup
- Python .gitignore file
- Apache 2.0 License
- CONTRIBUTING.md guidelines

### Changed
- Updated repository description

### Deprecated
- Nothing yet

### Removed
- Nothing yet

### Fixed
- Nothing yet

### Security
- Nothing yet

## [0.1.0] - 2026-06-06

### Added
- Initial repository creation
- Basic project structure
- Main branch setup with README

---

## Legend

- **Added** - for new features
- **Changed** - for changes in existing functionality
- **Deprecated** - for soon-to-be removed features
- **Removed** - for now removed features
- **Fixed** - for any bug fixes
- **Security** - in case of vulnerabilities

## How to Use This Changelog

When making changes to the project:

1. Add your changes under the [Unreleased] section
2. Categorize changes under appropriate headings
3. When releasing a new version:
   - Move items from [Unreleased] to a new version section
   - Update the version number and date
   - Create a git tag for the version

## Release Process

\\\ash
# Update version in relevant files
# Update CHANGELOG.md
# Commit changes
git add .
git commit -m \"Release v0.2.0\"
git tag -a v0.2.0 -m \"Version 0.2.0\"
git push origin main --tags
\\\

---

For more information on how to maintain this changelog, visit:
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)