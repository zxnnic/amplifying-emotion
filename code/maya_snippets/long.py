import csv
import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

PHRASE = ""
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


def get_level(mean_AUs, video, level_inds):
  """
  Gets the average level of happiness in the video:
  """
  # Extract the dynamic activation of the smile AU in the mean_AUs.
  smile_AU = mean_AUs.MouthSmileLeft

  # Extract the average activation of left and right smile in the target video.
  target = (video.MouthSmileLeft.mean() + video.MouthSmileRight.mean())/2

  # Finds the index (time) of the mean smile_AU that matches the average smile in the video the best.
  smile_AU_index = min(range(len(smile_AU)), key=lambda i: abs(smile_AU[i] - target))

  # Fins the index (level) of happiness that matches the time index of the smile the best.
  level_index = min(range(len(level_inds)), key=lambda i: abs(level_inds[i] - smile_AU_index))

  return level_index


def segment_amplification(mean_AU, mode, level_inds, init_level, start_level, end_level, total_duration):
  """
  Amplifies segment with desired start and end emotion intensities.
  """
  # If mode is data-driven mean_AU amplification.
  if mode == "amp":
    # If temporal amplification:
    if start_level < end_level:
      # Slice the segment of the mean_AU between the start and end emotion level indices.
      target = mean_AU[level_inds[start_level]:level_inds[end_level]]
      # Resample the signal to match the total duration of the original segment.
      resample = signal.resample(target, total_duration+40)[20:-20]

    # If temporal dampening, same but reverse the timing:
    elif end_level < start_level:
      target = mean_AU[level_inds[end_level]:level_inds[start_level]]
      target = target[::-1]
      resample = signal.resample(target, total_duration+40)[20:-20]

    # If static amplifiction, just add a fix factor according to the intensity:
    else:
      resample = mean_AU[level_inds[start_level]]*np.ones(total_duration)

  # If mode is naive linear amplification.
  else:
    # Find the start and end levels and interpolating linearly between them.
    start = mean_AU[level_inds[start_level]]
    end = mean_AU[level_inds[end_level]]
    resample = np.linspace(start, end, total_duration)

  # Adjust the amplification by the existing level of emotion in the video (to prevent overamplification).
  resample -= mean_AU[level_inds[init_level]]
  return resample


def padded_amplification(segment, start_ind, end_ind, total_length):
  """
  Pad the amplified segment with extra 0s to match the original length.
  """
  padded = np.zeros(total_length)
  padded[start_ind:end_ind] = segment
  return padded


def amplify(mean_AUs, video, mode="amp", control_dict={0:0, 100:4}):
  """
  Amplification method:
    - mean_AUs: csv of blendshapes of the dynamic AU activations from neutral to full emotion.
    - video: csv of blendshapes from video to alter.
    - mode: option between "amp" using the natural curves of mean_AUs, or "lin" using naive linear interpolation between emotion levels.
    - control_dict: a dictionary of video fraction from [0, 100]% to happiness level in [0, 4].
  """
  amplified = video.copy()

  # Manually get the indices of mean_AUs that represent 5 discretized levels of emotions (the numbers are based on K-Means clustering results).
  length = len(mean_AUs)
  level_inds = [int(0.17*length), int(0.36*length), int(0.48*length), int(0.62*length), int(0.85*length)]
  init_level = get_level(mean_AUs, video, level_inds)

  total_length = len(video)
  control_fracs = list(control_dict.keys())
  control_levels = list(control_dict.values())

  # For each video segment in the control_dict, extract desired start and end amplification levels.
  for i in range(len(control_fracs)-1):
    start_ind = int(control_fracs[i]/100*total_length)
    start_level = control_levels[i]
    end_ind = int(control_fracs[i+1]/100*total_length)
    end_level = control_levels[i+1]
    total_duration = end_ind - start_ind

    # For each AU in the video if it also exists in mean_AUs, apply amplification.
    for column in amplified:
      if column in mean.columns:
        segment_amplified = segment_amplification(mean_AUs[column], mode, level_inds,
                                                  init_level, start_level, end_level, total_duration)

        # Pad everything else outside of the segment with 0s and add to the video.
        amplified[column] += padded_amplification(segment_amplified, start_ind, end_ind, total_length)

  return amplified

def detect_sentiment(phrase):
  pass

# Read mean AUs captured from our recording study participants.
meanAU_path = r"duplicate_mean_aus_scaled.csv"
mean = pd.read_csv(meanAU_path)
mean = mean.drop(columns = ['Timecode', 'BlendshapeCount'])

# Read target video's ARKit blendshapes.
neutral_path = r"./inputs/nicole_neutral_long.csv"
neutral = pd.read_csv(neutral_path)
for col in neutral.columns:
  if col.lower() not in KNOWN_AUS:
    neutral.drop(col, axis=1, inplace=True)

# detect sentiment and set up the levels
control_dict = detect_sentiment(PHRASE)

# Apply amplification using our method "amp" or naive baseline "lin".
amplified_AMP = amplify(mean, neutral, mode="amp", control_dict={0:0, 35:3, 60:0, 100:4})
amplified_LIN = amplify(mean, neutral, mode="lin", control_dict={0:0, 35:3, 60:0, 100:4})

amplified_AMP.to_csv("./outputs/nicole_long_neutral_AMP.csv", index=False)
amplified_LIN.to_csv("./outputs/nicole_long_neutral_LIN.csv", index=False)
