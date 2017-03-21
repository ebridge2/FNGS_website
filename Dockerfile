FROM bids/base_fsl:5.0.9-3
MAINTAINER Eric Bridgeford <ericwb95@gmail.com>
RUN apt-get update && apt-get install -y python-dev python-setuptools python-numpy python-scipy zlib1g-dev python-nose fsl
RUN easy_install pip
RUN apt-get install -y libpng-dev libfreetype6-dev pkg-config
RUN pip install --ignore-installed cython numpy coveralls wget nibabel nilearn dipy sklearn networkx boto3 multiprocessing awscli plotly==1.12
RUN pip install django
RUN apt-get install python-dateutil
RUN apt-get install -y zip unzip
RUN apt-get install -y vim git
RUN pip install matplotlib==1.5.1
# testing

RUN git clone -b eric-dev-gkiar-fmri https://github.com/neurodata/ndmg.git /ndmg && cd /ndmg && python setup.py install
# apparently matplotlib gets messed up during install of ndmg
RUN pip install -U --force-reinstall matplotlib==1.5.1

# clone the website repo and make the location for the downloads
RUN git clone https://github.com/ebridge2/FNGS_website.git && mkdir /FNGS_server && mkdir /FNGS_server/input_data && mkdir /FNGS_server/output_data

RUN pip install psutil
# download the website
#RUN cd /FNGS_website/fngs && python manage.py makemigrations analyze && python manage.py migrate

# Get atlases
RUN cd /FNGS_server && wget http://openconnecto.me/mrdata/share/atlases/fmri_atlases.zip && unzip fmri_atlases.zip
RUN mkdir /ndmg_atlases && wget -rnH --cut-dirs=3 --no-parent -P /ndmg_atlases http://openconnecto.me/mrdata/share/atlases/

# copy over the entrypoint script
COPY ./startfngs.sh /
# and add it as an entrypoint
# ENTRYPOINT ["/startfngs.sh"]
ENTRYPOINT ["ndmg_bids"]
