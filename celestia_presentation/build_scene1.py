import os

print("🎬 Starting Manim Render...")
# Render all clips in the file sequentially using the OpenGL engine
os.system("manim --renderer=opengl -pqh scene1.py -a")

print("🔄 Stitching clips together...")
# Define the exact order of the clips
video_folder = "media/videos/scene1/1080p60/" # Adjust this if you use -pql (480p15)
clips = [
    "S1_Clip1_Immersion.mp4",
    "S1_Clip2_Abstraction.mp4",
    "S1_Clip3_Fold.mp4",
    "S1_Clip4_SphereSolution.mp4"
]

# Create a temporary text file that FFmpeg uses to know the order
with open("clip_list.txt", "w") as file:
    for clip in clips:
        # Check if the file exists to prevent FFmpeg crashes
        clip_path = os.path.join(video_folder, clip)
        if os.path.exists(clip_path):
            file.write(f"file '{clip_path}'\n")
        else:
            print(f"⚠️ Warning: Could not find {clip}")

# Run FFmpeg to concatenate the videos without re-encoding them (lightning fast)
os.system("ffmpeg -y -f concat -safe 0 -i clip_list.txt -c copy Final_Scene1_TheSkyboxProblem.mp4")

# Clean up the temporary text file
os.remove("clip_list.txt")

print("✅ Done! Your full scene is ready: Final_Scene1_TheSkyboxProblem.mp4")