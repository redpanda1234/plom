# Plom Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

### FIxed


## [0.5.1] - 2020-09-25

### Added
* Annotator: Ctrl-r shortcut key for Rearrange Pages tool.

### Changed
* `plom-hwscan` has command line arguments for gamma shift, off by default as it sometimes worsens already poor scans with large shadows.
* `plom-hwscan` does not extract jpeg's by default (it may in the future).
* `plom-hwscan` has new command line arguments for jpeg extraction.

### Fixed
* Workaround for bug in PyMuPDF 1.17.6.
* Various packaging improvements and fixes.
* "Rearrange Pages" dialog resizing improved.


## [0.5.0] - 2020-08-26

### Added
* Client now has a menu button for less-commonly used commands.
* Client can now insert small images, see "insert image" in menu.
* Client has experimental "Rearrange pages" dialog to fine-tune page selection and layout.
* We again offer prebuilt client binaries for some OSes.
* Server has new experimental "Homework mode" to deal with student-scanned images.
* Server can use Scikit-learn (instead of the default TensorFlow) for reading student numbers.

### Changed
* Command line utilities can report their version.
* Example demo data uses handwritten digits instead of fonts.
* Annotator remains open between papers.
* Totaller client was removed.
* ID-subclient - student name + id is entered in single field which auto-completes on both.
* Client sidebar can be set to the left or right (independent of mouse handedness).
* Grades output filename is now "marks.csv".
* Changes to various command-line tools to streamline uploading and other operations.
* Scanning is now based more strongly on concept of "bundles" of papers.
* Most tools now interact with the server via the API instead of using the file system.
* Server docker image uses pinned dependency information for reproducibility.* Server, Manager and Client handling of "unknown" pages has improved.
* Client has visual feedback for ctrl-, shift- tool alternatives via mouse cursor.
* Various client UI tweaks.
* Various improvements to the manager UI tool.

### Fixed
* Fix left-hand mouse mode.
* Annotation font sizes no longer directly depend on UI font size (but some issues still remain).
* Pan mode no longer incorrectly moves objections.
* Many other bug fixes.


## [0.4.2] - 2020-04-21

### Added
* User-management can be performed by the manager client.

### Changed
* Greater fidelity to the original scan because JPEG files are (carefully) extracted and used directly.
* JPEG transformations are done without lossy re-encoding, when possible.
* PNG files should be a little smaller with fewer interpolation artifacts in the reass
* User credentials now handled by database rather than separate authentication object.
* Client can no longer revert; this feature may return later if needed.

### Fixed
* Various bug fixes.


## [0.4.1] - 2020-04-13

### Added
* Re-enabled the automatic IDing of papers using machine learning.
* Python package has improved dependency information.
* `plom-demo` checks if server is running and warns if directory isn't empty.
* Appdata metadata added for Plom Client.

### Changed
* Manager UI tool has better reporting of what users are doing.
* Manager and command line tools report papers that are marked "out"; this may be useful in case of client crashes, to identify (and reset) papers marking out for grading/IDing.
* Update for new plomgrading.org domain name.
* Remove testing tool dependencies on xvfb.

### Fixed
* Fixed toml dependency in Dockerfile.
* Various misc fixes.


## [0.4.0] - 2020-04-04

### Added
* Plom is now a python package.
* Annotator has a "no answer given" button which places crossed lines on page, leaves a comment, sets mark to 0.
* Client can log to a file (set under "More options").
* Client has expert option to disable background upload/download.
* Client can generate a log file for debugging.
* Server management UI.
* Command-line scripts for creating tests, managing server, scanning, and finishing.
* Simple toy test+server for demonstrating Plom.
* Test-specification now has "do-not-mark" pages for formula-sheets and instruction pages.

### Changed
* Server: improved database.
* Server: new upload procedure/tools.
* Reassembly tasks are now faster.
* Client: if there are annotations, confirm before closing/cancelling.

### Fixed
* Server: manager-related database locks fixed.
* In some regrade cases, delta-comments did not apply correctly.
* Client: fix `ctrl-=` zoom toggle.
* Various bug fixes.


## [0.3.0] - 2020-02-10

### Added
* saved comments are filtered per question and per test.
* Marker has a "view" button to look at any test number.

