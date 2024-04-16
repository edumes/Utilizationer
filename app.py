import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from moviepy.video.fx.resize import resize
from moviepy.editor import VideoFileClip
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.current_minute = 0

        # configure window
        self.title("Utilizationer")
        self.geometry(f"{1280}x{720}")

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
        
        self.choose_folder_button = customtkinter.CTkButton(self.tabview.tab("Verticalizar"), text="Escolher Pasta de Saída",
                                                            command=self.choose_folder_event)
        self.choose_folder_button.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.selected_folder_label = customtkinter.CTkLabel(self.tabview.tab("Verticalizar"), text="", anchor="w")
        self.selected_folder_label.grid(row=9, column=0, padx=0, pady=(0, 0))

        self.seconds_label = customtkinter.CTkLabel(self.tabview.tab("Cortar Vídeo"), text="Segundos de cada parte cortada:")
        self.seconds_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.seconds_entry = customtkinter.CTkEntry(self.tabview.tab("Cortar Vídeo"), width=40)
        self.seconds_entry.grid(row=7, column=0, padx=20, pady=(0, 10))
        self.seconds_entry.insert(0, "60")  # Default value

        self.loading_label = customtkinter.CTkLabel(self.tabview.tab("Cortar Vídeo"), text="Carregando...", anchor="w")
        self.loading_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.loading_label.grid_remove()

        self.cut_video_button = customtkinter.CTkButton(self.tabview.tab("Cortar Vídeo"), text="Cortar Vídeo", command=self.cut_video_event)
        self.cut_video_button.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Adding elements for Verticalize tab
        self.choose_video_button = customtkinter.CTkButton(self.tabview.tab("Verticalizar"), text="Escolher Arquivo de Vídeo",
                                                            command=self.choose_video_event)
        self.choose_video_button.grid(row=0, column=0, padx=20, pady=(10, 10))

        # Thumbnails for each 15 seconds within a minute
        self.thumbnail_label_vertical_0 = tk.Label(self.tabview.tab("Verticalizar"))
        self.thumbnail_label_vertical_0.grid(row=1, column=0, padx=20)

        self.thumbnail_label_vertical_30 = tk.Label(self.tabview.tab("Verticalizar"))
        self.thumbnail_label_vertical_30.grid(row=2, column=0)

        self.verticalize_part_button = customtkinter.CTkButton(self.tabview.tab("Verticalizar"), text="Verticalizar Parte",
                                                            command=self.verticalize_part_event)
        self.verticalize_part_button.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.cut_part_button = customtkinter.CTkButton(self.tabview.tab("Verticalizar"), text="Apenas Cortar Parte",
                                                            command=self.cut_part_event)
        self.cut_part_button.grid(row=4, column=0, padx=20, pady=(10, 10))

        self.previous_minute_button = customtkinter.CTkButton(self.tabview.tab("Verticalizar"), text="<<< Ir para Minuto Anterior",
                                                            command=self.previous_minute_event)
        self.previous_minute_button.grid(row=5, column=0, padx=20, pady=(10, 10))
        self.previous_minute_button.configure(state="disabled")  # Disable initially

        self.next_minute_button = customtkinter.CTkButton(self.tabview.tab("Verticalizar"), text=">>> Ir para Próximo Minuto",
                                                            command=self.next_minute_event)
        self.next_minute_button.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.next_minute_button.configure(state="disabled")  # Disable initially

        self.selected_video_path = None
        self.selected_file_path = None
        self.current_time = 0  # Initialize current time

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

            self.loading_label.grid()

            self.cut_video_button.configure(state="disabled")

            threading.Thread(target=self.split_video, args=(self.selected_file_path, output_path, seconds)).start()
        else:
            messagebox.showerror("Error", "Please choose a video file.")

    def split_video(self, input_video, output_prefix, segment_duration):
        try:
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

            self.cut_video_button.configure(state="normal")
            messagebox.showinfo("Success", "Vídeo cortado com sucesso")

            self.loading_label.grid_remove()
        except Exception as e:
            self.cut_video_button.configure(state="normal")
            messagebox.showerror("Error", f"Erro ao cortar vídeo: {str(e)}")

            self.loading_label.grid_remove()

    def choose_video_event(self):
        self.selected_video_path = filedialog.askopenfilename()
        if self.selected_video_path:
            # print("Selected video:", self.selected_video_path)
            self.show_thumbnail_vertical(self.selected_video_path)

    def show_thumbnail_vertical(self, file_path, minute=0):
        try:
            clip = VideoFileClip(file_path)
            frame_0 = clip.get_frame(minute * 60)
            frame_15 = clip.get_frame(minute * 60 + 15)
            frame_30 = clip.get_frame(minute * 60 + 30)
            frame_45 = clip.get_frame(minute * 60 + 45)
            
            # Create thumbnails for each frame
            image_0 = Image.fromarray(frame_0)
            image_0.thumbnail((250, 250))
            photo_0 = ImageTk.PhotoImage(image_0)
            
            image_15 = Image.fromarray(frame_15)
            image_15.thumbnail((250, 250))
            photo_15 = ImageTk.PhotoImage(image_15)
            
            image_30 = Image.fromarray(frame_30)
            image_30.thumbnail((250, 250))
            photo_30 = ImageTk.PhotoImage(image_30)
            
            image_45 = Image.fromarray(frame_45)
            image_45.thumbnail((250, 250))
            photo_45 = ImageTk.PhotoImage(image_45)

            # Display thumbnails
            self.thumbnail_label_vertical_0.configure(image=photo_0)
            self.thumbnail_label_vertical_0.image = photo_0
            
            # self.thumbnail_label_vertical_15.configure(image=photo_15)
            # self.thumbnail_label_vertical_15.image = photo_15
            
            self.thumbnail_label_vertical_30.configure(image=photo_30)
            self.thumbnail_label_vertical_30.image = photo_30
            
            # self.thumbnail_label_vertical_45.configure(image=photo_45)
            # self.thumbnail_label_vertical_45.image = photo_45
            
            self.current_time = minute  # Update current time
            if minute + 1 < clip.duration // 60 + 1:
                self.next_minute_button.configure(state="normal")
                self.previous_minute_button.configure(state="normal")
            else:
                self.next_minute_button.configure(state="disabled")
            
            # Update button text
            self.verticalize_part_button.configure(text=f"Verticalizar Minuto {minute + 1}")
            self.cut_part_button.configure(text=f"Cortar Minuto {minute + 1}")

        except Exception as e:
            print("Error:", e)
            
    def cut_part_event(self):
        if self.selected_video_path:
            minute = self.current_time
            input_video = self.selected_video_path
            cut_video_part(input_video, minute)
        else:
            messagebox.showerror("Error", "Please choose a video file.")

    def verticalize_part_event(self):
        if self.selected_video_path:
            minute = self.current_time
            input_video = self.selected_video_path
            verticalize_video(input_video, minute)
        else:
            messagebox.showerror("Error", "Please choose a video file.")

    def next_minute_event(self):
        if self.selected_video_path:
            clip = VideoFileClip(self.selected_video_path)
            next_minute = min(self.current_time + 60, clip.duration)
            clip.close()
            self.current_minute += 1
            self.show_thumbnail_vertical(self.selected_video_path, self.current_minute)
            if next_minute == clip.duration:
                self.next_minute_button.configure(state="disabled")
        else:
            messagebox.showerror("Error", "Please choose a video file.")
            
    def previous_minute_event(self):
        if self.selected_video_path:
            previous_minute = max(self.current_minute - 1, 0)
            self.current_minute = previous_minute  # Atualizar o minuto atual
            self.show_thumbnail_vertical(self.selected_video_path, previous_minute)
            if previous_minute == 0:
                self.previous_minute_button.configure(state="disabled")
        else:
            messagebox.showerror("Error", "Please choose a video file.")

