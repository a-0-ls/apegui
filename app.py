import sys
import matplotlib as plt

#matplotlib.use('Agg')
import os
os.environ['DLClight'] = 'True'
import deeplabcut
if 'tkinter' not in sys.modules:
    from tkinter import *
import ffmpeg, subprocess
from tkinter import *
import tkinter as Tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import *
from tkinter.filedialog import askdirectory
import csv, glob, pandas as pd
from tkmacosx import Button

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.pyplot
from matplotlib.pyplot import subplots
import shutil
import numpy as np


# In[3]:


root = Tk()
root.title('Grooming Hand Clasp')
#root.iconbitmap('/Users/aishu/ape.icns')
root.geometry('600x600')
root.resizable(width=False, height=False)

n = ttk.Notebook(root)
n.pack(pady=5, padx=5)


f1 = Frame(n, width=550, height=550, bg='DarkGoldenrod2')
f2 = Frame(n, width=550, height=550, bg='DarkGoldenrod2')
f3 = Frame(n, width=550, height=550, bg='DarkGoldenrod2')
f4 = Frame(n, width=550, height=550, bg='DarkGoldenrod2')
f5 = Frame(n, width=550, height=550, bg='DarkGoldenrod2')

f1.pack(fill='both', expand=True)
f2.pack(fill='both', expand=True)
f3.pack(fill='both', expand=True)
f4.pack(fill='both', expand=True)
f5.pack(fill='both', expand=True)


f1.pack_propagate(False)
f2.pack_propagate(False)
f3.pack_propagate(False)
f4.pack_propagate(False)
f5.pack_propagate(False)


n.add(f1, text='Downsample')
n.add(f2, text='Analyze')
n.add(f3, text='Detect')
n.add(f4, text='Classify')
n.add(f5, text='Analyze2')

text_widget1 =Label(f1,text= "This will downsample the videos to: 532px * 300px",fg='black',bg='DarkGoldenrod2',font=(None, 14))
text_widget1.place(x=250,y=200,anchor="center")
text_widget2 =Label(f1,text= "Change the frame rate to 25fps",fg='black',bg='DarkGoldenrod2',font=(None, 14))
text_widget2.place(x=250,y=240,anchor="center")


# In[4]:


