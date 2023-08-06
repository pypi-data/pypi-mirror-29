dominosort
==========

*Sort sequences with respect to the similarity of consecutive items.*

Definition
----------

Given a sequence of items :math:`(x_i, y_i)`, where each item is represented by two values
:math:`x, y`, the goal is to sort the sequence such that the following loss
is minimal:

.. math::

   L = \sum_{i=1}^{N-1} \mu(y_i, x_{i+1})

where :math:`\mu` denotes a suitable metric for the items' values.

Example
-------

Given the items

.. code:: python

   >>> items = [
   ...     (0.4, 0.6),
   ...     (0.0, 0.2),
   ...     (0.8, 1.0),
   ...     (0.6, 0.8),
   ...     (0.2, 0.4),
   ... ]

together with the L1 distance :math:`\mu: (x, y) \rightarrow |x-y|`, the current loss is

.. code:: python

   >>> abs(0.6 - 0.0) + abs(0.2 - 0.8) + abs(1.0 - 0.6) + abs(0.8 - 0.2)
   2.2

Clearly the optimal sort order which minimizes the loss is

>>> optimal = [
   ...     (0.0, 0.2),
   ...     (0.2, 0.4),
   ...     (0.4, 1.6),
   ...     (0.6, 0.8),
   ...     (0.8, 1.0),
   ... ]

Related topics
--------------

Note that for the special case where :math:`x_i = y_i` and the :math:`x_i` represent 2d-coordinates
this corresponds to the Travelling Salesman Problem without return to the origin.


