# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Added rate limiting middleware to all API routes
- Added CSV export functionality for the analytics dashboard
- Added dark mode support to the settings page
- Added pagination to the `/users` and `/orders` endpoints
- Added input validation for date range filters
- Added Prometheus metrics endpoint at `/metrics`
- Added retry logic for outbound webhook delivery
- Added API key rotation endpoint

### Changed

- Updated README with new environment variable documentation
- Upgraded FastAPI from version 0.95 to 0.111

### Fixed

- Fixed null pointer exception in user session cleanup
- Fixed incorrect HTTP status code on empty search results (500 → 204)
- Fixed memory leak in background job processor
- Fixed duplicate email sending on password reset

### Removed

- Removed deprecated `/api/v1/legacy` endpoints
- Removed legacy user migration script (previously applied)