class HelperClass():
    
    def __init__(self):
        
        self.directory2 = ''
        self.directory3 = ''
        
        self.basepath = ''
        
        self.directory_csv = ''
        self.directory_out_csv = ''
        
        self.fol = ''
        self.folder = StringVar()
        
        self.threshold_value = 0.0
        self.nconsecutive_frames = 0
        
        self.threshold_value2 = 0.0
        self.nconsecutive_frames2 = 0
        
        self.non_ghc_file_names = []


    def get_videos (self, path):
        
        print ('GET VIDEOS FROM', path)
        
        files = []
        for f in os.listdir(path):
            joined = path + '/' + f
            if os.path.isdir(joined):
                files += self.get_videos(joined)
            else:
                files += [joined]

        return files
    
    def downsamplevideos(self):
        
        for filex in self.get_videos(self.directory3):
        
            if filex.split('/')[-1].startswith("."):
                print ("downsamplevideos---skipping:", filex)
                continue
            
            dirpath = filex.split('/')[(-2)]
            filename = filex.split('/')[(-1)]
            outputvideofile = dirpath + filename
            (
                ffmpeg
                .input(filex)
                .filter('fps', fps=25, round='up')
                .filter_('scale', 532, 300)
                .output(os.path.join(self.directory2,'{}'.format(outputvideofile)))
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=False)
            )
    
        labelprint = Label(f1, text='Downsampling Done!', bg='forest green')
        labelprint.pack()
        Label(f1, text='Videos are downsampled and fps is adjusted to 25fps', bg='forest green').pack()
        
        
    def open_file (self):
        print ("call to 'open_file")
        filex = askdirectory()
        if filex is not None:
            self.directory3 = str(filex)
            ('on open_file, INPUTFOLDER=self.drectory3=', self.directory3)

    def output_file(self):
        filex = askdirectory()
        if filex is not None:
            self.directory2 = str(filex)
            print ('SET OUTPUTFILE (dir2):', self.directory2)
            
    def analyvideos(self):
        
        for filex in self.get_videos(self.basepath):
            
            vtype = filex.split('.')[-1]
            print (filex, vtype)
            vtpes = ['mp4', 'm4v', 'mpg', 'mts', 'mov', 'mpeg']
            
            if not vtype.lower() in vtpes:
                print ('skipping!')
                continue
            deeplabcut.analyze_videos(config, [self.basepath], shuffle=shuffle, videotype='.'+vtype, save_as_csv=True)

        labelprint3 = Label(f2, text='All Videos have been analyzed,results are in the directory with downsampled videos', bg='forest green')
        labelprint3.pack()

    def csv_location(self):

        file_csv = askdirectory()
        
        if file_csv is not None:
            self.directory_csv = file_csv

    def base_directory(self):
        
        labelprint2 = Label(f2, text="As the program runs, don't run out of your patience." +"\n"+"This might be a sprint or a marathon depending on the size of your data!", bg='AntiqueWhite3')
        labelprint2.pack()
        filedowns = askdirectory()
        
        if filedowns is not None:
            self.basepath = filedowns
    
    def thresh_value(self, E1):
        
        self.threshold_value = float(E1.get())

    def get_no_of_consecutive_frames(self, E2):
        
        self.nconsecutive_frames = int(E2.get())

    def outcsv_location (self):

        file_out_csv = askdirectory()

        if file_out_csv is not None:
            self.directory_out_csv = file_out_csv


    def thresh_value2(self, Eanalyze2):
        self.threshold_value2 = float(Eanalyze2.get())


    def get_no_of_consecutive_frames2 (self, Eanalyze3):
        self.nconsecutive_frames2 = int(Eanalyze3.get())

    #def analyze2 (self, outputpath, likelihood_value, consecutive_frames):
    def analyze2 (self):
        
        # outputpath = write out to folder
        # inputpath_csv = folder with the h5 files from last analysis
        
        outputpath = os.path.join(self.directory_out_csv+ '/analyze2')
        
        #outputpath = os.path.join(self.directory_csv+ '/analyze2')
        
        os.makedirs(outputpath, exist_ok=True)
        inputpath_csv = os.path.join(self.directory_out_csv + '/csv')
        all_files2 = glob.glob(inputpath_csv+ "/*.csv")

        print ("*"*100)
        print ("ANALYZE2")
        print ("OUTPUTPATH:", outputpath)
        print ("INPUTPATHCSV:", inputpath_csv)
        print ("ALL_FILES2:", all_files2)
        print ("*"*100)
        
        print(all_files2)
        
        non_ghc=[]
        ghc = {}
        frames=[]
        start_time=[]
        end_time=[]
        video=[]
        bp=[]
        
        df = pd.DataFrame(columns=["start","end","Video_name","Duration"])
        
        for i in all_files2:
            video_name=i.split('/')[-1].split('.')[0]
            data_reset=pd.read_csv(i)
            right=data_reset[data_reset['bodyparts'].isin(right_hand_cluster)& (data_reset['DLC_mobnet_100_GHCApr1shuffle1_205000likelihood']>= self.threshold_value2)]
            left=data_reset[data_reset['bodyparts'].isin(left_hand_cluster)& (data_reset['DLC_mobnet_100_GHCApr1shuffle1_205000likelihood']>=self.threshold_value2)]
            common =         set.intersection(set(left.level_0), set(right.level_0))
            fdata=pd.concat([left[left.level_0.isin(common)],right[right.level_0.isin(common)]]).sort_values(by='level_0')
            dfh = fdata.sort_values('level_0').drop_duplicates(subset='level_0')
            s = (dfh['level_0'] != dfh['level_0'].shift(1) + 1).cumsum()
            m = dfh.groupby(s).transform('count')['level_0']
            Nf=self.nconsecutive_frames2
            dfh = dfh[m>Nf]
            df1 = dfh.groupby(dfh['level_0'].diff().ne(1).cumsum())['level_0'].agg(['min','max'])
            df1 = df1[df1['min'].ne(df1['max'])]
            out = [list(x) for x in df1.to_numpy()]
            lenout=len(out)
            if not out:
                non_ghc.append(video_name)
            else:
                lenout=len(out)
                ghc[video_name]=lenout
                for i in out:
                    srtime=i[0]
                    start_time.append(srtime)

                for i in out:
                    et=i[1]
                    end_time.append(et)

                for i in out:
                    k=i[1]-i[0]
                    frames.append(k)
                    video.append(video_name)

                for i in out:
                    dis_df=fdata[(fdata['level_0'] >=i[0]) & (fdata['level_0'] <=i[1])]
                    agg_func = {'level_0': [('length', lambda x: x.ne((x+1).shift()).cumsum().value_counts().max())]}
                    result = dis_df.groupby('bodyparts').agg(agg_func)
                    result.columns = result.columns.droplevel(0)
                    result.sort_values('length', ascending=False)
                    bp.append(result.index[:7].tolist())
        print ("GHCDICT:", ghc)
        df_detections = pd.DataFrame(list(ghc.items()),columns = ['Video_name','No_of_Detections'])
        ran1=pd.DataFrame(columns =['Video_Name'])
        ran1['Video_Name']= [x for x in video]
        ran1['Likelihood']= self.threshold_value2# [likelihood_value for i in range(len(ran1.index))]
        ran1['frames_detected']=[x for x in frames]
        ran1['Start_time(s)']=[x / 25 for x in start_time]
        ran1['End_time(s)']=[x / 25 for x in end_time]
        ran1['Duration_of_ghc(s)']=ran1['frames_detected']/25
        ran1['Seven most detected body parts in order']=[x for x in bp]
        ran1.to_csv(outputpath+'/analyze2_details.csv')
        df_detections.to_csv(outputpath+'/analyze2_detections.csv')
        Label(f5, text="The Results are in the subfolder:Analyze2 ", bg='forest green', font=("Helvetica", 13)).pack()
        Label(f5, text="Which is in the same output-folder you choose for detection part ", fg='forest green', bg='DarkGoldenrod2',font=("Calibri", 12)).pack()
        return ran1 ,df_detections

    
    def locate_ghc (self):

        file_location = self.directory_csv
        out_file_path = self.directory_out_csv
        tvalue = self.threshold_value
        ncframes = self.nconsecutive_frames


        all_files = glob.glob(file_location + '/*.h5')
        opath_csv = os.path.join(out_file_path + '/csv')
        opath_plot = os.path.join(out_file_path + '/plots')
        opath_dataframe = os.path.join(out_file_path + '/dataframes')
        
        os.makedirs(opath_csv, exist_ok=True)
        os.makedirs(opath_plot, exist_ok=True)
        os.makedirs(opath_dataframe, exist_ok=True)
        
        for i in all_files:
            videofilename = i.split('DLC')[0].split('/')[(-1)]
            print(opath_csv, videofilename)
            data = pd.read_hdf(i)
            a = data.stack(level=1)
            c = [''.join(col).strip() for col in a.columns.values]
            a.columns = c
            data_reset = a.reset_index(level=[1, 0])
            data_reset.to_csv(os.path.join(opath_csv + '/{}.csv'.format(videofilename)))

        ghc_or_not = {}
        confidence = {}
        non_ghc_file_names=[]
        ghc_file_names=[]
        summm_l = []
        prob_array_smooth_l = []
        y_l = []
        len_max_conse_label_l = []
        csvfile_name_l = []
        time_points=[]
        for files in os.listdir(opath_csv):
            if files.endswith('.csv'):
                csvfile_name = os.path.basename(files)
                csvfile_name_l.append(csvfile_name.split('.')[0])
                with open((os.path.join(opath_csv, files)), newline='') as (csvfile):
                    reader = csv.reader(csvfile, delimiter=',')
                    reader = list(reader)
                    reader = reader[1:]
                    
                    adict = {}
                    for row in reader:
                        bpart = row[2]
                        prob = row[3]
                        if bpart not in adict:
                            adict[bpart] = []
                        adict[bpart] += [np.float(prob)]
                    
                    
                    # make sure all lists have same length
                    minlen=min(map(len, adict.values()))
    
                    body_parts = list(adict.keys())
                    for bp in body_parts:
                        adict[bp] = adict[bp][:minlen]
                    
                    prob_array = np.stack([adict[body_part] for body_part in body_parts])
                    
                    thresh = self.threshold_value
                    
                    print(thresh)
                    
                    present = np.zeros_like(prob_array)
                    present[prob_array > thresh] = 1
                    
                    N_CONSECUTIVE = self.nconsecutive_frames
                    present_csc = np.array([np.sum((present[:, i:i + N_CONSECUTIVE]), axis=(-1)) for i in range(present.shape[(-1)] - N_CONSECUTIVE)]).T
                    present_csc = np.int8(present_csc == N_CONSECUTIVE)
                    summm = np.sum(present_csc, axis=0)
                    summm_l.append(summm)
                    present_csc_smt = np.int32(np.sum(present_csc, axis=0) == len(body_parts))
                    w = 100
                    prob_array_smooth = np.array([np.mean((prob_array[:, i:i + w]), axis=(-1)) for i in range(prob_array.shape[(-1)] - w)]).T
                    prob_array_smooth_l.append(prob_array_smooth)
                    iloveyou = (prob_array > thresh).astype(int)
                    
                    x = np.array([np.sum((iloveyou[:, i:i + N_CONSECUTIVE]), axis=(-1)) for i in range(present.shape[(-1)] - N_CONSECUTIVE)]).T
                    x = (x == N_CONSECUTIVE).astype(int)
                    
                    y = np.sum(x, axis=0)
                    
                    
                    no_of_lab = max(y)
                    
                    y_l.append(no_of_lab)
                    
                    len_max_conse_label = len(np.arange(len(y))[(y == no_of_lab)])
                    len_max_conse_label_l.append(len_max_conse_label)
                    
                    N_CONSECUTIVE2 = self.nconsecutive_frames2

                    if no_of_lab == 0:
                        
                        ghc_or_not[csvfile_name.split('.')[0]] = 'No'
                        
                        confidence[csvfile_name.split('.')[0]]="Certain::Not_GHC"
                        non_ghc_file_names.append(csvfile_name.split('.')[0])
                        time_points.append(["None"])

                    elif no_of_lab <= 2:

                        ghc_or_not[csvfile_name.split('.')[0]] = 'GHC maybe'

                        confidence[csvfile_name.split('.')[0]]="Uncertain/Grooming"
                        ghc_file_names.append(csvfile_name)
                        thresh2 = 1
                        
                        
                        
                        z = np.array([np.int8(np.all(y[i:i+N_CONSECUTIVE2]>=thresh2)) for i in range(len(y)-N_CONSECUTIVE2)])
                        z = np.arange(len(z))[z.astype(bool)]
                        if z.size != 0:
                            inds = [z[0]]+z[1:][(z[1:]-z[:-1])>1].tolist()
                            inds_new= [ind / 25 for ind in inds]
                            time_points.append(inds_new)
                        else:
                            time_points.append(["None"])

                    else:
                        
                        ghc_or_not[csvfile_name.split('.')[0]] = 'GHC'
                    
                        confidence[csvfile_name.split('.')[0]]="Certain::GHC"
                        ghc_file_names.append(csvfile_name)
                        thresh2 = 2
                        z = np.array([np.int8(np.all(y[i:i+N_CONSECUTIVE2]>=thresh2)) for i in range(len(y)-N_CONSECUTIVE2)])
                        z = np.arange(len(z))[z.astype(bool)]
                        
                        print ("MORE THAN 2, z:", z)
                        
                        
                        if z.size != 0:
                            inds = [z[0]]+z[1:][(z[1:]-z[:-1])>1].tolist()
                            inds_new= [x / 25 for x in inds]
                            time_points.append(inds_new)
                        else:
                            time_points.append(["None"])
                    
                    print ("DONE LINE 442")
                    
                    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(28, 6))
                    ax1.plot(summm)
                    ax1.set_title('Labels in consecutive {} frames across all frames'.format(self.nconsecutive_frames))
                    ax1.set_xlabel('Frame Index')
                    ax1.set_ylabel('No of bodyparts present in {} consecutive frames'.format(self.nconsecutive_frames))
                    ax2.plot(prob_array_smooth.T)
                    ax2.set_title('Likelihood values of labels across Frames')
                    ax2.yaxis.tick_right()
                    ax2.set_xlabel('Frame Index')
                    ax2.set_ylabel('Likelihood Values')
                    fig.show()
                    fig.savefig(((opath_plot + '/{}.png').format(csvfile_name.split('.')[0])), dpi=300)
                    
                    print ("DONE LINE 457")
        
        
        ghc_dataframe = pd.DataFrame({'File_name':csvfile_name_l,  'Prediction':ghc_or_not.values(),  'Confidence':confidence.values(),'Max_consecutive_labels':y_l,'Time_Points':time_points})
        
        
