# BIDS-Conveter-CO-REG

**Compatibility**
This program is built using python 3.14.2
Using it, or the executeble through a terminal with a 
different version might cause problems.

ubunty 22.04


**Using the program**
In this project you will find a foldder named APP, and inside different versions
of the app version of this program can be fund. 
Under each opperating system folder there is a "dist", and inside is the app.

The program will open on the coregistration page. To switch pages, open the "Mode" 
menu at the topp and select "Bids Conversion". 
In that page, enter your input folder, your output folder, and any setting you
might want to change. Then press "Run".

**Instructions for building the project as an app:**
The program is made to be packaged into apps for
windows, mac, and linux. This was done using pyinstaller

For mac, use the terminal command:
pyinstaller \
  --osx-bundle-identifier se.ki.kex26.bidsandcoreg \
  --collect-datas bidsschematools \
  --add-data "/opt/anaconda3/envs/BIDS_and_coreg/lib/python3.14/site-packages/ci_info/vendors.json:ci_info" \
  --collect-datas etelemetry \
  --add-binary "/opt/anaconda3/envs/BIDS_and_coreg/bin/dcm2niix:." \
  --add-binary "/opt/anaconda3/envs/BIDS_and_coreg/bin/deno:." \
  --onedir \
  --windowed \
  --clean \
  --name "Bids_and_coreg" \
  --icon=Prel_BIDS_icon.ico \
  main.py
  

For Windows, use the terminal command:
pyinstaller `
  --collect-datas bidsschematools `
  --add-data "C:\Users\**\anaconda3\Lib\site-packages\ci_info\vendors.json;ci_info" `
  --collect-datas etelemetry `
  --add-binary "C:\Users\**\anaconda3\envs\BIDS_and_coreg\Library\bin\dcm2niix.exe;." `
  --onedir `
  --windowed `
  --runtime-hook ".\pyi_fix_stdio.py" `
  --clean `
  --name "Bids_and_coreg" `
  --icon "Prel_BIDS_icon.ico" `
  main.py

For Linux, use the terminal command:
Linux: 
    python -m PyInstaller \
      --collect-datas bidsschematools \
      --collect-datas etelemetry \
      --collect-all openpyxl \
      --add-data "/home/**/miniconda3/envs/BIDS_and_coreg_linux/lib/python3.11/site-packages/ci_info/vendors.json:ci_info" \
      --add-binary "$(which dcm2niix):." \
      --add-binary "$CONDA_PREFIX/lib/libexpat.so.1:." \
      --onedir \
      --runtime-hook ./pyi_fix_stdio.py \
      --clean \
      --name "Bids_and_coreg_linux" \
      main.py

Remember to replace "--add-data" and "--add-binary" paths with your 
coresponding paths to: deno, dcm2niix, and vendors.json



