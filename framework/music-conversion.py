from pydub import AudioSegment
import os

# Define the source and target directories
source_dir = 'music'
target_dir = 'music-short'

# Check if the target directory exists, if not create it
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Loop through each file in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith('.wav'):
        # Load the audio file
        audio = AudioSegment.from_wav(os.path.join(source_dir, filename))
        
        # Shorten the audio to the first 20 seconds
        short_audio = audio[:20000]  # AudioSegment works in milliseconds
        
        # Save the shortened audio to the target directory
        short_audio.export(os.path.join(target_dir, filename), format='wav')

print("All files have been processed.")