#        print ("CSV OUTPUT:")
#        print ("csvfile_name_l:", len(csvfile_name_l))
#        print ("ghc_or_not:", len(ghc_or_not.values()))
#        print ("conf vals:", len(confidence.values()))
#        print ("conf vals:", len(y_l))
#        print ("time_points:", len(time_points))
        
        
#        ghc_dataframe = pd.DataFrame({'File_name':csvfile_name_l,  'Prediction':ghc_or_not.values(),  'Confidence':confidence.values(),'Max_consecutive_labels':y_l})

        ghc_video_names = pd.DataFrame(ghc_file_names,columns=['Video_Names'])
        
        print(ghc_dataframe)
        print(non_ghc_file_names)
        
        ghc_dataframe.to_csv(opath_dataframe + '/ghc_main_dataframe.csv')
        ghc_video_names.to_csv(opath_dataframe + '/ghc_video_names.csv')
        Label(f3,text="""We are done here!""",fg='forest green', bg='DarkGoldenrod2',font=("Calibri", 12)).pack()
        
        
        self.non_ghc_file_names = non_ghc_file_names
        
        #return (non_ghc_file_names, ghc_dataframe, summm_l, prob_array_smooth_l, y_l, len_max_conse_label_l, csvfile_name_l, ghc_or_not, confidence)


    def shift_videos (self):
        
        
        
        name = str(self.folder.get())
        
        print ("SHIFT VIDEOS", self.directory_out_csv, "name:", name)
        
        new_path= self.directory_out_csv + "/" + name
        os.makedirs(new_path, exist_ok=True)
        source_dir = self.directory3
        
        for file_name in self.non_ghc_file_names:
            
            shutil.move(os.path.join(source_dir, file_name), new_path)


    def path (self):
        
        global Epath
        
        Epath = Entry(f4, textvariable=self.folder, bd=5)
        Epath.pack()
        Epath.insert(0, 'Type: Name for the new folder here')
        Epath.focus_set()
        
        btn11 = Button(f4, text='Move', command=(lambda : helper.shift_videos()), bg='tomato2', fg='black')
        btn11.pack(side=TOP, pady=20, expand=True)
    



