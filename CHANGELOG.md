# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- If you have more ideas for features, you can either open an issue or drop a pull request
##[1.2.0] - 2020-03-28
### Added
 - user can no change the timezone.
    - This has an effect on the time that votes get deleted and the time a slack message is sent.

##[1.1.0] - 2020-03-12
### Changed
 - new look for Where To Eat

##[1.0.3] - 2020-02-13
### Added
 - automatic deletion of debug and audit log file if they are to big / every hour there will be one check
### Bugfix
 - Votes will now be deleted after entering an absence for the current vote day


##[1.0.2] - 2020-02-12
### Bugfix
- Background image and default Background settings are now available for absence Page

### Added
- new log file for audit logs /also mounted via log folder

### Changed
- Log folder is now mounted in a volume

## [1.0.1] - 2020-02-10
### Added
- default background. If the admin does not provide a background-image, background-color will be set to a gray shade
- changelog 

### Changed
- env.dev, some variables were not used anymore 
- local_settings, delete unused/not necessary settings
- slack messages are now in english.

## [1.0.0] - 2020-02-03
### Added
- published project