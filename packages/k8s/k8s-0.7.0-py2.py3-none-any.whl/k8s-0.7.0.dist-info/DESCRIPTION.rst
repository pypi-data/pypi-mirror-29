k8s - Python client library for the Kubernetes API
--------------------------------------------------

|Build Status| |Codacy Quality Badge| |Codacy Coverage Badge|

.. |Build Status| image:: https://semaphoreci.com/api/v1/fiaas/k8s/branches/master/badge.svg
    :target: https://semaphoreci.com/fiaas/k8s
.. |Codacy Quality Badge| image:: https://api.codacy.com/project/badge/Grade/cb51fc9f95464f22b6084379e88fad77
    :target: https://www.codacy.com/app/mortenlj/k8s?utm_source=github.com&utm_medium=referral&utm_content=fiaas/k8s&utm_campaign=badger
.. |Codacy Coverage Badge| image:: https://api.codacy.com/project/badge/Coverage/cb51fc9f95464f22b6084379e88fad77
    :target: https://www.codacy.com/app/mortenlj/k8s?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fiaas/k8s&amp;utm_campaign=Badge_Coverage

Documentation
    https://k8s.readthedocs.io
Code
    https://github.com/fiaas/k8s

k8s is a python client library for Kubernetes developed as part of the FiaaS project at FINN.no, Norway's leading classifieds site. The library tries to provide an intuitive developer experience, rather than modelling the REST API directly. Our approach does not allow us to use Swagger to auto-generate a library that covers the entire API, but the parts we have implemented are (in our opinion) easier to work with than the client you get when using Swagger.

Check out the tutorial_ to find out how to use the library, or the `developer guide`_ to learn how to extend the library to cover parts of the API we haven't gotten around to yet.

.. _tutorial: http://k8s.readthedocs.io/en/latest/tutorial.html
.. _developer guide: http://k8s.readthedocs.io/en/latest/developer.html


Changes since last version
--------------------------

* `664a82e`_: Extend jobspec with the available api fields
* `7109ac5`_: Remove test_replication_controller
* `ae3f6e1`_: Fix field type
* `b2f3695`_: Optimize imports
* `82c67dd`_: Add support for jobs api
* `71c5bfe`_: Add support for specifying a specific command to run for a container
* `445bd6d`_: Add support for auto-generated names in metadata

.. _7109ac5: https://github.com/fiaas/k8s/commit/7109ac5
.. _82c67dd: https://github.com/fiaas/k8s/commit/82c67dd
.. _71c5bfe: https://github.com/fiaas/k8s/commit/71c5bfe
.. _ae3f6e1: https://github.com/fiaas/k8s/commit/ae3f6e1
.. _664a82e: https://github.com/fiaas/k8s/commit/664a82e
.. _b2f3695: https://github.com/fiaas/k8s/commit/b2f3695
.. _445bd6d: https://github.com/fiaas/k8s/commit/445bd6d

