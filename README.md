# BIDS-Conveter-CO-REG




**Instructions for using the code through terminal**
Because the code is made to be built into an app, some 
program calls don't work when launching through the edditor.

We have included both versions of the code, but commented 
one version out. So to make it work just comment out one version
and remove comment the other. They are labled.

In packages.Elliot.UI_CO_REG: 
    between line 2826 - 2939
In packages.Manfred_and_Sofia.File_handling.Analyze_and_Convert_Subject: 
    between line 229 - 240

**Instructions for building the project as an app:**
The program is made to be packaged into apps for
windows, mac, and linux. This was done using pyinstaller

For mac, use the terminal command:
pyinstaller \
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

Remember to replace "--add-data" and "--add-binary" paths with your 
coresponding paths to: deno, dcm2niix, and vendors.json



