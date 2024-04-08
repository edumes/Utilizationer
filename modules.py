from moviepy.editor import VideoFileClip
from tkinter import messagebox

def split_video(self, input_video, output_prefix, segment_duration):
    clip = VideoFileClip(input_video)
    total_duration = clip.duration
    num_segments = int(total_duration / segment_duration)

    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, total_duration)
        subclip = clip.subclip(start_time, end_time)
        output_name = os.path.join(output_prefix, f"{os.path.basename(output_prefix)}_{i + 1}.mp4")
        subclip.write_videofile(output_name)

    clip.close()
    messagebox.showinfo("Success", "Vídeo cortado com sucesso")