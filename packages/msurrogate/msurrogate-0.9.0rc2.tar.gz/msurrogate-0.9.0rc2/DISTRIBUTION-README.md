# Distribution details for developers

## Twine Usage

Review 
https://pypi.python.org/pypi/twine

but essentially

./setup.py sdist bdist_wheel

then,

twine upload dist/*

## Versioning Check

The setup.py script for bdist, sdist, and bdist_wheel will check and warn if versions are inconsistent between the module's stated version, the setup.py version and the current git describe --tags call. It will not warn if it cannot load the module or if it cannot call git.

If the tagging was done on a revision, but the source must then be tweaked (perhaps to fix these versioning hiccups), then the tag can be force changed using

>git tag -f -a -m "message" tag

Note that the tag should not be sent to the remote at this point, this can be tested with

>git ls-remote --tags <remote>

or 

>git ls-remote <remote> /refs/tags/<tag>


These hooks are described in
https://stackoverflow.com/questions/11331175/hook-to-add-commands-to-distutils-build


## RST
review at http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html
