##########
Change Log
##########

All notable changes to this project are documented in this file.


==================
1.2.1 - 2018-02-15
==================

Fixed
-----
* Include LICENSE in the manifest.
* Remove unnecessary documentation files, fix warnings and update
  documentation.

Added
-----
* Fix build bundle and prepare release


==================
1.2.0 - 2015-11-17
==================

Fixed
-----

* Documentation supports new namespace.
* Scripts support new namespace.


==================
1.1.2 - 2015-05-27
==================

Changed
-------

* Use urllib.urlparse.
* Slumber version bump (>=0.7.1).


==================
1.1.1 - 2015-04-27
==================

Changed
-------

* Query projects by slug or ID.

Fixed
-----

* Renamed genapi module in README.
* Renamed some methods for fetching resources.

Added
-----

* Query data directly.


==================
1.1.0 - 2015-04-27
==================

Changed
-------

* Renamed genesis-genapi to genesis-pyapi.
* Renamed genapi to genesis.
* Refactored API architecture.


==================
1.0.3 - 2015-04-22
==================

Fixed
-----

* Fix not in cache bug at download.


==================
1.0.2 - 2015-04-22
==================

Changed
-------

* Docs updated to work for recent changes.

Added
-----

* Universal flag set in setup.cfg.


==================
1.0.1 - 2015-04-21
==================

Fixed
-----

* URL set to dictyexpress.research.bcm.edu by default.
* Id and name attribute are set on init.

Added
-----

* Added label field to annotation.


==================
1.0.0 - 2015-04-17
==================

Changed
-------

* Upload files in chunks of 10MB.

Fixed
-----

* Create resources fixed for SSL.
