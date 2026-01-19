# 📦 Archived Tests

Historical and deprecated test files preserved for reference.

## 📋 Overview

This directory contains archived tests, deprecated test suites, and historical test data that is no longer actively maintained but preserved for reference and historical analysis.

## 📁 Structure

```
archive/
├── README.md           # This file
└── 2025-12-04/        # Example: Tests archived on 2025-12-04
    └── [archived test files]
```

## 🎯 Purpose

Tests are archived when:

- **Deprecated Features** - Testing functionality that has been removed
- **Superseded Tests** - Replaced by better test implementations
- **Historical Reference** - Preserving test evolution history
- **Migration Records** - Tests from previous testing frameworks
- **Research & Analysis** - Understanding past testing approaches

## 📦 What Gets Archived

### Test Files

- Deprecated unit tests
- Old integration test suites
- Previous validation scripts
- Legacy evaluation configs
- Superseded test frameworks

### Test Data

- Historical test results
- Benchmark data from old versions
- Previous evaluation outputs
- Deprecated test fixtures

### Documentation

- Old testing documentation
- Previous testing strategies
- Historical test plans
- Migration records

## 🚀 Archiving Process

### When to Archive

Archive tests when:

1. **Feature Removed** - The tested feature no longer exists
2. **Test Superseded** - A better test implementation replaces it
3. **Framework Change** - Migrating to new testing framework
4. **Cleanup** - Removing unused or redundant tests
5. **Version Milestone** - Major version changes

### How to Archive

```bash
# Create date-stamped archive directory
ARCHIVE_DATE=$(date +%Y-%m-%d)
mkdir -p testing/archive/$ARCHIVE_DATE

# Move deprecated tests
mv testing/old_test_file.py testing/archive/$ARCHIVE_DATE/

# Add archive note
cat > testing/archive/$ARCHIVE_DATE/README.md << EOF
# Archive: $ARCHIVE_DATE

## Reason for Archival
[Explanation of why these tests were archived]

## Contents
- old_test_file.py - [Description]

## Replacement
[Link to new tests that replace these]

## Context
[Any relevant context or history]
EOF

# Commit archive
git add testing/archive/$ARCHIVE_DATE/
git commit -m "Archive deprecated tests from $ARCHIVE_DATE"
```

## 📊 Archive Organization

### Directory Structure

```
archive/
├── 2024-01-15/
│   ├── README.md                # Why archived
│   ├── test_old_feature.py      # Archived test
│   └── test_legacy_api.py       # Archived test
│
├── 2024-06-20/
│   ├── README.md
│   ├── old_eval_framework/      # Entire framework archived
│   │   ├── eval.py
│   │   └── test_eval.py
│   └── migration_notes.md       # Migration documentation
│
└── 2025-12-04/
    ├── README.md
    └── [current archive]
```

### Archive README Template

```markdown
# Archive: [Date]

## Archival Information

**Date:** [YYYY-MM-DD]
**Archived By:** [Name/Team]
**Reason:** [Brief reason]

## Contents

### Test Files
- `test_file1.py` - [Description, reason for archival]
- `test_file2.py` - [Description, reason for archival]

### Supporting Files
- `fixtures.json` - [Description]
- `config.yaml` - [Description]

## Context

### What These Tests Did
[Explanation of original purpose]

### Why Archived
[Detailed reason for archival]

### What Replaced Them
[Link to new tests or explanation of removal]

## Historical Value

### Lessons Learned
[What we learned from these tests]

### Notable Findings
[Any significant bugs or issues found]

### Performance Metrics
[Historical performance data if relevant]

## Restoration

### If You Need to Restore
```bash
# Copy back from archive
cp testing/archive/[date]/test_file.py testing/[location]/

# Update dependencies and imports
# [Specific instructions]
```

### Known Issues
[Any known problems if attempting to run archived tests]

## References

- Original PR: [link]
- Discussion: [link]
- Related Issues: [links]
```

## 🔍 Accessing Archived Tests

### Browse Archives

```bash
# List all archives
ls -la testing/archive/

# List contents of specific archive
ls -la testing/archive/2025-12-04/

# View archive README
cat testing/archive/2025-12-04/README.md
```

### Search Archives

```bash
# Find specific test
find testing/archive/ -name "test_specific_feature.py"

# Search for tests mentioning a feature
grep -r "feature_name" testing/archive/

# Find archives from a date range
ls testing/archive/ | grep "2024-"
```

