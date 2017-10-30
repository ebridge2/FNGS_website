FROM neurodata/sic:paper
MAINTAINER Eric Bridgeford

USER root

#--------Environment Variables-----------------------------------------------#
ENV NDMG_URL https://github.com/neurodata/ndmg.git
ENV ATLASES http://openconnecto.me/mrdata/share/eric_atlases/eric_atlases.zip
ENV AFNI_URL https://afni.nimh.nih.gov/pub/dist/bin/linux_fedora_21_64/@update.afni.binaries
ENV LIBXP_URL http://mirrors.kernel.org/ubuntu/pool/main/libx/libxp/libxp6_1.0.2-2_amd64.deb


#--------Initial Configuration-----------------------------------------------#
# download/install basic dependencies, and set up python
RUN apt-get update
RUN apt-get install -y zip unzip vim git python-dev curl libglu1
RUN echo "ln -s /usr/lib/x86_64-linux-gnu/libgsl.so /usr/lib/libgsl.so.0" >> ~/.bashrc

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

RUN apt-get clean && apt-get update

RUN \
    apt-get install -y git libpng-dev 
RUN apt-get install -y libfreetype6-dev
RUN apt-get install -y pkg-config
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y g++
RUN apt-get install -y vim


#---------AFNI INSTALL--------------------------------------------------------#
# setup of AFNI, which provides robust modifications of many of neuroimaging
# algorithms
RUN \
    wget -c $LIBXP_URL && \
    dpkg -i `basename $LIBXP_URL` && \
    apt-get install -f && \
    curl -O $AFNI_URL && \
    chsh -s /usr/bin/tcsh && \
    tcsh @update.afni.binaries -package linux_openmp_64 -do_extras && \
    chsh -s /bin/bash && \
    cp /root/abin/AFNI.afnirc /root/.afnirc && \
    echo "PATH=$PATH:/root/abin" >> ~/.bashrc


#--------NDMG SETUP-----------------------------------------------------------#
# setup of python dependencies for ndmg itself, as well as file dependencies
RUN \
    pip install numpy==1.12.1 networkx>=1.11 nibabel>=2.0 dipy>=0.1 scipy \
    boto3 awscli matplotlib==1.5.3 plotly==1.12.1 nilearn>=0.2 sklearn>=0.0 \
    pandas cython

RUN \
    a=a git clone -b m3r-release $NDMG_URL /ndmg && \
    cd /ndmg && \
    python setup.py install 

RUN \
    mkdir /ndmg_atlases && \
    cd /ndmg_atlases && \
    aws s3 cp --no-sign-request s3://mrneurodata/data/resources/ndmg_atlases.zip ./ && \
    unzip ndmg_atlases.zip


COPY sic_ndmg.ipynb /home/sic-user/sic_ndmg.ipynb
USER sic-user
