# How to

This readme covers how to create an interactive layer for easing debugging of services offered in docker containers. This makes it simple to debug from a remote server using, say, docker.

## Dockerfile

```
# this container contains the pipeline pre-installed
FROM neurodata/m3r-release:0.1.1
# me
MAINTAINER Eric Bridgeford <ericwb95@gmail.com>

# jupyter so we can forward out of a notebook
RUN pip install jupyter

# entrypoint for jupyter
ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
```

As you can see above, our goal is to create an interactive layer for the `neurodata/m3r-release` docker container from jupyter notebooks.

We indicate the container we want to build from, and simply install jupyter on top of it. Finally, we set the entrypoint as appropriate to default to jupyter.

We use the following convention:

```
container-port: a port for the docker container.
remote-port: a port for the server.
host-port: a port from the host machine (your computer).
```

## From first shell

`ssh` to your server:

```
ssh <username>@<server>
```

Begin by building your new container:

```
docker build -t <user>/<container-name>:<version> .
```

which in my case is:

```
docker build -t neurodata/m3r-release:jupyter .
```

Next, start up the docker container and jupyter service using docker:

```
docker run -t -p <remote-port>:<container-port> <user>/<container-name>:<version>
```

Which in my case is:

```
docker run -t -p 8890:8888 neurodata/m3r-release:jupyter
```

Note you will receive the following terminal output (particularly, the token):

```
[I 04:04:58.753 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 04:04:58.972 NotebookApp] Serving notebooks from local directory: /
[I 04:04:58.972 NotebookApp] The Jupyter Notebook is running at:
[I 04:04:58.972 NotebookApp] http://(bff0366fec48 or 127.0.0.1):8888/?token=<token>
[I 04:04:58.972 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 04:04:58.976 NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-1-open.html
    Or copy and paste one of these URLs:
        http://(bff0366fec48 or 127.0.0.1):8888/?token=<token>
```

Leave this shell session open.

## From your second shell

Open an ssh tunnel from a new shell session:

```
ssh -L localhost:<host-port>:<remote-port> <username>@<server>
```

Which in my case is:

```
ssh -L localhost: <username>@<server>
```

Then, in your browser, navigate to:

```
localhost:<host-port>/?token=<token>
```
Which for me is:

```
localhost:8888/?token=<token>
```