helper = HelperClass()

#helper.fol = StringVar()

print ("LALALALALA")


btn = Button(f1, text='Input folder', command=(lambda : helper.open_file()))
btn.pack(side=TOP, pady=5)

btn2 = Button(f1, text='Output folder', command=helper.output_file)
btn2.pack(side=TOP, pady=5)

#a = helper.locate_ghc()

btn3 = Button(f1, text='Downsample', command=helper.downsamplevideos)
btn3.pack(side=BOTTOM, pady=5, expand=True)




#############Frame2##########################


text_widget3 =Label(f2,text= "Here, the pre-trained network is used to analyze the downsampled videos",fg='black',bg='DarkGoldenrod2',font=(None, 14))
text_widget3.place(x=260,y=200,anchor="center")

#project = '00GHC-CB-2020-04-01'
#shuffle = 1
#prefix = '/Users/aishu/Desktop/'
#projectpath = os.path.join(prefix, project)
#config = os.path.join(projectpath, 'config.yml')

# FEDIT 18/2/21
shuffle = 1
project = '00GHC-CB-2020-04-01'
prefix = os.path.abspath(os.path.dirname(__file__))
projectpath = os.path.join(prefix, project)
config = os.path.join(projectpath, 'config.yml')

import yaml
import io

# edit yaml so project_path is correct
with open(config, 'r') as stream:
    data_loaded = yaml.safe_load(stream)
    data_loaded['project_path'] = projectpath

