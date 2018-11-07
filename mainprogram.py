from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.io import export_png
import cv2
import numpy as np
import csv
import time
cap = cv2.VideoCapture('world.mp4')
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
area = int(width * height)
cv2.namedWindow('pupil')
frameCnt = 0
frames_Tatal = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = int(cap.get(cv2.CAP_PROP_FPS))
print(frames_Tatal,FPS)
def nothing(emp):
	pass
"""pos = int(frameCnt)
    cv2.getTrackbarPos('Time', 'pupil')
    cv2.setTrackbarPos('Time', 'pupil', pos)
    """
def mouse(event, x, y, flags, param):
    #if event == cv2.EVENT_MOUSEMOVE:
    if event == cv2.EVENT_RBUTTONDOWN:
        fromCenter = False
        global r
        #r = cv2.selectROI(frame, fromCenter)
        r = cv2.selectROI("pupil", frame, fromCenter)
        imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        print(r)
        #cv2.imshow("pupil", imCrop)
        cv2.waitKey(1)
        #cv2.imshow('pupil', frame)
        time.sleep(2.5)
        global RecROI
        RecROI += 1
        
with open('1013.csv', 'w',newline='') as out:
    reader = csv.reader(open('gaze_positions.csv', 'r'))
    writer = csv.writer(out)
    s=0
    for row in reader:
      s=s+1
      fin = s%4
      if fin == 1:
        writer.writerow(row)

