# GitHub Actions Workflows

This project uses two GitHub Actions workflows to build and release artifacts:

## 1. Release Workflow (`release.yaml`)

**Purpose**: Create stable, versioned releases

**Trigger**: Push of version tags matching pattern `v*.*.*`
```bash
git tag v1.0.0
git push origin v1.0.0
```

**What it does**:
1. Checks out code
2. Sets up Java 11
3. Builds with Maven
4. Creates GitHub Release with name "Release 1.0.0"
5. Uploads `sap-devops-1.0.0.zip` artifact

**Release Properties**:
- Draft: No (published immediately)
- Prerelease: No (marked as latest)
- Retention: Permanent (all releases kept)

**Example Release**:
- Tag: `v1.0.0`
- Release Name: `Release 1.0.0`
- Artifact: `sap-devops-1.0.0.zip`
- URL: https://github.com/njohnjoel/SAP_Devops/releases/tag/v1.0.0

---

## 2. Snapshot Workflow (`snapshot.yaml`)

**Purpose**: Create development/continuous integration builds

**Trigger**: 
- Push to `main` branch
- Push to `develop` branch
- Manual trigger via `workflow_dispatch`

**What it does**:
1. Checks out code
2. Sets up Java 11
3. Generates timestamp-based version
4. Updates pom.xml version
5. Builds with Maven
6. Creates GitHub Release with name "Snapshot YYYYMMDD-HHMMSS"
7. Uploads `sap-devops-snapshot-YYYYMMDD-HHMMSS.zip` artifact
8. Keeps latest 5 snapshots, deletes older ones

**Release Properties**:
- Draft: No (published immediately)
- Prerelease: Yes (marked as pre-release)
- Retention: Last 5 only (older snapshots auto-deleted)

**Example Release**:
- Tag: `snapshot-20260622-230400`
- Release Name: `Snapshot 20260622-230400`
- Artifact: `sap-devops-snapshot-20260622-230400.zip`
- Status: Pre-release

---

## Workflow Comparison

| Feature | Release | Snapshot |
|---------|---------|----------|
| **Trigger** | Version tags (v*) | Branch push + manual |
| **Branches** | N/A | main, develop |
| **Artifact Name** | sap-devops-{version}.zip | sap-devops-snapshot-{timestamp}.zip |
| **Release Name** | Release 1.0.0 | Snapshot 20260622-230400 |
| **Version Type** | Semantic (X.Y.Z) | Timestamp (YYYYMMDD-HHMMSS) |
| **Draft** | No | No |
| **Prerelease** | No | Yes |
| **Retention** | All | Last 5 |
| **Cleanup** | Never | Auto-delete old |

---

## Version Management

### Release Process
```bash
# 1. Update version in pom.xml
nano pom.xml  # Change version to 1.0.1

# 2. Commit changes
git add pom.xml
git commit -m "Bump version to 1.0.1"

# 3. Create and push tag
git tag v1.0.1
git push origin v1.0.1

# 4. Release workflow triggers automatically
# GitHub Release created: Release 1.0.1
# Artifact: sap-devops-1.0.1.zip
```

### Snapshot Process
```bash
# 1. Make changes and commit to main/develop
git add .
git commit -m "Add new feature"
git push origin main

# 2. Snapshot workflow triggers automatically
# GitHub Release created: Snapshot YYYYMMDD-HHMMSS
# Artifact: sap-devops-snapshot-YYYYMMDD-HHMMSS.zip
# Old snapshots cleaned up (keeps last 5)
```

---

## Using Releases

### Download a Release
```bash
# From release page
# https://github.com/njohnjoel/SAP_Devops/releases

# Or using gh CLI
gh release download v1.0.0 -p "sap-devops-1.0.0.zip"
```

### Install from Release
```bash
# Using the installer script
python3 install_devops.py 1.0.0
```

### View All Releases
```bash
gh release list --repo njohnjoel/SAP_Devops
```

---

## Troubleshooting

### Release Workflow Didn't Trigger
- Check tag format: Must be `v*.*.*` (e.g., `v1.0.0`, not `1.0.0`)
- Verify tag was pushed: `git push origin v1.0.0`
- Check workflow logs: Actions tab → Release workflow

### Snapshot Artifacts Not Uploading
- Check workflow logs for build errors
- Verify Maven is building the zip file
- Ensure gh CLI has proper permissions (GITHUB_TOKEN)

### Old Snapshots Not Deleted
- Check gh CLI cleanup script in snapshot workflow
- Ensure GITHUB_TOKEN has release deletion permissions
- Manual cleanup: Go to releases page and delete manually

---

## Release Page Maintenance

The releases page automatically maintains:
- **All stable releases** under "Releases"
- **Latest snapshot** marked as "Pre-release"
- **Old snapshots** auto-deleted (keeps last 5)

View at: https://github.com/njohnjoel/SAP_Devops/releases