with io.open(config, 'w', encoding='utf8') as outfile:
    yaml.dump(data_loaded, outfile, default_flow_style=False, allow_unicode=True)

# END EDIT



btn4 = Button(f2, text='Path to downsampled videos', command=helper.base_directory)
btn4.pack(side=TOP, pady=20)



btn5 = Button(f2, text='Analyze Data', command=helper.analyvideos)
btn5.pack(side=BOTTOM, pady=20)


##########################Frame3 ##########################




btn6 = Button(f3, text='Folder with the h5 files from last analysis', command=helper.csv_location)
btn6.pack(side=TOP, padx=5, pady=5, expand=True)





btn7 = Button(f3, text='write out to folder', command=helper.outcsv_location)
btn7.pack(side=TOP, padx=5, pady=5, expand=True)
tv = DoubleVar()
N = IntVar()

global E1
E1 = Entry(f3, textvariable=tv, bd=5)
E1.pack()
E1.insert(0, 'Enter a threshold value for detection and click confirm_threshold')
E1.focus_set()

btn8 = Button(f3, text='confirm_threshold', command=(lambda : helper.thresh_value(E1)), bg='tomato2', fg='black')
btn8.pack(side=TOP, pady=20, expand=True)

global E2
E2 = Entry(f3, textvariable=N, bd=5)
E2.pack()
E2.insert(0, 'Enter number of consecutive frames and click confirm_cframes')
E2.focus_set()
btn9 = Button(f3, text='confirm_cframes', command=(lambda : helper.get_no_of_consecutive_frames(E2)), bg='tomato2', fg='black')
btn9.pack(side=TOP, pady=20, expand=True)




