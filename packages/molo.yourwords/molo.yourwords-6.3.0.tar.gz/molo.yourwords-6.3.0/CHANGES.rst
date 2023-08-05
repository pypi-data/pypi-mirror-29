CHANGE LOG
==========

6.3.0
-----
- Replace Page with MoloPage proxy

6.2.5
-----
- bug fix: return entry site when user profile has no site or site is none

6.2.4
-----
- bug fix: return entry site when user profile has no site or site is none

6.2.3
-----
- bug fix: return entry site when user profile has no site

6.2.2
-----
- bug fix: only use get_object_or_404 with pks

6.2.1
-----
- fix PyPI classifier

6.2.0
-----
- add support for Python 3
- template improvements: compress images, improve date picker

6.1.0
-----
- add support for Django 1.11

6.0.1
-----
- added country to csv

6.0.0
-----
- Official release for YourWords 6.0.0
- Dropped support for Django 1.10

6.0.1-beta.1
------------
- Upgrade to Django 1.10, Molo 6x

6.0.0-beta.1
------------
- Upgrade to Django 1.10, Molo 6x

5.0.1
-----
- Bug Fix: Only show entries specific to site

5.0.0
-----
- Added multi-site functionality

2.2.2
-----
- Remove promotion settings from Ts&Cs and thank you page

2.2.1
-----
- Fixed brken link for competitions in the admin, by allowing users to filter competition entries by competition slug

2.2.0
-----
- Added Your Words view to Wagtail Admin

2.1.0
-----
- Removed ability to delete YourWords Competition IndexPage in the Admin UI

2.0.0
-----
- Upgraded dependency to molo v4
- Fixed bug in converting yourwords entry to an article

1.2.2
-----
- Add yourwords permission to groups

1.2.1
-----
- Updated YourWords markup to

1.2.0
-----
- Add YourWords to sections

1.1.4
-----
- Server srcset image thumbnail

1.1.3
-----
- Home page thumbnail and main page images

NOTE: Templates updates

1.1.2
-----
- Return None if there is no competition

1.1.1
-----
- BEM templates methodology

1.1.0
-----
- Add support for hiding untranslated content

1.0.2
-----
- Removed `http://testserver` from test URLs

1.0.1
-----

- Restructured your words competition to introduce index page

NOTE: This release is not compatible with molo versions less than 3.0

1.0.0
-----

- Added multi-language support

Backwards incompatible changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- deprecated use of ``LanguagePage``: your words competition is now direct child of ``Main`` (use ``SiteLanguage`` for multilanguage support)
- deprecated use of ``competition.thank_you_page``: use the template tag ``{% load_thank_you_page_for_competition competition as thank_you_pages %}``

NOTE: This release is not compatible with molo versions less than 3.0

0.0.2
-----
- update django admin
- add convert to article functionality

0.0.1
-----
- initial release
