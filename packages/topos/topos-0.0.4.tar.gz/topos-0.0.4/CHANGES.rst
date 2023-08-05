0.0.4 21/03/2018
================

Setting the release to only be on the test_travis task and python version 3.6

0.0.3 21/02/2018
================

Another "release" that will hopefully work this time

0.0.2 21/02/2018
================

This release is mainly to test the deploy: option on travis although there
have been some changes

Added
-----
- Mesh class to manage and export object data
- Mesh data can be exported in .obj format
- Generators that can generate either a plane or a uncapped cylinder
- New Primitives:
  + Plane
  + Cylinder
- Started thinking about a transformation framework which makes use of the
  :code:`>>` operator to support 'pipeline' operations e.g. obj >> scale >>
  transform


0.0.1 17/02/2018
================

Initial release
