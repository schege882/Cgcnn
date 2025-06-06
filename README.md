#  Crystal Graph Convolutional Neural Network (CGCNN) Tutorial 2

## Step 1: Download and Install Anaconda

* Go [here](https://www.anaconda.com/download) and enter your email. You'll receieve a donload link in your email.

* Once you've successfuly downloaded the `Anaconda3-2024.10-1-Linux-x86_64.sh` file, install it with,

   `$ bash Anaconda3-2024.10-1-Linux-x86_64.sh`
   
and follow the given prompts.

## Step 2: Install and configure CGCNN
* Upgrade conda
  `$ conda upgrade conda`
  
* Install prerequisites and CGCNN
  `$ conda create -n cgcnn python=3 scikit-learn pytorch torchvision pymatgen -c pytorch -c conda-forge`
  
* Activate `cgcnn` conda environment
  `$ conda activate cgcnn`
 
  `$ conda install -c conda-forge mp-api `

* Clone the cgcnn repo from github;
`$ git clone https://github.com/txie-93/cgcnn.git`

## Step 3: Using cgcnn
### Step 3.1: Prepare data
* Go to the cloned repository
    `$ cd cgcnn`

* Inside the `data` directory, create a new directory with anyname, in this case `formation_energy` 
`$ cd data`
`$ mkdir formation_energy-trained`
`$ cd formation_energy`
and inside it have the following files:
    1. `CIF` files having the format *ID.cif*
    2. `id_prop.csv` which contains material id and property we want to predict in the first and second column respectively.
    3. `atom_init.json` a JSON file that stores the initialization vector for each element. This `data/sample-regression/atom_init.json` file should be good for most applications.

* The `CIF` and `id_prop.csv` files can be obtained by editing `generateCIF.py` file appropriately to suit your needs and then running;
    `$ python3 generateCIF.py`
    
* The `atom_init.json` file can be obtained by;
    `$ cp ../sample-regression/atom_init.json .`

### Step3.2: The Util directory
* Create a `Util` directory at the root of the `cgcnn` directory to store utility scripts and data.
 `$ mkdir Util`
 
* In the `data/formation_energy` directory, move the `generateCIF.py` and `full_dataset.csv` files to the newly created `Util` directory.
    `$ mv generateCIF.py ../../Util/`
    `$ mv full_dataset.csv ../../Util/`

### Step 3.3: Train data
* To train the model;
`$ python main.py --train-ratio 0.6 --val-ratio 0.2 --test-ratio 0.2 path/to/data/formation_energy 2>&1 | tee training.log `

* To proceed with the calculation after an interuption;
` $ python3 main.py --train-ratio 0.6 --val-ratio 0.2 --test-ratio 0.2 data/formation_energy/ --resume checkpoint.pth.tar 2>&1 | tee training.log `

* After training, you will get three files in `cgcnn` directory;
    1. `model_best.pth.tar`: stores the CGCNN model
        with the best validation accuracy.
    2. `checkpoint.pth.tar`: stores the CGCNN model 
        at the last epoch.
    3. `test_results.csv`: stores the ID, target 
        value, and predicted value for each crystal
        in test set.
### Step 3.4: Predict material properties
* In the `data` directory create a new directory (in this case `formation_energy_prediction` ) and inside it have the `CIF` files, the `atom_init.json` and the `id_prop.csv` file.
* Run the following command at the root of `cgcnn` directory;
    ` $ python3 predict.py post-processing/model_best.pth.tar data/formation_energy_prediction/ 2>&1 | tee formation_energy_prection.log`
    
* All the output from running the training and prediction is contained in the `post-processing` directory.

* After predicting, you will get one file in `cgcnn` directory:
    1. `test_results.csv`: stores the ID, target value, and predicted value for each crystal in test set. Here the target value is just any number that you set while defining the dataset in `id_prop.csv`, which is not important.
    

For more info see the github repo by Tian Xie [here](https://github.com/txie-93/cgcnn) and the article on [arXiv](https://arxiv.org/abs/1710.10324) .