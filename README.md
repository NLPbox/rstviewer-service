Warning
=======

This repository is DEPRECATED, please use the REST API of rstWeb instead:
https://github.com/NLPbox/rstweb-service


rstviewer-service
=================

This docker container allows you to build, install and run
[rstviewer](https://github.com/arne-cl/rstviewer) as a REST API in a docker container.

`rstviewer` is a command-line tool for converting Rhetorical Structure Theory
rs3 files into images. It is heavily based on Amir Zeldes' [rstWeb](https://github.com/amir-zeldes/rstWeb), a web based
annotation tool for rhetorical structures.


Installation
------------

You can either build the service locally and run it like this:

```
git clone https://github.com/NLPbox/rstviewer-service
cd rstviewer-service
docker build -t rstviewer-service .
docker run -p 8000:8000 -ti rstviewer-service
```

Or, you can just run a pre-built docker container from Docker Hub:

```
docker run -p 8000:8000 -ti nlpbox/rstviewer-service
```

Usage
-----

`rstviewer-service` can either convert an `.rs3` file into a `.png` image
of the Rhetorical Structure tree or return a `base64` encoded string of
a `.png` image.

```
curl -X POST -F "input=@input.rs3" http://localhost:8000/rs3_to_png > output.png
curl -X POST -F "input=@input.rs3" http://localhost:8000/rs3_to_png_base64 | base64 --decode > decoded.png
```
