
The evoke module allows you to create evoke apps, which are twisted web-server-applications which:

- use twisted webserver (optionally proxied via apache) to serve the data
- use mysql for data storage, and present the data to you as python objects
- produce HTML output via evoke's own "evo" templating

requirements
------------

- python3 (tested on 3.6.2)
- linux (should work on BSD and MacOS also - but not yet tested)
- mysql

caution
-------

Evoke is a stable system, which has been in production use for commercial mission-critical systems since its inception in 2001.

However, python packaging and automated install are a recent (October 2017) work in progress, and some manual configuration is currently required. (see the file README.md )


