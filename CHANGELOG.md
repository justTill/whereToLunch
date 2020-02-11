# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- automatic deletion/clearing of debug.log file/volume

##[1.0.1] - 2020-02.11
### Bugfix
- Background image and default Background settings are now available for absence Page

### Changed
- Logfile is now mounted in a volume

## [1.0.1] - 2020-02-10
### Added
- default background. If the admin does not provide a background-image, background-color will be set to a gray shade
- changelog 

### Changed
- env.dev, some variables were not used anymore 
- local_settings, delete unused/not necessary settings
- increase version number in docker-compose.prod file
- slack messages are now in english.

## [1.0.0] - 2020-02-03
### Added
- published project