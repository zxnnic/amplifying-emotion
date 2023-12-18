import json
data_path = r"D:\Grad\Courses\CSC2521\data_talking\happy\p2_goodday_neutral\MySlate_17_iPhone.csv"

ADJUST_VALLEYGIRL = ["mouthstretchright", "mouthstretchleft", "mouthlowerdownright", "mouthlowerdownleft", "mouthupperupright", "mouthupperupleft"]

def load_apple_motion(motion_data_path = "", recordingfps=30, calibration_data_path=""):

    name_to_mesh = {"eyesquintright": ["AU7 – lid tightener", "Mesh31", "Squint_R.Squint_R", 0, 8],
                 "eyesquintleft": ["AU7 – lid tightener", "Mesh32", "Squint_L.Squint_L", 0, 8],
                 "eyelookupright": ["M63 – eyes up", "Mesh33", "CNT_EYE_RIGHT.DownUp_eye_R", 0, 10],
                 "eyelookupleft": ["M63 – eyes up", "Mesh34", "CNT_EYE_LEFT.DownUp_eye_L", 0, 10],
                 "jawright": ["AD30 – jaw sideways", "Mesh25", "CNT_JAW.LeftRight_jaw", 0, 10],
                 "jawleft": ["AD30 – jaw sideways", "Mesh27", "CNT_JAW.LeftRight_jaw", 0, -10],
                 "mouthstretchright": ["AU20 – lip stretcher", "Mesh4", "Grimace_R.Grimace_R", 0, 10],
                 "mouthstretchleft": ["AU20 – lip stretcher", "Mesh6", "Grimace_L.Grimace_L", 0, 10],
                 "browdownright": ["AU4 – brow lowerer", "Mesh49", "BrowFurrow_R", 0, 4],
                 "browdownleft": ["AU4 – brow lowerer", "Mesh50", "BrowFurrow_L", 0, 4],
                 "browdownleft\n": ["AU4 – brow lowerer", "Mesh50", "BrowFurrow_L", 0, 4],
                 "cheekpuff": ["AD34 – puff", "Mesh45", "SuckBlow", 0, 10],
                 "mouthsmileright": ["AU12 – lip corner puller", "Mesh7", "Smile_R.Smile_R", 0, 10],
                 "mouthsmileleft": ["AU12 – lip corner puller", "Mesh5", "Smile_L.Smile_L", 0, 10],
                 "jawopen": ["AU26 – jaw drop or AU27 – mouth stretch", "Mesh26", "CNT_JAW.Open_jaw", 0, 10],
                 "jawforward": ["AD29 – jaw thrust", "Mesh28", "CNT_JAW.Thrust_jaw", 0, 10],
                 "mouthrollupper": ["AU28 – lips suck", "Mesh10", "UpLip_ctl.TightenFunnel_upLip", 0, -5],
                 "mouthrolllower": ["AU28 – lips suck", "Mesh11", "LoLip_ctl.TightenFunnel_loLip", 0, -5],
                 "mouthlowerdownright": ["AU16 – lower lip depressor", "Mesh16", "LoLip_R_ctl.DownUp_loLip_R", 0, -5],
                 "mouthlowerdownleft": ["AU16 – lower lip depressor", "Mesh17", "LoLip_L_ctl.DownUp_loLip_L", 0, -5],
                 "browouterupright": ["AU2 – outer brow raiser", "Mesh46", "OuterBrowRaise_R", 0, 8],
                 "browouterupleft": ["AU2 – outer brow raiser", "Mesh47", "OuterBrowRaise_L", 0, 8],
                 "mouthdimpleright": ["AU14 – dimpler", "Mesh22", "Dimple_R", 0, 10],
                 "mouthdimpleleft": ["AU14 – dimpler", "Mesh23", "Dimple_L", 0, 10],
                 "eyelookdownright": ["M64 – eyes down", "Mesh39", "CNT_EYE_RIGHT.DownUp_eye_R", 0, -10],
                 "eyelookdownleft": ["M64 – eyes down", "Mesh40", "CNT_EYE_LEFT.DownUp_eye_L", 0, -10],
                 "eyewideright": ["AU5 – upper lid raiser", "Mesh29", "blink_R", 0, -5],
                 "eyewideleft": ["AU5 – upper lid raiser", "Mesh30", "blink_L", 0, -5],
                 "cheeksquintright": ["AU6 – cheek raiser", "Mesh43", "CheekRaise_R", 0, 5],
                 "cheeksquintleft": ["AU6 – cheek raiser", "Mesh44", "CheekRaise_L", 0, 5],
                 "mouthpucker": ["AU18 – lip pucker", "Mesh13", "Pucker", 0, 10],
                 "mouthupperupright": ["AU10 – upper lip raiser", "Mesh2", "UpLip_R_ctl.DownUp_upLip_R", 0, -3], #??
                 "mouthupperupleft": ["AU10 – upper lip raiser", "Mesh3", "UpLip_L_ctl.DownUp_upLip_L", 0, -3],  #??
                 "nosesneerright\n": ["AU9 – nose wrinkler", "Mesh", "Wince_R", 0, 4],
                 "nosesneerright": ["AU9 – nose wrinkler", "Mesh", "Wince_R", 0, 4],
                 "nosesneerleft": ["AU9 – nose wrinkler", "Mesh1", "Wince_L", 0, 4],
                 "eyelookoutright": ["AU65 – walleye", "Mesh35", "CNT_EYE_RIGHT.LeftRight_eye_R", 0, -10],
                 "eyelookoutleft": ["AU65 – walleye", "Mesh36", "CNT_EYE_LEFT.LeftRight_eye_L", 0, 10],
                 "browinnerup": ["AU1 – inner brow raiser", "Mesh48", "InnerBrowRaise", 0, 10],
                 "eyelookinleft": ["AU66 – crosseye", "Mesh38", "CNT_EYE_RIGHT.LeftRight_eye_R", 0, 10],
                 "eyelookinright": ["AU66 – crosseye", "Mesh37", "CNT_EYE_LEFT.LeftRight_eye_L", 0, -10],
                 "eyeblinkright": ["AU45 – blink", "Mesh41", "blink_R", 0, 10],
                 "eyeblinkleft": ["AU45 – blink", "Mesh42", "blink_L", 0, 10],
                 "mouthfrownright": ["AU15 – lip corner depressor", "Mesh20", "Frown_R", 0, 8],
                 "mouthfrownleft": ["AU15 – lip corner depressor", "Mesh21", "Frown_L", 0, 8],
                 "mouthfunnel": ["AU22 – lip funneler", "Mesh19", "MouthCTL.TightenFunnel", 0, 8],
                #  "mouthpressright": ["AU24 – lip presser", "Mesh14"],
                #  "mouthpressleft": ["AU24 – lip presser", "Mesh15"],
                #  "mouthclose": ["N/A", "Mesh24"],
                #  "mouthshrugupper": ["N/A", "Mesh8"],
                #  "mouthshruglower": ["N/A", "Mesh9"],
                #  "mouthright": ["N/A", "Mesh12"],
                #  "mouthleft": ["N/A", "Mesh18"],
                #  "tongueout", head roll, eye pitch...
                 }

    # load data from file
    columns = []
    raw_cal_data = []
    cal_data = []
    times = []
    with open(calibration_data_path) as f:
        labels = f.readline()
        columns = labels.split(",")
        columns = columns[2:]
        raw_cal_data = f.readlines()
    
    # adjustments(raw_cal_data)

    for i in range(0, len(raw_cal_data)):
        frame_time = raw_cal_data[i].split(",")[0]
        frame_time_list = frame_time.split(":")
        frame_hour, frame_minute, frame_second, frame_frame = frame_time_list
        frame_hour = float(frame_hour)
        frame_minute = float(frame_minute)
        frame_second = float(frame_second)
        frame_frame = float(frame_frame)
        frame_time = frame_frame/recordingfps + frame_second + frame_minute * 60 + frame_hour * 3600
        frame_cal_data = raw_cal_data[i].split(",")

        # if len(frame_cal_data) > 20:
        times.append(frame_time)
        cal_data.append(frame_cal_data[2:])

    start_time = times[0]

    for i in range(0, len(times)):
        times[i] = times[i] - start_time
    for j in range(0, len(columns)): #-10
        name = columns[j].lower()
        weight_name = name_to_mesh[name][2]
        cmds.cutKey(weight_name, s=True)

    # compute curve using loaded data:
    for i in range(0, len(times)):
        for j in range(0, len(columns)):
            name = columns[j].lower()
            weight_name = name_to_mesh[name][2]
            cmds.setKeyframe(weight_name, v=float(cal_data[i][j])*(name_to_mesh[name][4]-name_to_mesh[name][3]),
                                 t=times[i] * mel.eval('float $fps = `currentTimeUnitToFPS`'))

load_apple_motion(data_path, 60, data_path)