def verticalize_video(input_video, minute):
    try:
        # Carregar o vídeo
        video_clip = VideoFileClip(input_video)
        
        # Obter dimensões do vídeo
        width, height = video_clip.size
        
        # Definir a proporção correta (9:16)
        target_width = int((9 / 16) * height)
        x_offset = (width - target_width) // 2
        
        # Definir o tempo de início e fim para verticalizar somente o minuto escolhido
        start_time = minute * 60
        end_time = (minute + 1) * 60 if (minute + 1) * 60 < video_clip.duration else video_clip.duration
        
        # Cortar o vídeo verticalmente e redimensionar para 1080x1920
        cropped_clip = video_clip.subclip(start_time, end_time).crop(x1=x_offset, y1=0, x2=x_offset + target_width, y2=height)
        resized_clip = resize(cropped_clip, newsize=(1080, 1920))
        
        output_folder = os.path.splitext(input_video)[0]
        os.makedirs(output_folder, exist_ok=True)
        
        output_video = os.path.join(output_folder, f"{os.path.basename(input_video)}_vertical_{minute + 1}.mp4")
        resized_clip.write_videofile(output_video)
        
        video_clip.close()
        resized_clip.close()
        
        messagebox.showinfo("Success", "Vídeo verticalizado com sucesso")
    except Exception as e:
        messagebox.showerror("Error", f"Erro ao verticalizar vídeo: {str(e)}")
        
def cut_video_part(input_video, minute):
    try:
        # Carregar o vídeo
        video_clip = VideoFileClip(input_video)
        
        # Definir o tempo de início e fim para cortar somente o minuto escolhido
        start_time = minute * 60
        end_time = (minute + 1) * 60 if (minute + 1) * 60 < video_clip.duration else video_clip.duration
        
        # Cortar o vídeo
        cut_clip = video_clip.subclip(start_time, end_time)
        
        output_folder = os.path.splitext(input_video)[0]
        os.makedirs(output_folder, exist_ok=True)
        
        output_video = os.path.join(output_folder, f"{os.path.basename(input_video)}_cut_{minute + 1}.mp4")
        cut_clip.write_videofile(output_video)
        
        video_clip.close()
        cut_clip.close()
        
        messagebox.showinfo("Success", "Parte do vídeo cortada com sucesso")
    except Exception as e:
        messagebox.showerror("Error", f"Erro ao cortar parte do vídeo: {str(e)}")