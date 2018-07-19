# WUSC-KEEP
This repository contains Dockerised data pipeline stages for the WUSC-KEEP project, and a collection of Bash scripts
for executing both those stages and the SMS platform data fetcher over WUSC-KEEP data.

## Usage
### Prerequisites
#### Tools
Install Python 3.6+, Pipenv, and Docker.

#### SMS Fetcher
The data fetching stages of the pipeline require access to a local copy of the 
[Echo Mobile fetcher](https://github.com/AfricasVoices/EchoMobileExperiments) project.
To configure this:
 
1. Clone that repository to your local system:

   `$ git clone https://github.com/AfricasVoices/EchoMobileExperiments.git`
   
1. Checkout the appropriate commit for this project:

   `$ git checkout 423fecc4325b5f5d6852699cb4608bb7dd5cf446`  # TODO: Tag EchoMobileExperiments appropriately
   
1. Install project dependencies:
   ```bash
   $ cd EchoMobileExperiments
   $ pipenv --three
   $ pipenv sync
   ```
   
1. When using the fetch scripts in `run_scripts/`, set the `<echo-mobile-root>` argument to the absolute path 
   to the directory just cloned. For example:

   `$ sh 01_fetch_messages.sh test_user /Users/test_user/EchoMobileExperiments ...`

#### Data Directory
All the run scripts take a `<data-root>` argument. This should be a path to an initially-empty directory.
Each run script will populate this directory with intermediate subdirectories and data-files.

### Running
Scripts to run each stage of the pipeline are provided in `run_scripts/`.

To run each script, first run `$ sh <script-name.sh>` to get help on the arguments it expects.
Then set those arguments appropriately to run that pipeline stage.

Each script populates the data directory with one or more subdirectories of outputs.
Scripts are prefixed with the numbers of the directories they output to.

To run the whole pipeline, run each script in run_scripts in ascending order of the numeric prefixes.
