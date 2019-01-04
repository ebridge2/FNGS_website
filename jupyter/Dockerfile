# this container contains the pipeline pre-installed
FROM neurodata/m3r-release:0.1.1
# me
MAINTAINER Eric Bridgeford <ericwb95@gmail.com>

# jupyter so we can forward out of a notebook
RUN pip install jupyter

# entrypoint for jupyter
ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
