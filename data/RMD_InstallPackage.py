import os
os.system("title RMD_InstallPackages")

package_list = ["json", "textual", "datetime", "termcolor", "Imath", "asciichartpy", "plotext", "threading", "json", "colorama", "OpenEXR", "subprocess", "time", "numpy"]
for package in package_list:
	os.system("python -m pip install %s"%package)

print("Package installation done !")
os.system("pause")