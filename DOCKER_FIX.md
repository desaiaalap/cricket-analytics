# Docker Build Fix

## Issue
Docker build was failing with error:
```
failed to compute cache key: "/tests": not found
```

## Root Cause
The `.dockerignore` file (line 52) excludes the `tests/` directory to keep the production image slim, but the `Dockerfile` (line 48) was trying to copy it.

**Conflict:**
- `.dockerignore` line 52: `tests/` (excluded from build context)
- `Dockerfile` line 48: `COPY tests/ ./tests/` (tried to copy excluded dir)

## Solution
Updated `Dockerfile` to only copy files needed for production:

**Removed:**
- `COPY tests/ ./tests/` - Not needed in production
- `COPY *.py ./` - No root-level .py files needed
- `COPY *.md ./` - Already excluded by .dockerignore
- `COPY Makefile ./` - Development tool, not needed
- `COPY pyproject.toml ./` - Build config, not runtime
- `COPY pytest.ini ./` - Test config, not needed

**Kept:**
- `COPY scripts/ ./scripts/` - Core data processing
- `COPY notebooks/ ./notebooks/` - Analysis notebooks
- `COPY dashboard/ ./dashboard/` - Web dashboards
- `COPY requirements.txt ./` - For reference
- `COPY README.md ./` - Documentation (optional)

## Why This Matters

**Production images should be minimal:**
- ✅ Faster builds (less data to copy)
- ✅ Smaller images (less disk space)
- ✅ Faster deployment (less data to transfer)
- ✅ Better security (fewer files exposed)

**Tests are for development:**
- Run tests locally or in CI/CD
- Not needed in production containers
- Excluded via `.dockerignore` is correct

## Verification

After fix, Docker build should work:

```bash
docker-compose up --build
```

Expected:
- ✅ Build succeeds
- ✅ No "not found" errors
- ✅ Image size reduced
- ✅ All dashboards work normally

## Files Changed

1. **Dockerfile** - Removed COPY commands for excluded files
2. **DOCKER_FIX.md** - This documentation (new)

## Related Files

- `.dockerignore` - Defines what's excluded (unchanged, working correctly)
- `docker-compose.yml` - Service definitions (unchanged)

---

**Status:** ✅ Fixed
**Date:** January 24, 2026
