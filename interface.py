import os
from tkinter import messagebox
from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import filedialog
import customtkinter
from PIL import Image, ImageTk
import threading

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Utilizationer")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Utilizationer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Vídeo", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Conversores", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=640, height=800)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Cortar Vídeo")
        self.tabview.add("Verticalizar")
        self.tabview.tab("Cortar Vídeo").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Verticalizar").grid_columnconfigure(0, weight=1)

        self.choose_file_button = customtkinter.CTkButton(self.tabview.tab("Cortar Vídeo"), text="Escolher Arquivo de Vídeo",
                                                          command=self.choose_file_event)
        self.choose_file_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.thumbnail_label = tk.Label(self.tabview.tab("Cortar Vídeo"))
        self.thumbnail_label.grid(row=3, column=0, padx=20, pady=(20, 20))
        self.choose_folder_button = customtkinter.CTkButton(self.tabview.tab("Cortar Vídeo"), text="Escolher Pasta de Saída",
                                                            command=self.choose_folder_event)
        self.choose_folder_button.grid(row=4, column=0, padx=20, pady=(10, 10))
        self.selected_folder_label = customtkinter.CTkLabel(self.tabview.tab("Cortar Vídeo"), text="", anchor="w")
        self.selected_folder_label.grid(row=5, column=0, padx=0, pady=(0, 0))

        # Create input for seconds
        self.seconds_label = customtkinter.CTkLabel(self.tabview.tab("Cortar Vídeo"), text="Segundos de cada parte cortada:")
        self.seconds_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.seconds_entry = customtkinter.CTkEntry(self.tabview.tab("Cortar Vídeo"), width=40)
        self.seconds_entry.grid(row=7, column=0, padx=20, pady=(0, 10))
        self.seconds_entry.insert(0, "60")  # Default value

        # Button to cut video
        self.cut_video_button = customtkinter.CTkButton(self.tabview.tab("Cortar Vídeo"), text="Cortar Vídeo", command=self.cut_video_event)
        self.cut_video_button.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self.tabview.tab("Cortar Vídeo"), fg_color="transparent")
        self.slider_progressbar_frame.grid(row=9, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(100, 100), pady=(0, 100), sticky="ew")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.selected_file_path = None

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def choose_file_event(self):
        self.selected_file_path = filedialog.askopenfilename()
        if self.selected_file_path:
            print("Selected file:", self.selected_file_path)
            self.show_thumbnail(self.selected_file_path)

    def choose_folder_event(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            print("Selected folder:", folder_path)
            self.selected_folder_label.configure(text=folder_path)

    def show_thumbnail(self, file_path):
        try:
            clip = VideoFileClip(file_path)
            frame = clip.get_frame(0)
            image = Image.fromarray(frame)
            image.thumbnail((250, 250))
            photo = ImageTk.PhotoImage(image)
            self.thumbnail_label.configure(image=photo)
            self.thumbnail_label.image = photo
        except Exception as e:
            print("Error:", e)

    def cut_video_event(self):
        if self.selected_file_path:
            seconds = int(self.seconds_entry.get())
            print("Cutting video with {} seconds per part".format(seconds))
            output_folder = self.selected_folder_label.cget("text")
            if not output_folder:
                messagebox.showerror("Error", "Please choose an output folder.")
                return

            base_name = os.path.splitext(os.path.basename(self.selected_file_path))[0]

            output_path = os.path.join(output_folder, f"{base_name}")
            print("output pathh", output_folder, output_path)
            os.makedirs(output_path, exist_ok=True)

            threading.Thread(target=self.split_video, args=(self.selected_file_path, output_path, seconds)).start()
        else:
            messagebox.showerror("Error", "Please choose a video file.")

    def update_progress(self, progress):
        self.progressbar_1["value"] = progress

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