with open('1013.csv', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        cv2.setMouseCallback('pupil', mouse)
        RecROI = 0
        gaze,g2aze,g3aze,g4aze = 0,0,0,0
        while(cap.isOpened()):                
          ret, frame = cap.read()
          if ret == False:
             break
          if RecROI == 1:
                block1 = r[0] + r[2]
                block2 = r[1] + r[3]
                block3 = r[0]
                block4 = r[1]
          if RecROI == 2:
                b2lock1 = r[0] + r[2]
                b2lock2 = r[1] + r[3]
                b2lock3 = r[0]
                b2lock4 = r[1]
          if RecROI == 3:
                b3lock1 = r[0] + r[2]
                b3lock2 = r[1] + r[3]
                b3lock3 = r[0]
                b3lock4 = r[1]
          if RecROI == 4:
                b4lock1 = r[0] + r[2]
                b4lock2 = r[1] + r[3]
                b4lock3 = r[0]
                b4lock4 = r[1]
          frameCnt = (frameCnt + 1)
          second=int(frameCnt/30)
          second_Tatal=int(frames_Tatal/30)
          cv2.createTrackbar('Time', 'pupil',second,second_Tatal,nothing)
          cv2.setMouseCallback('pupil', mouse)
          for row in rows:
            a = float(row['norm_pos_x'])*width
            b = (1-float(row['norm_pos_y']))*height
            #print(int(a),int(b),RecROI)
            if RecROI == 1:
                    """block1 = r[0] + r[2]
                    block2 = r[1] + r[3]
                    block3 = r[0]
                    block4 = r[1]
                    print(r[0],r[1],r[2],r[3])"""
                    if (int(a)>int(block3) and int(a)<int(block1)
                        and int(b)>int(block4) and int(b)<int(block2)):
                            gaze = gaze + 1
            if RecROI == 2:
                    if (int(a)>int(block3) and int(a)<int(block1)
                        and int(b)>int(block4) and int(b)<int(block2)):
                            gaze = gaze + 1
                    if (int(a)>int(b2lock3) and int(a)<int(b2lock1)
                        and int(b)>int(b2lock4) and int(b)<int(b2lock2)):
                            g2aze = g2aze + 1
            if RecROI == 3:
                    if (int(a)>int(block3) and int(a)<int(block1)
                        and int(b)>int(block4) and int(b)<int(block2)):
                            gaze = gaze + 1
                    if (int(a)>int(b2lock3) and int(a)<int(b2lock1)
                        and int(b)>int(b2lock4) and int(b)<int(b2lock2)):
                            g2aze = g2aze + 1
                    if (int(a)>int(b3lock3) and int(a)<int(b3lock1)
                        and int(b)>int(b3lock4) and int(b)<int(b3lock2)):
                            g3aze = g3aze + 1
            if RecROI == 4:
                    if (int(a)>int(block3) and int(a)<int(block1)
                        and int(b)>int(block4) and int(b)<int(block2)):
                            gaze = gaze + 1
                    if (int(a)>int(b2lock3) and int(a)<int(b2lock1)
                        and int(b)>int(b2lock4) and int(b)<int(b2lock2)):
                            g2aze = g2aze + 1
                    if (int(a)>int(b3lock3) and int(a)<int(b3lock1)
                        and int(b)>int(b3lock4) and int(b)<int(b3lock2)):
                            g3aze = g3aze + 1
                    if (int(a)>int(b4lock3) and int(a)<int(b4lock1)
                        and int(b)>int(b4lock4) and int(b)<int(b4lock2)):
                            g4aze = g4aze + 1
            cv2.circle(frame,(int(a),int(b)),5,(0,0,255),5)
            cv2.putText(frame, str(frameCnt), (1110,110), cv2.FONT_HERSHEY_DUPLEX,1.5
                        , (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow('pupil', frame)
            print(gaze)
            print("%.1f" % (gaze/30)+" -","%.1f" % (g2aze/30)+" -","%.1f" % (g3aze/30)+" -","%.1f" % (g4aze/30))
            break
          localtime = time.asctime(time.localtime(time.time()))
          c = cv2.waitKey(1)
          if c==27:
                  break
          elif c==32:
                  cv2.waitKey(0)
          elif c &0xFF == ord('s'):
                  
                  print(str(localtime.replace(' ', '').replace(':', ''))+'.png')
                  cv2.imwrite( str(localtime.replace(' ', '').replace(':', ''))+'.png',frame)
print("%.1f" % (gaze/30)+" -","%.1f" % (g2aze/30)+" -","%.1f" % (g3aze/30)+" -","%.1f" % (g4aze/30))

"""nm = int(input('請輸入秒數：'))
name = nm*30
da = cap.set(cv2.CAP_PROP_POS_FRAMES, name)
ret, frame = cap.read(da)
cv2.imshow('pupil', frame)x
c = cv2.waitKey(18)
if c &0xFF == ord('t'):"""
while True:
        
        shutdown = input('shutdown  y/n：')
        shutdown = shutdown.lower()
        if(shutdown=='y'or shutdown == 'yes'):
                cap.release()
                cv2.destroyAllWindows()
                break
        elif(shutdown=='n'or shutdown == 'no'):
                cap.release()
                cv2.destroyAllWindows()
                cap = cv2.VideoCapture('world.mp4')
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                area = int(width * height)
                cv2.namedWindow('pupil2')
                frameCnt = 0
                with open('1013.csv', newline='') as csvfile:
                        rows = csv.DictReader(csvfile)
                        while(cap.isOpened()):
                                nm = int(input('請輸入您需的區間起始秒：'))
                                nm2 = int(input('請輸入您需的區間終止秒：'))
                                name = nm*30
                                name2 = nm2*30
                                da = cap.set(cv2.CAP_PROP_POS_FRAMES, name)
                                ret, frame = cap.read(da)
                                if ret == False:
                                        break                        
                                second=int(frameCnt/30)
                                second_Tatal=int(frames_Tatal/30)
                                cv2.createTrackbar('Time', 'pupil2',0,1000,nothing)
                                
                                for row in rows:
                                    frameCnt = (frameCnt + 1)
                                    if frameCnt >= name and frameCnt <= name2 :
                                        a = float(row['norm_pos_x'])*width
                                        b = (1-float(row['norm_pos_y']))*height
                                        cv2.circle(frame,(int(a),int(b)),15,(47,252,182),2)
                                        cv2.imshow('pupil2', frame)
                                        
                                localtime = time.asctime(time.localtime(time.time()))
                                cv2.imwrite( str(localtime.replace(' ', '').replace(':', ''))+'.png',frame)
                                c = cv2.waitKey(1)
                                if c==27:
                                    break
                                elif c==32:
                                    cv2.waitKey(0)
                                elif c &0xFF == ord('s'):
                                    print(str(localtime.replace(' ', ''))+'.png')
                                    cv2.imwrite( str(localtime.replace(' ', '').replace(':', ''))+'.png',frame)
                                break
                break
                """time.sleep(5)
                shutdown = input('Press Enter to shutdown：')
                if(shutdown==''):
                    cap.release()
                    cv2.destroyAllWindows()"""
        else:
                print("Error,Please input [y/n]")
                continue

output_file("colormapped_bars.html")
Gazing = ['Region1', 'Region2', 'Region3', 'Region4']
times = [(gaze/30), (g2aze/30), (g3aze/30), (g4aze/30)]

source = ColumnDataSource(data=dict(Gazing=Gazing, times=times))

p = figure(x_range=Gazing, plot_height=450, toolbar_location=None, title="Gazing times")
p.vbar(x='Gazing', top='times', width=0.9, source=source, legend="Gazing",
       line_color='white', fill_color=factor_cmap('Gazing', palette=Spectral6, factors=Gazing))

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.y_range.end = 25
p.legend.orientation = "horizontal"
p.legend.location = "top_center"
show(p)
