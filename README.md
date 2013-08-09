# Information
This project started as a school assignment which I will continue to
work on for fun... I'm choosing to make pgsql as a requirement because
I want to learn it and move away from mysql. Portability may be 
something that I will worry about later.

# Install
```
virtualenv env 
source env/bin/activate
pip install -r requirements.txt
cp settings.py.default settings.py
cp bootstrap.py.default bootstrap.py
```

Edit settings.py and bootstrap.py  

```
python bootstrap.py
python ppbot.py
```
