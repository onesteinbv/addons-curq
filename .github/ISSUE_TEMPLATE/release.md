---
name: Release
about: Track release preparation tasks
title: "Release X.Y.Z"
labels: release
assignees: ''
---

## Release Checklist

### Testing
- [ ] Test the development Docker build if all changes in the newsfragments directory are included and working as expected
- [ ] Assign a second reviewer to verify

### Create Release Notes
- [ ] Run towncrier to generate release notes (`towncrier build --version 18.0.X.Y`)
- [ ] Review the generated release notes and make any necessary edits to ensure clarity and accuracy for users, try to avoid technical jargon and keep it concise.
- [ ] Translate release notes to Dutch (`NEWS.nl_NL.md`)
- [ ] Update documentation on [docs.curq.nl](https://docs.curq.nl) if necessary (https://github.com/onesteinbv/curq-docs)
- [ ] Commit release notes to the repository

### Release
- [ ] Tag commit with version number (e.g. 18.0.11.2)
- [ ] Push the tag to the repository
- [ ] Wait until CI pipeline completes successfully (https://github.com/onesteinbv/addons-curq/actions/workflows/tag.yml)
  - [ ] If the CI pipeline fails, fix the issues and repeat the previous steps
- [ ] Create and publish GitHub release with release notes and changelog (in English)

### Post-Release
- [ ] Publish release announcement on https://curq.nl and social media channels
- [ ] Plan next release cycle
