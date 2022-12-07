EBBR Release Process
====================

The latest top of tree version can be found on
`https://arm-software.github.io/ebbr`.
PDF copies are generated for each tagged release, and can be found at
`https://github.com/arm-software/ebbr/releases`.

EBBR uses github actions to produce document artifacts, including PDF and github
pages version.
This is configured in the ``.github/workflows/main.yaml`` file.
The github builds are triggered by updates to any github repository, including
personal forks, and releases are made in Arm's repository
`https://github.com/arm-software/ebbr`.
This document covers the process for making an EBBR release so that the build in
Arm's repository is triggered correctly.

In practical terms, only the persons with permission to push to Arm' repository
are able to do this release process.
The process is documented here for both transparency and to remind the
authorised persons how to make a release.

Process for merging changes into mainline
-----------------------------------------

Push changes to ``main`` branch on `https://github.com/arm-software/ebbr` or
merge pull requests.

Updating ``main`` branch will trigger github actions to update
`https://arm-software.github.io/ebbr` and generate PDF for the run.

Process for tagging releases and pre-releases
---------------------------------------------

Create a signed tag for the pre-release in the form ``v<w>.<x>.<y>[-pre<z>]``
and push out to ``main`` branch on `https://github.com/arm-software/ebbr`::

   git tag --sign vW.X.Y-preZ
   git push --follow-tags origin main:main

Updating ``main`` branch with a tag will trigger github actions to perform a
release and publish a .pdf.
Github will automatically recognize the difference between pre-releases and full
releases.
If the build passes, a release is created in
`https://github.com/ARM-software/ebbr/releases`.
Releases can also be marked as pre-release manually.
