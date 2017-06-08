FROM neurodata/sic:paper
MAINTAINER Eric Bridgeford

USER root
RUN pip install numpy==1.12.1 
RUN pip install matplotlib==1.5.3
RUN git clone -b eric-dev-gkiar-fmri https://github.com/neurodata/ndmg.git /ndmg && cd /ndmg && python setup.py install

COPY sic_fngs.ipynb /home/sic-user/sic_fngs.ipynb
USER sic-user
