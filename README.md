# Open Source Project Stock Trading
web-based technical screener for candlestick patterns using TA-Lib, Python, and Flask

Windows
Download the Anaconda Installer:
Go to the Anaconda Distribution page.
Download the Windows installer.
Run the Installer:
Double-click the downloaded .exe file.
Follow the installation instructions. You can choose to add Anaconda to your PATH, but it’s often recommended to use the Anaconda Prompt.
Verify Installation:
Open the Anaconda Prompt and type:
bash
Copy code
conda --version

macOS
Download the Anaconda Installer:
Visit the Anaconda Distribution page.
Download the macOS installer.
Run the Installer:
Open a terminal and navigate to the directory where you downloaded the installer.
Run the installer using:
bash
Copy code
bash Anaconda3-*.sh
Follow the on-screen instructions.
Verify Installation:
Type the following in your terminal:
bash
Copy code
conda --version

Linux
Download the Anaconda Installer:
Go to the Anaconda Distribution page.
Download the Linux installer.
Run the Installer:
Open a terminal and navigate to the download location.
Execute the installer:
bash
Copy code
bash Anaconda3-*.sh
Follow the prompts during installation.
Verify Installation:
Check the installation by running:
bash
Copy code
conda --version


*clone the repository locally and run these commands 
* curl -O https://repo.anaconda.com/archive/Anaconda3-2023.03-MacOSX-x86_64.sh
* bash Anaconda3-2023.03-MacOSX-x86_64.sh
* restart terminal
* conda env create -f environment.yml
* conda activate finance_env
* flask run


*other commands

python3.10 -m venv env

source env/bin/activate

pip install -r requirements.txt

flask run