### Changed
* The manual-identifier now has a "discard" option for unneeded page images, such as blank extra pages.
* More robust networking by moving to https (rather than raw sockets). This is handled by the "requests" library on the client side and the "aiohttp" library on the server side.
* Client: config and saved comments now more human-readable in toml files.
* Client: can download test/server info before logging in.
* Client is more pessimistic about errors and will crash instead of trying to continue
in most cases.
* Client checks for double-logins and can force logout a previous session.
* Client: you must make at least one annotation on the page.

### Fixed
* Many fixes, especially related to client crashes due to networking.


## [0.2.2] - 2019-11-29

### Added
* Can now build papers with student Names/IDs pre-written on page 1.
* Client now has a "view" button to quickly view other questions.

### Changed
* Warning given for non-Latin names in classlist (may cause problems in PDFs).

### Fixed
* Annotator mark up/down and handedness preferences now saved between sessions.


## [0.2.1] - 2019-11-11

### Added
* preliminary support for a canned user list.
* autogenerate password suggestions for new users.
* 05 script now warns about potential extra pages.
* Annotator - spacebar pans through paper (down and right), shift-space pans back (up and left). Ctrl+space, Ctrl-shift-space does similarly but more slowly.
* Annotator - zoom-mode click-drag creates a (temp) rectangle to zoom into.

### Changed
* make 04 script less verbose.
* Increase timeout on server ping test.
* Annotator has more keybindings for grades of 0-10 (see "key help").
* resizing annotator persists between papers.
* zooming annotator persists between papers.
* docs: changes for uploading to the new Canvas gradebook.
* Annotator - can no longer click in region around score-box. This prevents accidentally pasting objects behind the scorebox.

### Fixed
* fixed race conditions when/uploading and downloading.
* certain file transfers are more robust at reporting errors.
* userManager was failing to start.
* return to greeter dialog on e.g., wrong server or pagegroup/version out of range.
* `mark_reverter` less fragile if files DNE.
* if you skip identifying a test, the client will defer it until the end.
* identifying has various other UI fixes.


## [0.2.0] - 2019-10-11

### Added

#### Client
* delete tool: right-mouse button drag sweeps out a rectangle and deletes its contents.
* improve zoom ("ctrl-=" cycles through zoom modes).
* shift-click and control-click should now emulate right-click and middle-click.
* middle-button in line/pen tools creates line/path with arrow-heads at both ends.
* annotations are now saved in ".plom" files, supports continuing previously marked papers.
* marker now uploads/downloads papers in the background.

#### Server
* Handle upload/download of .plom files.
* New `12_archive` script makes a minimal zip file for archiving.
* Support for Docker.
* New templates for making your own tests.

### Changed

#### Client
* client not backward compatible with v0.1.0 servers.
* mark-total mode is removed.
* comment-delta is now its own grouped object, with many changes to encourage comment-reuse.
* comment-add and edit is now via a pop-up window.
* user can now make 0-point comments (for which the zero is pasted).
* user can also make no-point comments which are pasted as just text.
* general GUI improvements.

#### Server
* Server not backward compatible with v0.1.0 clients.
* More general support for student names.
* Returned PDF files have better sizes for printing hardcopies.

### Fixed

* Many many bugfixes.


## 0.1.0 - 2019-06-26

This is the first release of Plom, PaperLess Open Marking.

[Unreleased]: https://gitlab.com/plom/plom/compare/v0.5.1...master
[0.5.1]: https://gitlab.com/plom/plom/compare/v0.5.0...v0.5.1
[0.5.0]: https://gitlab.com/plom/plom/compare/v0.4.2...v0.5.0
[0.4.2]: https://gitlab.com/plom/plom/compare/v0.4.1...v0.4.2
[0.4.1]: https://gitlab.com/plom/plom/compare/v0.4.0...v0.4.1
[0.4.0]: https://gitlab.com/plom/plom/compare/v0.3.0...v0.4.0
[0.3.0]: https://gitlab.com/plom/plom/compare/v0.2.2...v0.3.0
[0.2.2]: https://gitlab.com/plom/plom/compare/v0.2.1...v0.2.2
[0.2.1]: https://gitlab.com/plom/plom/compare/v0.2.0...v0.2.1
[0.2.0]: https://gitlab.com/plom/plom/compare/v0.1.0...v0.2.0
