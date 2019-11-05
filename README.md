REQUIREMENTS
=======
Python 3.5

PRE-INSTALL
=======
Linux
```bash
$ sudo add-apt-repository -y ppa:ubuntugis/ppa
$ sudo apt-get update
$ sudo apt install gdal-bin python-gdal python3-gdal
$ export CPLUS_INCLUDE_PATH=/usr/include/gdal
$ export C_INCLUDE_PATH=/usr/include/gdal

```
Windows
```bash
???
```

INSTALL
=======
Linux
```bash
$ pip install -r requirements.txt
```
Windows
```bash
python -m pip install -r requirements.txt
```

RUN
===
```bash
$ python server.py &
```

TEST
===
```html
http://localhost:5000
```
