import cv2
import numpy as np
import librosa
import pygame
print ("works")
# Parameters
AUDIO_FILE = "./files/song1.mp3"  
VIDEO_FILE = "./files/video1.mp4"  
FRAME_JUMP = 15  
print ("works2")

# Load audio and detect beats
y, sr = librosa.load(AUDIO_FILE, sr=None)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=512)
beat_times = librosa.frames_to_time(beats, sr=sr)

# Open video file
cap = cv2.VideoCapture(VIDEO_FILE)
fps = cap.get(cv2.CAP_PROP_FPS)

# Convert beat times to frame numbers
beat_frames = (beat_times * fps).astype(int)

# Initialize audio playback
pygame.mixer.init()
pygame.mixer.music.load(AUDIO_FILE)
pygame.mixer.music.play()

# Play video with beat skipping
current_beat = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Video Sync', frame)

    # Skip frames on beat
    if current_beat < len(beat_frames) and cap.get(cv2.CAP_PROP_POS_FRAMES) >= beat_frames[current_beat]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + FRAME_JUMP)
        current_beat += 1

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()