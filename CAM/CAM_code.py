import pandas as pd

cam = pd.read_excel("CAM_base.xlsx")
print(cam)
print(cam.columns)

van_num = int (input("Введите номер вагона: "))
cam_cam = cam[cam["van_num"] == van_num]
print(cam_cam)

cam_cam.index = range(0,1)

print(f'''"IP Cam1" - {cam_cam["Cam1"][0]},
"IP Cam2" - {cam_cam["Cam2"][0]},
"IP Cam3" - {cam_cam["Cam3"][0]},
"IP Cam4" - {cam_cam["Cam4"][0]},
"IP bes1" - {cam_cam["bes1"][0]},
"IP bes2" - {cam_cam["bes2"][0]},
"IP bes3" - {cam_cam["bes3"][0]},
"IP bes4" - {cam_cam["bes4"][0]}.
''')