#def locate_ghc(file_location, out_file_path, tvalue, ncframes):

btn10 = Button(f3, text='Classify', command=helper.locate_ghc)
btn10.pack(side='bottom', expand=True)


#helper.directory_csv=csv_location()
#helper.directory_out_csv=outcsv_location

#a=locate_ghc(directory_csv, directory_out_csv, threshold_value, nconsecutive_frames)
if 0:
    a = helper.locate_ghc()

    non_ghc_files=a[0]
#print(a)


######### Frame 4: Classify ##############


Label(f4, text="""Would you like to move videos without GHC to a new folder?""", justify=LEFT, padx=5).pack()

var = IntVar()

def sel():
    s=Label(f4,text="Aw, don't be like that!")
    s.pack()


#global fol

#helper.fol = StringVar()




#def path(fol,directory3,directory_out_csv):
#    global Epath
#    Epath = Entry(f4, textvariable=fol, bd=5)
#    Epath.pack()
#    Epath.insert(0, 'Type: Name for the new folder here')
#    Epath.focus_set()
#    btn11 = Button(f4, text='Move', command=(lambda : shift_videos(fol,directory3,directory_out_csv,non_ghc_files)), bg='tomato2', fg='black')
#    btn11.pack(side=TOP, pady=20, expand=True)
#
#
#def shift_videos(fol,directory3,directory_out_csv,non_ghc_files):
#    name=str(fol.get())
#    new_path = directory_out_csv + "/" + name
#    os.makedirs(new_path, exist_ok=True)
#    for file in directory3:
#        #if file.split(".")[0] in non_
#        for i in non_ghc_files:
#            if file.startswith(i):
#                shutil.move(file,os.path.join(new_path,file))
#    Label(f4,text="The videos are in the same output-folder as in the previous section",fg='forest green', bg='DarkGoldenrod2',font=("Calibri", 12)).pack()


