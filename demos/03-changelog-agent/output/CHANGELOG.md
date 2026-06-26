# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Added rate limiting middleware to all API routes
- Added CSV export for analytics dashboard
- Added dark mode support to settings page
- Added pagination to /users and /orders endpoints
- Added input validation for date range filters
- Added prometheus metrics endpoint at /metrics
- Added retry logic to outbound webhook delivery
- Added API key rotation endpoint

### Fixed

- Fixed null pointer in user session cleanup
- Fixed incorrect status code on empty search results (was 500, now 204)
- Fixed memory leak in background job processor
- Fixed duplicate email sending on password reset

### Removed

- Removed deprecated /api/v1/legacy endpoints
- Removed user_legacy table migration script (already applied)
