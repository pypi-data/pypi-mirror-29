Tiny Block: A Simple Blockchain
=========================

Installation
------------

Install and update using `pip`_:

.. code-block:: bash

    $ pip install tinyblock

Block
-------------

.. code-block:: python

    dict({'previous_hash'(str): '...',
          'timestamp'(int): '...',
          'data'(any): '...',
          'nonce'(int): '...',
          'next_hash'(str): '...'})

Usage
-------------

* Define a simple blockchain:

  .. code-block:: python

      from tinyblock import tinyblock
      #The initial variable should be a list of blocks. If not set it, the default chain would be an empty list.
      my_blockchain = tinyblock()

* Add a block to the chain:

  .. code-block:: python

      #The parameter is the data of this block
      my_blockchain.add('This is a block.')

* Find a block with statement:

  .. code-block:: python

      #Find the blocks with features below. The return elements will content the index in origin chain list.
      #Completely match: previous_hash, nonce, next_hash.
      #Partly match: data. (Currently support str, int, float, list, dict, bool and tuple)
      #Range match: timestamp.(Could be an int, list or tuple)
      my_blockchain.find(previous_hash='', timestamp='', data='', nonce='', next_hash='')

* Pop the last block of the chain:

  .. code-block:: python

      my_blockchain.pop()

* Check wether the blockchain is anything correct:

  .. code-block:: python

      my_blockchain.chainCheck(print_option=True)

* Fix the blockchain(with start and stop index):

  .. code-block:: python

      my_blockchain.chainFix(start=0, stop=4)

* Get the block list:

  .. code-block:: python

      my_blockchain.getChain()

* Customise the rule for mining new block:

  .. code-block:: python

      #The default rule is hash start with '0000'.
      #To change the rule, you can override the mineRule function.
      def newRule(hash):
          if hash[0:5] == '0'*5:
              return True
          return False

      my_blockchain.mineRule = newRule

.. _pip: https://pip.pypa.io/en/stable/quickstart/