### Extract Archived Data

```bash
# Copy specific file from archive
cp testing/archive/2024-06-20/test_old_api.py /tmp/

# Extract entire archive
cp -r testing/archive/2024-06-20/ /tmp/archive-review/

# Compare with current tests
diff testing/archive/2024-06-20/test_feature.py testing/unit/test_feature.py
```

## 📈 Archive Metrics

### Current Archives

| Archive Date | Reason | Files | Size | Notes |
|--------------|--------|-------|------|-------|
| 2025-12-04 | [Reason] | [Count] | [Size] | [Notes] |

### Archive History

```bash
# Count total archives
ls testing/archive/ | wc -l

# Total archived files
find testing/archive/ -type f | wc -l

# Total archive size
du -sh testing/archive/

# Archives per year
ls testing/archive/ | cut -d'-' -f1 | sort | uniq -c
```

## 🔄 Restoration Process

### When to Restore

Restore archived tests if:

1. **Feature Reintroduced** - Bringing back a removed feature
2. **Historical Analysis** - Studying past testing approaches
3. **Bug Investigation** - Checking historical test behavior
4. **Regression Testing** - Comparing current vs. historical tests

### How to Restore

```bash
# 1. Identify the archive
ls testing/archive/2024-06-20/

# 2. Review the archive README
cat testing/archive/2024-06-20/README.md

# 3. Copy files to appropriate location
cp testing/archive/2024-06-20/test_feature.py testing/unit/

# 4. Update imports and dependencies
# Edit test_feature.py as needed

# 5. Run the restored test
pytest testing/unit/test_feature.py -v

# 6. Update if necessary
# Make required changes for current codebase

# 7. Document restoration
git commit -m "Restore test_feature.py from archive (2024-06-20)"
```

## 🎓 Best Practices

### Archive Documentation

✅ **Always Include:**
- Date of archival
- Reason for archival
- What replaced these tests
- How to restore if needed
- Context and history

✅ **Archive Metadata:**
- Original purpose
- Test coverage
- Known issues
- Dependencies
- Related documentation

### Retention Policy

**Keep Archives For:**
- At least 2 years (minimum)
- Longer for major versions
- Indefinitely for critical features
- As long as referenced in documentation

**Can Delete After:**
- 5+ years for minor features
- After multiple major versions
- When storage is constrained
- With team consensus

### Regular Maintenance

```bash
# Quarterly: Review archives
# - Identify archives > 5 years old
# - Check if still needed
# - Document decisions

# Annually: Archive audit
# - Update archive READMEs
# - Verify restoration instructions
# - Check for broken references
```

## 🔒 Archive Preservation

### Version Control

```bash
# Archives should be in git
git add testing/archive/
git commit -m "Add archive for [reason]"

# Tag important archives
git tag -a archive-v1.0 -m "Archive from v1.0 migration"
```

### Backup Strategy

- ✅ Archives committed to git
- ✅ Included in repository backups
- ✅ Tagged for important milestones
- ✅ Documented in CHANGELOG

## 📊 Archive Analysis

### Historical Trends

```python
import os
from pathlib import Path
from datetime import datetime

archive_dir = Path("testing/archive")
archives = []

for archive in archive_dir.iterdir():
    if archive.is_dir() and archive.name != ".git":
        date = datetime.strptime(archive.name, "%Y-%m-%d")
        file_count = len(list(archive.rglob("*.py")))
        archives.append((date, file_count))

archives.sort()

print("Archive History:")
for date, count in archives:
    print(f"{date.strftime('%Y-%m-%d')}: {count} files")
```

### Archive Statistics

```bash
# Archives per year
ls testing/archive/ | cut -d'-' -f1 | sort | uniq -c

# Most common archive month
ls testing/archive/ | cut -d'-' -f2 | sort | uniq -c | sort -rn | head -5

# Largest archives
du -sh testing/archive/*/ | sort -rh | head -10
```

## 📖 See Also

- [../README.md](../README.md) - Testing overview
- [../unit/README.md](../unit/README.md) - Current unit tests
- [../integration/README.md](../integration/README.md) - Current integration tests
- [../../CHANGELOG.md](../../CHANGELOG.md) - Version history
- [../../docs/ARCHITECTURE_PLAN.md](../../docs/ARCHITECTURE_PLAN.md) - Architecture documentation

---

**Preserved with ❤️ for historical reference**
