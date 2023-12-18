import pandas as pd

KNOWN_AUS = {"timecode":[],"blendshapecount":[],
  "eyesquintright": ["AU7 – lid tightener", "Mesh31", "Squint_R.Squint_R", 0, 8],
    "eyesquintleft": ["AU7 – lid tightener", "Mesh32", "Squint_L.Squint_L", 0, 8],
    "eyelookupright": ["M63 – eyes up", "Mesh33", "CNT_EYE_RIGHT.DownUp_eye_R", 0, 10],
    "eyelookupleft": ["M63 – eyes up", "Mesh34", "CNT_EYE_LEFT.DownUp_eye_L", 0, 10],
    # "jawright": ["AD30 – jaw sideways", "Mesh25", "CNT_JAW.LeftRight_jaw", 0, 10],
    # "jawleft": ["AD30 – jaw sideways", "Mesh27", "CNT_JAW.LeftRight_jaw", 0, -10],
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
    # "mouthrollupper": ["AU28 – lips suck", "Mesh10", "UpLip_ctl.TightenFunnel_upLip", 0, -5],
    # "mouthrolllower": ["AU28 – lips suck", "Mesh11", "LoLip_ctl.TightenFunnel_loLip", 0, -5],
    "mouthlowerdownright": ["AU16 – lower lip depressor", "Mesh16", "LoLip_R_ctl.DownUp_loLip_R", 0, -5],
    "mouthlowerdownleft": ["AU16 – lower lip depressor", "Mesh17", "LoLip_L_ctl.DownUp_loLip_L", 0, -5],
    # "browouterupright": ["AU2 – outer brow raiser", "Mesh46", "OuterBrowRaise_R", 0, 8],
    # "browouterupleft": ["AU2 – outer brow raiser", "Mesh47", "OuterBrowRaise_L", 0, 8],
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
    # "mouthfrownright": ["AU15 – lip corner depressor", "Mesh20", "Frown_R", 0, 8],
    # "mouthfrownleft": ["AU15 – lip corner depressor", "Mesh21", "Frown_L", 0, 8],
    # "mouthfunnel": ["AU22 – lip funneler", "Mesh19", "MouthCTL.TightenFunnel", 0, 8]
}
KNOWN_AUS = KNOWN_AUS.keys()

FILENAME = "./inputs/MySlate_17_iPhone.csv"
OUT_PATH = "./outputs/"

# Read target video's ARKit blendshapes.
neutral = pd.read_csv(FILENAME)
for col in neutral.columns:
  if col.lower() not in KNOWN_AUS:
    neutral.drop(col, axis=1, inplace=True)

neutral.to_csv(OUT_PATH+"p2_goodday_neutral.csv", index=False)