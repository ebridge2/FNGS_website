FROM bids/base_fsl:5.0.9-3
MAINTAINER Eric Bridgeford <ericwb95@gmail.com>
RUN apt-get update
RUN apt-get install -y zip unzip
RUN apt-get install -y vim git

RUN apt-get install -y python-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

RUN apt-get install -y git libpng-dev libfreetype6-dev pkg-config zlib1g-dev g++ vim

RUN pip install numpy==1.12.1 networkx>=1.11 nibabel>=2.0 dipy>=0.1 scipy boto3 awscli matplotlib==1.5.3 plotly==1.12.1 nilearn>=0.2 sklearn>=0.0 pandas

RUN a=a git clone -b eric-dev-gkiar-fmri https://github.com/neurodata/ndmg.git /ndmg && cd /ndmg && python setup.py install 

RUN mkdir /ndmg_atlases && cd /ndmg_atlases && wget -rnH --cut-dirs=3 --no-parent -P /ndmg_atlases http://openconnecto.me/mrdata/share/eric_atlases/fmri_atlases.zip && unzip fmri_atlases.zip

# copy over the entrypoint script
COPY ./startfngs.sh /
ADD ./.vimrc .vimrc

# and add it as an entrypoint
ENTRYPOINT ["ndmg_bids"]