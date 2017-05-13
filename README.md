# herbalife website
## adaptatif template website

This repo contains an adaptatif template website for a herbalife seller. It is written with Python2, bootstrap, Flask,Flask-mail and Jinja2.

#### Dependancies
- Python 2
- Flask
- Flask mail

### Initialization

#### To launch the server (Back-end)
After installing dependencies, and editing config parameter in server_vanilla.py:

        $ chmod +x server_vanilla.py
        $ ./server_vanilla.py

#### How to use it (Front-end)

Once the server is up, type in your browser's URL bar the URL displayed in the terminal after executing last command.
Per default, it should be <http://localhost:8084> but may change depending on your flask configuration.

##### Create a network

Once connected, click on 'new analysis' in the top right corner and fill up inputs form and upload your .faa input file.
Please refer to EGN documentation for input value.
- Don't forget to enter your mail adress to get back your zip archive (containing all outputs files) when analysis is done.
- Be aware that starting several runs (with different parameters) on the same input file will return a zip archive that also contains all previous outputs analysis for this input file.


##### Visualize a network

After receiving zip archive, reconnect to EGNize page, click on "load a network" button and upload a json or gexf file.
After clicking on ok, modal should close and visualization tool should display your network.
Report to the 'Actual available interaction' section above for possible interactions.