R1 = Radiobutton(f4, text="Yes", variable=var, value=1, command=lambda : helper.path())

R1.pack(anchor=S, pady=15)

R2 = Radiobutton(f4, text="No", variable=var, value=2, command=sel)
R2.pack(anchor=S, pady=15)



Button(f4, text='Exit', command=f4.destroy).pack(side=BOTTOM)






#########Label 5: Further Detection ################


right_hand_cluster=['right_palm_thumbfingertohandjoint',
                    'right_insidepalm_thumbarea',
                    'right_elbowoutside',
                    'right_elbowoutside','right_palm_knukles1','right_finger_endpoint2',
                    'right_finger_endpoint',
                    'right_finger_thumb',
                    'right_finger_2',
                    'right_finger_1',
                    'right_wrist_rightside',
                    'right_wrist_leftside','right_arm_to_body','right_shoulderpoint']

left_hand_cluster = ['left_wrist_leftside',
                     'left_wrist_rightside',
                     'left_finger_1',
                     'left_elbowoutside',
                     'left_elbowinside',
                     'left_finger_2',
                     'left_finger_thumb',
                     'left_finger_endpoint',
                    'left_finger_endpoint2',
                    'left_palm_knukles1',
                   'left_insidepalm_thumbarea',
                   'left_palm_thumbfingertohandjoint',
                   'left_arm_to_body',
                   'left_shoulderpoint']



#button input threshold and consecutive frames

tv2 = DoubleVar()
N2 = IntVar()






global Eanalyze2
Eanalyze2 = Entry(f5, textvariable=tv2, bd=5)
Eanalyze2.pack()
Eanalyze2.insert(0, 'Enter a threshold value for detection and click confirm_threshold')
Eanalyze2.focus_set()

btn12 = Button(f5, text='confirm_threshold', command=(lambda : helper.thresh_value2(Eanalyze2)), bg='tomato2', fg='black')
btn12.pack(side=TOP, pady=20, expand=True)

global Eanalyze3
Eanalyze3 = Entry(f5, textvariable=N2, bd=5)
Eanalyze3.pack()
Eanalyze3.insert(0, 'Enter number of consecutive frames and click confirm_cframes')
Eanalyze3.focus_set()

btn13 = Button(f5, text='confirm_cframes', command=(lambda : helper.get_no_of_consecutive_frames2(Eanalyze3)), bg='tomato2', fg='black')
btn13.pack(side=TOP, pady=20, expand=True)





#btn13 = Button(f5, text='Analyze2', command=(lambda : helper.analyze2(inputpath_csv, directory_out_csv,threshold_value2,nconsecutive_frames2)))
btn13 = Button(f5, text='Analyze2', command=(lambda : helper.analyze2()))
btn13.pack(side='bottom', expand=True)

Button(f5, text='Exit', command=f5.destroy).pack(side=BOTTOM)


root.mainloop()