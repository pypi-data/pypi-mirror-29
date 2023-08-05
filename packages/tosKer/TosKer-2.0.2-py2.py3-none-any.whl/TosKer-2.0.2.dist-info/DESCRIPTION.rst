TosKer
======

TosKer is an orchestrator engine capable of automatically deploying and managing multi-component applications specifies in `OASIS TOSCA <https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=tosca>`__, by exploiting `Docker <https://www.docker.com>`__ as a lightweight virtualization framework.
The novelty of TosKer is to decouple the application-specific components, from the containers used to build their infrastructure.
This permits to improve the orchestration of the components and to ease the change of the containers underneath.

=======
History
=======

0.4.0 (2017-07-10)
------------------

* First release on PyPI.


1.0.0 (2017-11-20)
----------------------------
Stable release without Management Protocols.

* Add command log, to show the execution of an operation on a component.
* Add command prune, to remove all TosKer files and restore initial state.
* Improve memory management.
* Improve command line interface.
* Bug fix.


2.0.1 (2017-12-09)
----------------------------
* Switch to Management Protocols to manage the life cycle of the components
* Add support for derived node types.
* Add support for custom interfaces.
* Support custom management protocol defined using policies.
* Support safe execution of plans (list of <component, interface, operation>).
* Improve command line interface.

2.0.2 (2017-02-12)
----------------------------
Stable release with Management Protocols.

* Add support of two type of plans (.plan, .csv).
* Fix piped input error.
* Fix errors in python2 interpreter.
* Fix bug that does not execute the delete operation on Docker volumes.

