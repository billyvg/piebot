====
Contributing
====

    vagrant up
    vagrant ssh
    virtualenv env
    source env/bin/activate
    python setup.py develop
    cp settings.py.default settings.py
    cp bootstrap.py.default bootstrap.py

Edit settings.py and bootstrap.py

    python bootstrap.py
    python bin/bot.py
