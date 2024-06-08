Usage
=====

Here is how to use ai_diff_commit:

.. code-block:: python

   # Example usage of ai_diff_commit
   import ai_diff_commit
   ai_diff_commit.run()

The `ai_diff_commit` script automates the process of generating commit messages using AI. It can analyze diffs, generate commit messages, and optionally push changes.

Command Line Arguments
-----------------------

- `-p, --push` : Automatically push changes.
- `-a, --add` : Automatically add all changes.
- `-m, --model` : Specify the OpenAI API language model.

Example
-------

To run the script and automatically push changes:

.. code-block:: shell

   python ai_diff_commit.py --push
