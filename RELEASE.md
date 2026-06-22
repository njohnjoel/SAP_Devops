# Release Instructions

## Overview
This project uses Maven to build and GitHub Actions to automatically release artifacts to the releases page.

## Version Management
- Version is defined in `pom.xml` as `1.0.0`
- Update version in `pom.xml` before creating a new release tag

## Creating a Release

### Step 1: Update Version (if needed)
Edit `pom.xml` and change the version:
```xml
<version>1.0.1</version>
```

### Step 2: Create Git Tag
```bash
git tag v1.0.1
git push origin v1.0.1
```

### Step 3: GitHub Actions
- Workflow is automatically triggered on tag push
- Builds the project with Maven
- Creates a GitHub Release
- Uploads the `sap-devops-1.0.1.zip` artifact

## Build Output
- Artifact: `target/sap-devops-1.0.0.zip`
- Contents: 
  - All Python source files from `src/`
  - README.md
  - LICENSE
  - pom.xml
  - .gitignore

## Manual Build (Local)
```bash
mvn clean package
```

The zip file will be created in the `target/` directory.
