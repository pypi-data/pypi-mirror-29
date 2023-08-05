GitConsensus
============

This simple project allows github projects to be automated. It uses
“reaction” as a voting mechanism to automatically merge (or close) pull
requests.

Consensus Rules
---------------

The file ``.gitconsensus.yaml`` needs to be placed in the repository to
be managed. Any rule set to ``false`` or ommitted will be skipped.

.. code:: yaml

    # Which version of the consensus rules to use
    version: 2

    # Add extra labels for the vote counts and age when merging
    extra_labels: false

    # Don't count any vote from a user who votes for multiple options
    prevent_doubles: true

    # Minimum number of voters
    quorum: 5

    # Required percentage of "yes" votes (ignoring abstentions)
    threshold: 0.65

    # Only process votes by contributors
    contributors_only: false

    # Only process votes by collaborators
    collaborators_only: false

    # When defined only process votes from these github users
    whitelist:
      - alice
      - carol

    # When defined votes from these users will be ignored
    blacklist:
      - bob
      - dan

    # Number of hours after last action (commit or opening the pull request) before issue can be merged
    mergedelay: 24

    # Number of votes from contributors at which the mergedelay gets ignored, assuming no negative votes.
    delayoverride: 10

    # When `delayoverride` is set this value is the minimum hours without changes before the PR will be merged
    mergedelaymin: 1

    # Require this amount of time in hours before a PR with a license change will be merged.
    licensedelay: 72

    # Require this amount of time in hours before a PR with a consensus change will be merged.
    consensusdelay: 72

    # Do not allow license changes to be merged.
    lockconsensus: true

    # Do not allow consensus changes to be merged.
    lockconsensus: true

    # Number of hours after last action (commit or opening the pull request) before issue is autoclosed
    timeout: 720

Voting
------

Votes are made by using reactions on the top level comment of the Pull
Request.

+------------+---------+
| Reaction   | Vote    |
+============+=========+
| |+1|       | Yes     |
+------------+---------+
| |-1|       | No      |
+------------+---------+
| |confused| | Abstain |
+------------+---------+

Label Overrides
---------------

Any Pull Request with a ``WIP`` or ``DONTMERGE`` label (case
insensitive) will be skipped over.

Commands
--------

Authentication
~~~~~~~~~~~~~~

.. code:: shell

    gitconsensus auth

You will be asked for your username, password, and 2fa token (if
configured). This will be used to get an authentication token from
Github that will be used in place of your username and password (which
are never saved).

Merge
~~~~~

Merge all pull requests that meet consensus rules.

.. code:: shell

    gitconsensus merge USERNAME REPOSITORY

Close
~~~~~

Close all pull requests that have passed the “timeout” date (if it is
set).

.. code:: shell

    gitconsensus close USERNAME REPOSITORY

Info
~~~~

Get detailed infromation about a specific pull request and what rules it
passes.

.. code:: shell

    gitconsensus info USERNAME REPOSITORY PR_NUMBER

Force Close
~~~~~~~~~~~

Close specific pull request, including any labels and comments that
normally would be sent.

.. code:: shell

    gitconsensus forceclose USERNAME REPOSITORY PR_NUMBER

Force Merge
~~~~~~~~~~~

Merge specific pull request, including any labels and comments that
normally would be sent.

.. code:: shell

    gitconsensus forcemerge USERNAME REPOSITORY PR_NUMBER

.. |+1| image:: https://assets-cdn.github.com/images/icons/emoji/unicode/1f44d.png
.. |-1| image:: https://assets-cdn.github.com/images/icons/emoji/unicode/1f44e.png
.. |confused| image:: https://assets-cdn.github.com/images/icons/emoji/unicode/1f615.png



