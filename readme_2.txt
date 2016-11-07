test
This Python program is used to download PDF spec from PDP automatically for NVPNs listed in nvpn.csv file.
It's tested in Windows7 with Python3.5. 

Basic PDP access follows below wiki:
https://wiki.nvidia.com/gpuboardsolutions/index.php/Windchill10/Script_to_Login_to_and_Download_from_PDP
And this program focus on automation batch download.

- SW Requirement (Windows):
1. Python3 installed
2. necessary python module installed


- Input
1. nvpn.csv file in the same folder of download_pdf.py
	The NVPN list is in nvpn.csv file, with "Name" colum for NVPN and "Manufacturer Part Number" colum for mfg PN. The firt row of csv file must contain "Name" and "Manufacturer Part Number", which is default name when export BOM from PDP. Other colums are not required but won't affect the program run if they are kept in the .csv file.
	Suggest export BOM from PDP, remove unnecessary items, and save it as .csv file. 
	An example .csv file is attached for reference.(to simplify, the unncessary colums are removed, but it's not required for your .csv file).


- Output
1. spec PDF are downloaded in to "download" folder
2. log file in "log' folder record NVPNs and reasons for which failed to download spec

- Usage
1. run command line 'python download_pdf.py'
2. input PDP username and password
3. wait download finish, the status can be monitored in console output

