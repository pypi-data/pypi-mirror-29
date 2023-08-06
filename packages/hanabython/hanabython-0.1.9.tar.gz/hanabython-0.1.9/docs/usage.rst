=====
Usage
=====

Import
------

To use Hanabython in a project::

    import hanabython

Getting started (in a terminal)
-------------------------------

::

    from hanabython import Game, Configuration, PlayerHumanText
    Game(players=[
        PlayerHumanText('Antoine'),
        PlayerHumanText('Donald X'),
        PlayerHumanText('Uwe')
    ]).play();

Getting started (in a notebook)
-------------------------------

::

    from hanabython import Game, Configuration, PlayerHumanText
    Game(players=[
        PlayerHumanText('Antoine', ipython=True),
        PlayerHumanText('Donald X', ipython=True),
        PlayerHumanText('Uwe', ipython=True)
    ]).play();
