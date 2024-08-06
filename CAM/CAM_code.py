import pandas as pd

cam = pd.read_excel("CAM_base.xlsx")
print(cam)
print(cam.columns)

van_num = int (input("Введите номер вагона: "))
cam_cam = cam[cam["van_num"] == van_num]
print(cam_cam)

print(f'''"IP Cam1" - {cam_cam["Cam1"]},
"IP Cam2" - {cam_cam["Cam2"]},
"IP Cam3" - {cam_cam["Cam3"]},
"IP Cam4" - {cam_cam["Cam4"]},
"IP bes1" - {cam_cam["bes1"]},
"IP bes2" - {cam_cam["bes2"]},
"IP bes3" - {cam_cam["bes3"]},
"IP bes4" - {cam_cam["bes4"]},
''')

