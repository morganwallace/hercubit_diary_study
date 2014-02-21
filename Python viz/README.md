#Python Viz

*This README explains how to use the 'Hercubit' Python visualizations in the 'Python Viz' folder.*

**Start by using pip to setup dependencies:**

`` $ pip install -r requirements.txt``

****
#####double check...
Make sure to run **xyz_out_micro.ino** on the ardiuno and connect it via USB or Bluetooth before executing Python scripts in this directory.
#####FYI
All scripts in the **Python Viz/** folder call the **hercubit/** modules for standard functions and settings.

----

##Server (with web sockets)

|File|Description|
|-------|
|app.py|Flask server using FlaskSockets-IO to send data back and forth.|
|templates/index.html|Web page rendered when app.py is run. Uses javascript to send and receive with web sockets.|



---
##Animations
####animation_XYZ_Gs_movingWindow.py
Plots x, y, and z acceleration in gs over time (seconds). The animation window moves as time proceeds.
####saved_animations_and_data.py
Similar to the previous script, x, y, and z acceleration in gs is plotted for 30 seconds and then saved in the ``saved_animations_and_data`` directory and then in a timestamped folder with:

1. CSV file
2. Python pickle file 
3. PNG image of graph

####barchart.py
Bar graph counting bicep curls.

 

##hercubit/


| Modules in hercubit | Description|
|---------|---|
|``settings.py``|configures settings like: Serial port, sample rate, etc|
|``device.py``|Creates a serial connection to the device and pulls accelerometer data out one sample at a time, using ``acc_data()`` - call this function in a loop for each sample rate|
|``peak_detect.py``|Detects peaks and dips (pattern recognition) in accelerometer data and output. Will count repititions with free weights|
|``example_using_peak_detect.py``|Shows how importing ``peak_detect.py`` works|
|naive_bayes_detect.py|...coming soon|
