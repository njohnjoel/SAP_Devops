# Workflow Fixes - Error 403 Resolution

## Problem
Workflows were failing with:
```
Error 403: Resource not accessible by integration
```

This happens when GitHub Actions doesn't have permission to create releases.

## Fixes Applied

### 1. Added Permissions to Workflows ✅
Both `release.yaml` and `snapshot.yaml` now include:
```yaml
permissions:
  contents: write
```

This grants `GITHUB_TOKEN` the necessary permissions to:
- Create releases
- Upload artifacts
- Delete old releases (cleanup)

### 2. Updated Action Versions ✅
Changed from deprecated v3 to current v4:
```yaml
# Before
- uses: actions/checkout@v3
- uses: actions/setup-java@v3

# After
- uses: actions/checkout@v4
- uses: actions/setup-java@v4
```

Fixes Node.js 20 deprecation warnings.

### 3. Fixed Parameter Typo ✅
Fixed in snapshot.yaml:
```yaml
# Before (incorrect)
updateOnlyUnrelease: false

# After (correct)
updateOnlyUnreleased: false
```

## Repository Configuration

For workflows to have full write permissions, ensure your repository settings are configured:

1. Go to: **Settings → Actions → General**
2. Under "Workflow permissions", select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**

3. Click **Save**

## Verification

To verify the fixes work:

### Test Release Workflow
```bash
# Create a version tag
git tag v1.0.0
git push origin v1.0.0

# Monitor: Actions tab → Release workflow
# Expected: Release created successfully
```

### Test Snapshot Workflow
```bash
# Commit to main branch
git commit -m "Test snapshot"
git push origin main

# Or trigger manually:
# Actions tab → Snapshot → Run workflow

# Monitor: Actions tab → Snapshot workflow
# Expected: Snapshot pre-release created successfully
```

## Artifacts Expected

After fixes are applied:

**Release Workflow:**
- Release tag: `v1.0.0`
- Release name: `Release 1.0.0`
- Artifact: `sap-devops-1.0.0.zip`
- Type: Stable release

**Snapshot Workflow:**
- Release tag: `snapshot-20260622-230400`
- Release name: `Snapshot 20260622-230400`
- Artifact: `sap-devops-snapshot-20260622-230400.zip`
- Type: Pre-release

## Files Modified

```
.github/workflows/release.yaml
- Added permissions: contents: write
- Updated checkout@v3 → v4
- Updated setup-java@v3 → v4

.github/workflows/snapshot.yaml
- Added permissions: contents: write
- Updated checkout@v3 → v4
- Updated setup-java@v3 → v4
- Fixed updateOnlyUnrelease → updateOnlyUnreleased
```

## If Issues Persist

1. Check repository has correct workflow permissions (Read and write)
2. Verify GITHUB_TOKEN is not restricted
3. Check Actions logs for detailed error messages
4. Ensure tags follow correct format (v*.*.* for release)

## Related Documentation

- [WORKFLOWS.md](./WORKFLOWS.md) - Workflow usage guide
- [RELEASE.md](./RELEASE.md) - Release management guide
- [INSTALL.md](./INSTALL.md) - Installation script guide
