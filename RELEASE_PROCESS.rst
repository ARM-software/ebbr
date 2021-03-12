EBBR Release Process
====================

The latest top of tree version can be found on
`https://arm-software.github.io/ebbr`.
PDF copies are generated for each tagged release, and can be found at
`https://github.com/arm-software/ebbr/releases`.

EBBR uses Travis-CI to produce document artifacts, including PDF and github
pages version.
The TravisCI builds are triggered by updates to Grant Likely's github fork,
`https://github.com/glikely/ebbr`.
This document covers the process for making an EBBR release so that the
Travis CI build is triggered correctly.

In practical terms, only Grant is able to do this release process.
The Travis CI key is associated with his personal repo because the
github.com/ARM-Software account is not connected with Travis CI.
The process is documented here for both transparency and to remind
Grant how to make a release.

Process for merging changes into mainline
-----------------------------------------

1. Push changes to ``main`` branch on `https://github.com/arm-software/ebbr`
   or merge pull requests.
2. Update ``upstream`` branch on `https://github.com/glikely/ebbr`::

      git push glikely main:upstream

Updating ``upstream`` branch will trigger Travis ci to update
`https://arm-software.github.io/ebbr`.

Process for tagging releases and pre-releases
--------------------------------

1. Create a signed tag for the pre-release in the form ``v<w>.<x>.<y>[-rc<z>]``
   and push out to ``main`` branch on `github.com/arm-software/ebbr`::

      git tag --sign vW.X.Y-rcZ
      git push --follow-tags origin main:main

2. Sync to ``upstream`` branch on ``github.com/glikely/ebbr``::

      git push --follow-tags glikely main:upstream

   Updating `upstream` branch with a tag will trigger Travis CI to perform a
   release and publish a .pdf.
   Github will automatically recognize the difference between pre-releases
   and full releases.

3. If the build passes, manually create a release in
   `https://github.com/ARM-software/ebbr/releases` and copy ``ebbr-<version>.pdf``
   from `https://github.com/glikely-software/ebbr/releases`
