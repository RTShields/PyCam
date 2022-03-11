# PyView
# Created by John Palmer
# Coded on 2022 03 10 - Happy MAR10!
#
# A utility to view and save frames from any available camera

import os
import datetime as dt
import cv2 as cv
# ########################## Cam Check ######################## #


def CamViewer(Clist):
    # Cycle through the list of available views and allow the selection of one, return selection
    cycle = True
    while cycle is True:
        for cam in Clist:
            title = 'Camera ' + str(cam)
            view = cv.VideoCapture(cam)
            cv.namedWindow(title)
            while True:
                ret, frame = view.read()
                k = cv.waitKey(1) % 265
                if k == 32 or k == 26:
                    cycle = False
                    return cam

                x = cv.waitKeyEx(5000)
                if x == 2555904:
                    break


def CamCheck():
    # Find all available cameras and allow the choosing of one for settings
    settings = 'App/settings.dll'
    if os.path.isfile(settings) is False:
        cameras = []
        for view in range(10):
            cap = cv.VideoCapture(view)
            if cap is None or not cap.isOpened():
                pass
            else:
                cameras.append(view)
        if len(cameras) == 0:
            print("Error: No cameras are connected or installed on machine.\n\n")
            return
        elif len(cameras) == 1:
            return cameras[0]
        else:
            CamNum = CamViewer(cameras)
            return CamNum
# ######################## Check DLL ########################## #


def CheckDll():
    # ### Check to make sure all the needed modules are installed.
    # ### At the end, set up a network drive for the repository.
    settings = 'App/settings.dll'
    if os.path.isfile(settings) is False:
        with open('setup.bat', 'w') as start:
            start.write('python.exe -m pip install --upgrade pip\n')
            installs = ['opencv-python', 'tkinter']
            for mod in installs:
                start.write('pip install ' + mod)
            start.write("net use p: \\RPiBridge\\Photos /user:Tech $74rl1gh7 /persistent:Yes")
            start.close()

    # ### Create a settings.dll file
    if os.path.isfile(settings) is False:
        with open(settings, 'w') as dll:
            save = 'P:/'
            if os.path.isdir(save) is False:
                dll.write('DestDrive:C\n')
            else:
                dll.write('DestDrive:P\n')
            dll.write('CamSet=' + CamCheck())
            dll.close()
# ########################## Get Date ######################### #


def getDate(split):
    # Get the current time from the computer, and serve it up to multiple calls
    t = dt.datetime.today()
    now = str(t)

    tspace = now.find(" ")
    date = now[:tspace]
    time = now[tspace + 1:]

    # ### Break down date into yy/mm/dd components
    dbreaks = []
    for c in range(len(date)):
        if date[c] == '-':
            dbreaks.append(c)
    YYYY = date[:4]
    MM = date[dbreaks[0] + 1: dbreaks[1]]
    DD = date[dbreaks[1] + 1:]

    # ### Breate down time in to components
    tbreaks = []
    for t in range(len(time)):
        if time[t] == ':' or time[t] == '.':
            tbreaks.append(t)
    HR = time[:tbreaks[0]]
    MN = time[tbreaks[0] + 1: tbreaks[1]]
    SC = time[tbreaks[1] + 1: tbreaks[2]]
    MS = time[tbreaks[2] + 1: tbreaks[2] + 3]
    timestamp = HR + MN + '-' + SC + MS

    if split == "CW":
        return date  # , file, timestamp
    elif split == "FC":
        FC = [YYYY, MM, DD, HR]
        return FC
    elif split == "TS":
        return timestamp
# ####################### Folder Check ######################## #


def NumCheck(num):
    # Check to see if the string is a double or single digit, return int
    if num[0] == "0":
        return int(num[1])
    else:
        return int(num)


def FolderCheck(drive):
    # Check for destination path, generate time-based folders as needed
    Calendar = {1: '01-Jan', 2: '02-Feb', 3: '03-Mar', 4: '04-Apr', 5: '05-May', 6: '06-Jun', 7: '07-Jul', 8: '08-Aug', 9: '09-Sep', 10: '10-Oct', 11: '11-Nov', 12: '12-Dec'}
    Clock = {7: '07 AM', 8: '08 AM', 9: '09 AM', 10: '10 AM', 11: '11 AM', 12: '12 PM', 13: '1 PM', 14: '2 PM', 15: '3 PM', 16: '4 PM', 17: '5 PM', 18: '6 PM'}
    Checks = getDate("FC")
    Netdrive = drive + ':/DentCapture'
    # ### Check to see if the P:/ drive is available
    if os.path.isdir(Netdrive) is False:
        os.mkdir(Netdrive)
    s = '/'

    # ### Test for Year folder, otherwise make one
    Ypath = Netdrive + s + Checks[0]
    if os.path.isdir(Ypath) is False:
        os.mkdir(Ypath)

    # ### Test for Month folder, otherwise make one
    Mpath = Ypath + s + Calendar[NumCheck(Checks[1])]
    if os.path.isdir(Mpath) is False:
        os.mkdir(Mpath)

    # ### Test for Day folder, otherwise make one
    Dpath = Mpath + s + Checks[2]
    if os.path.isdir(Dpath) is False:
        os.mkdir(Dpath)

    # ### Test for ToD folder, otherwise make one
    hour = NumCheck(Checks[3])

    if hour > 18:
        Hpath = 'After Hours/'
    elif hour < 7:
        Hpath = 'Before Hours/'
    else:
        Hpath = Clock[hour]

    Fpath = Dpath + s + Hpath
    if os.path.isdir(Fpath) is False:
        os.mkdir(Fpath)

    return Fpath
# ########################## Cam Win ########################## #


def SetCheck():
    settings = 'App/settings.dll'
    lines = []
    with open(settings, 'r') as check:
        for cfg in settings:
            lines.append(cfg)
        check.close()
    drive_line = lines[0]
    drive_letter = drive_line[-1]
    return drive_letter


def CamWin():
    # Create a window to get the video feed, take photos
    CamSet = CheckDll()
    if CamSet is None:
        CamSet = 0
    date = getDate("CW")

    # ### Craft Window Title
    computer = os.environ['COMPUTERNAME']
    user = 'Op' + str(computer[-1])
    title = user + ' on ' + date

    # ### Set up livefeed
    #view = cv.VideoCapture(0)
    cam = cv.VideoCapture(0, cv.CAP_DSHOW)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    cv.namedWindow(title)

    # ### Set up Esc and Space (Trigger) keys
    while True:
        ret, frame = cam.read()
        cv.imshow(title,frame)
        if not ret:
            print('Failed to grab frame - camera not found.')
            break
        else:
            k = cv.waitKey(1) % 256
            if k == 27:  # Esc is pressed
                break
            if k == 32 or k == 26:  # Space/trigger is hit
                Fname = getDate('TS')
                file = user + '-' + Fname + '.jpg'
                filepath = FolderCheck('C')
                filesave = filepath + '/' + file
                cv.imwrite(filesave, frame)
                os.startfile(filesave, "open")
                if os.path.isdir('P:/') is True:
                    backuppath = filepath.replace('C:/', 'P:/') + '/' + file
                    cv.imwrite(backuppath, frame)
    cam.release()
    cv.destroyAllWindows()


CamWin()
