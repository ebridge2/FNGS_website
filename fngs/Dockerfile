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
RUN pip install django==1.11.1
RUN pip install --ignore-installed cython coveralls wget sklearn networkx multiprocessing django-docs
RUN apt-get install python-dateutil

RUN git clone -b eric-dev-gkiar-fmri https://github.com/neurodata/ndmg.git /ndmg && cd /ndmg && python setup.py install

# clone the website repo and make the location for the downloads
RUN git clone https://github.com/ebridge2/FNGS_website.git && mkdir /FNGS_server && mkdir /FNGS_server/input_data && mkdir /FNGS_server/output_data

# setup the website
RUN cd /FNGS_website/fngs && python manage.py makemigrations $APP && python manage.py migrate && python manage.py migrate --run-syncdb 

RUN mkdir /FNGS_server/demo_data && cd /FNGS_server/demo_data && wget http://openconnecto.me/mrdata/share/demo_data/ndmg_func_cloud_demo.zip && unzip ndmg_func_cloud_demo.zip

# copy over the entrypoint script
COPY ./startfngs.sh /
ADD ./.vimrc .vimrc

# and add it as an entrypoint
ENTRYPOINT ["/startfngs.sh"]
