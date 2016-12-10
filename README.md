# FNGS_website

# Tutorial

## Getting the Pipeline Running

[Using the Pipeline](#pipeline)

### ## Pipeline Use<a name="pipeline"></a>
```
git clone https://github.com/ebridge2/FNGS_website.git
cd FNGS_website
docker build --no-cache -t <your-handle>/fngs .

# -v argument allows your container to use data that is only available locally. Ie, in this case, the data in
# /local/path/to/your/data/ would be visible inside the docker container at /data
docker run -ti -v /local/path/to/your/data/:/data --entrypoint /bin/bash <your-handle>/fngs
# otherwise, you can just skip the -v flag entirely if you plan to use the demo data
docker run -ti --entrypoint /bin/bash <your-handle>/fngs

# takes you into the docker container
cd /ndmg/ndmg/scripts/
# runs the demo
./ndmg_demo-func.sh
```

### Building Docker Container for Web Use

Note that this guide is very similar to the preceeding guide, except now we need to forward ports when we use the docker container.
```
git clone https://github.com/ebridge2/FNGS_website.git
cd FNGS_website
docker build --no-cache -t <your-handle>/fngs .

# -v argument allows your container to use data that is only available locally. Ie, in this case, the data in
# /local/path/to/your/data/ would be visible inside the docker container at /data
docker run -ti -v /local/path/to/your/data/:/data -p <portnum>:<portnum>  --entrypoint /bin/bash <your-handle>/fngs
# takes you into the docker container
# otherwise, you can just skip the -v flag entirely if you plan to use the demo data
docker run -ti -p <portnum>:<portnum> --entrypoint /bin/bash <your-handle>/fngs

cd /ndmg/ndmg/scripts/
# runs the demo to make sure things work
./ndmg_demo-func.sh

# proceed to tutorial below about setting up the server
```

### Pulling Docker Container from Remote
```
docker pull ericw95/fngs:0.0.3

# -v argument allows your container to use data that is only available locally. Ie, in this case, the data in
# /local/path/to/your/data/ would be visible inside the docker container at /data
docker run -ti -v /local/path/to/your/data/:/data -p <portnum>:<portnum> --entrypoint /bin/bash ericw95/fngs:0.0.3
# otherwise, you can just skip the -v flag entirely if you plan to use the demo data
docker run -ti -p <portnum>:<portnum> --entrypoint /bin/bash <your-handle>/fngs


# takes you into the docker container


cd /ndmg/ndmg/scripts/
./ndmg_demo-func.sh
# runs the demo

# proceed to tutorial below about setting up the server
```

### Local Setup Tutorial

Note that in order for this to work, you need to have FSL version 0.5.9 configured on your local machine (non-intuitive for non Red Hat distributions). This path is not recommended unless you have experience installing FSL on non-RH Linux distributions. 

```
git clone https://github.com/neurodata/ndmg.git
cd ndmg/
python setup.py install
cd ndmg/scripts
# confirm that the pipeline runs without error
./ndmg_demo-func.sh

cd ../../../
git clone git@github.com:ebridge2/FNGS_website.git

mkdir /FNGS_server # the server expects this directory
cd /FNGS_server
wget http://openconnecto.me/mrdata/share/demo_data/less_small_atlases.zip
unzip less_small_atlases.zip # puts atlases we expect to have in the correct spot

# proceed to tutorial below about setting up the server
```

## Server Tutorial

Now that we have the pipeline working, we can try to get some scans uploaded and analyzed for visualization and downloading through the web service. From inside the docker container (or, if you installed locally, from the website folder):
```
$ cd /FNGS_website/fngs # (if installed locally, cd FNGS_website/fngs from wherver the FNGS_website repo is cloned)
$ python manage.py runserver 0.0.0.0:<portnum> # puts the server up on 0.0.0.0:<portnum> for whatever port you choose
Performing system checks...

System check identified some issues:

WARNINGS:
?: (urls.W001) Your URL pattern '^$' uses include with a regex ending with a '$'. Remove the dollar from the regex to avoid problems including URLs.

System check identified 1 issue (0 silenced).
December 07, 2016 - 20:33:52
Django version 1.10.4, using settings 'fngs.settings'
Starting development server at http://localhost:8000/ # this line tells you where to go to open the service, or just click
Quit the server with CONTROL-C.
```
Following the link given by the service will take you to the home page:
![FNGS Homepage](https://cloud.githubusercontent.com/assets/8883547/20985816/12fabc48-bc94-11e6-90d8-d74aa0e1bf70.png)
Click the link above to take you to the "Analyze" Tab.

Let's run through a quick demonstration of how the web service can be used with a real example. You should see that no datasets are available for viewing. To begin, let's click the add-dataset button. 
![Add Dataset](https://cloud.githubusercontent.com/assets/8883547/20985885/5a9c76d6-bc94-11e6-9233-40a213f95f38.png)

I've added some text for the Dataset's ID as well as the collection site name. Once we've added this information, add the dataset.
![Add new dataset](https://cloud.githubusercontent.com/assets/8883547/20985939/91cdee96-bc94-11e6-964f-5418486149dc.png)

Next, let's upload a subject for analysis:
![Add subject](https://cloud.githubusercontent.com/assets/8883547/20985966/ae843946-bc94-11e6-9bfa-2e299a859e6b.png)

Before we add any information here, let's return to a new terminal window and download some demo data.

```
cd /tmp/
wget http://openconnecto.me/mrdata/share/demo_data/full_demo_func.zip # this might take a few seconds to download
unzip full_demo_func.zip
# if you would prefer to use smaller data, make sure to use the appropriate functional scan and anatomical scan
wget http://openconnecto.me/mrdata/share/demo_data/small_demo_func.zip
unzip small_demo_func.zip
```
This gives us 2 subjects, and 2 trials per subject, of demo data to play around with. Next, let's go back to the website, and fill out the required information for the subject. I chose subject 0025864, scan 1, for this demo. As you can see, we will need to include the functional scan and the structural scan, which can be found at the path "/tmp/full_func/BNU1/sub-0025864/session-1/func/sub-0025864_session-1_bold.nii.gz" and "/tmp/full_func/BNU1/sub-0025864/session-1/anat/sub-0025864_session-1_T1w.nii.gz" respectively  (assuming you downloaded the .zip file to the /tmp/ directory):

![Choosing Functional Scan](https://cloud.githubusercontent.com/assets/8883547/20987531/0da6906c-bc9b-11e6-83cd-d19fbbba9550.png)
![Choosing Anatomical Scan](https://cloud.githubusercontent.com/assets/8883547/20987510/f4879f7c-bc9a-11e6-8da4-287261324d01.png)

Note that I also went ahead and selected the Structural scan type (T1w) and the Slice Timing Method (Interleaved). Information about the structural scan type is necessary to ensure that when we segment our anatomical image into different brain tissues for nuisance correction, we know what sorts of intensities to look for (ie, white matter looks different in T1w than T2w). Slice timing acquisition is a measure of the acquisition sequence in which the image is acquired. This is unique to the individual dataset, so see the dataset release information if you are not sure which to choose (or, just leave this blank and select "None" in which slice timing correction will not be performed). 

Finally, once you have the entire form filled out, click to add the subject, and wait a few seconds while the upload commences.
![Add the subject](https://cloud.githubusercontent.com/assets/8883547/20987564/2d09fe44-bc9b-11e6-9f48-b15358c63fae.png)

Note that the web service does not yet have a queuing system, so the next steps require care when uploading your scans for analysis. Take great care not to click the analyze button twice (before the previous analysis is completed and the results are vieweable and downloadable) or delete while an analysis is taking place. This is because the lack of a queuing system means that jobs are just spawned in process modules (a naive, short term solution), so processes are run disconnected from the python session, and analyzing again will spawn new processes over the existing ones (leading to processes being overallocated, and probably crashing the program), and in the case of deletes, leading to processes spontaneously crashing (and probably also crashing the program). Additionally, there is not yet a feature to update your subjects after you upload the data, so if you upload something mistakenly, just delete it and start over. These features are already on the backlog for second semester, so hopefully it will be a lot smoother in the near future.

Next, click to analyze your data (ONCE). 
![Analyze Your data](https://cloud.githubusercontent.com/assets/8883547/20987602/4f9297aa-bc9b-11e6-83cc-d72b646275da.png)

Note that it may be tempting to reload this page because it looks like nothing happened. DON'T (I've done it a bunch of times; the fix if you accidentally do this is below to reset the database)! You will notice that the URL at the top will end with "/analyze/". This means that reloading the page will cause analysis to begin a second time, which will cause the two analyses to conflict and could lead to epic-fail as described above. Give the program a little bit of time, and maybe in the meantime, check out the algorithms section to look at the workflow and pseudo code provided.

Note that you can check on the progress of your run by keeping the terminal you used to start the server open on the side. When the run is finished, you will see a screen something like the one below:
![Run Complete](https://cloud.githubusercontent.com/assets/8883547/20987885/56b9bc2e-bc9c-11e6-8c00-0556af08d168.png)

Now, navigate over to the "explore" tab and we can see all of the cool stuff our pipeline made. Click the dataset, and you should see the subject as below. Feel free to download the data, but for now we'll look at the pretty QC page. 

![View Data](https://cloud.githubusercontent.com/assets/8883547/20987934/84544d98-bc9c-11e6-9b81-3fec18f226bc.png)

And voila! This tutorial is now complete. Feedback can be left in the form of git issues, and if you have any recommendations or things that you'd like to see incorporated into the pipeline (anything from specific fMRI processing techniques to helpful web dev frameworks) I'm all ears. Thanks!

### For people who felt the need to reload the analysis page (like me! the sad thing is I've done it a bunch of times)

If you accidentally reload the analysis page or something gets screwed up, I've had the best luck instead of trying to figure out how messed up it is and going from there, just resetting the service entirely. Go to the directory where you have the website installed:
```
cd /FNGS_website/fngs # if on the docker container, it will be right here
python manage.py flush # Removes all data from the database, but does not touch the existing tables
rm -rf /FNGS_server/input_data # deletes the existing data... goodbye! 
rm -rf /FNGS_server/output_data
cd /FNGS_website/fngs
python manage.py 0.0.0.0:8000 # should be back up and good to go again
```
