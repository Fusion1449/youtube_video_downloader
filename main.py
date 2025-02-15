import os
import customtkinter as ctk
from tkinter import filedialog
from yt_dlp import YoutubeDL

# Theme configuration
ctk.set_appearance_mode("Dark")  # Dark mode
ctk.set_default_color_theme("green")  # Green theme

# Default download directory
download_path = os.getcwd()


def select_download_directory():
    """Allows the user to choose a directory to save downloads."""
    global download_path
    chosen_path = filedialog.askdirectory()
    if chosen_path:
        download_path = chosen_path
        download_directory_label.configure(text=f"Save to: {download_path}")


def download_audio_file(video_url):
    """Downloads the audio of the video in MP3 format."""
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        audio_config = {
            'format': 'bestaudio/best',
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
        }

        with YoutubeDL(audio_config) as downloader:
            downloader.download([video_url])

        download_status_label.pack_forget()
        show_alert("Success!", "Audio downloaded!")
    except Exception as error:
        download_status_label.pack_forget()
        show_alert("Error!", f"An issue occurred: {error}")


def download_video_file(video_url):
    """Downloads the video in MP4 format."""
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        video_config = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        }

        with YoutubeDL(video_config) as downloader:
            downloader.download([video_url])

        download_status_label.pack_forget()
        show_alert("Success!", "Video downloaded!")
    except Exception as error:
        download_status_label.pack_forget()
        show_alert("Error!", f"An issue occurred: {error}")


def initiate_audio_download():
    url = video_url_entry.get()
    if url:
        download_status_label.configure(text="⌛ Downloading audio...", text_color="blue")
        download_status_label.pack(pady=10)
        window.after(100, download_audio_file, url)
    else:
        show_alert("Warning", "Please enter the video URL.")


def initiate_video_download():
    url = video_url_entry.get()
    if url:
        download_status_label.configure(text="⌛ Downloading video...", text_color="purple")
        download_status_label.pack(pady=10)
        window.after(100, download_video_file, url)
    else:
        show_alert("Warning", "Please enter the video URL.")


def show_alert(title, message):
    """Displays a customized alert window."""
    alert = ctk.CTkToplevel(window)
    alert.title(title)
    alert.geometry("300x200")
    alert.resizable(False, False)

    title_label = ctk.CTkLabel(alert, text=title, font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    message_label = ctk.CTkLabel(alert, text=message, font=("Arial", 14))
    message_label.pack(pady=10)

    ok_button = ctk.CTkButton(alert, text="OK", command=alert.destroy, width=150, height=40)
    ok_button.pack(pady=10)


# Main window configuration
window = ctk.CTk()
window.title("YouTube Video Downloader")
window.geometry("500x400")
window.resizable(False, False)

# Interface elements
window_title = ctk.CTkLabel(window, text="Download Your Videos", font=("Arial", 20))
window_title.pack(pady=20)

video_url_entry = ctk.CTkEntry(window, placeholder_text="Enter the video URL", width=400)
video_url_entry.pack(pady=10)

choose_directory_button = ctk.CTkButton(window, text="Choose Directory", command=select_download_directory)
choose_directory_button.pack(pady=10)

download_directory_label = ctk.CTkLabel(window, text=f"Save to: {download_path}", font=("Arial", 12))
download_directory_label.pack(pady=5)

download_status_label = ctk.CTkLabel(window, text="", font=("Arial", 14))

audio_download_button = ctk.CTkButton(window, text="Download Audio", command=initiate_audio_download, width=200)
audio_download_button.pack(pady=10)

video_download_button = ctk.CTkButton(window, text="Download Video", command=initiate_video_download, width=200)
video_download_button.pack(pady=10)

# Run the application
window.mainloop()
