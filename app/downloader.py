import yt_dlp
import os
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # pasta raiz do projeto
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video(url, format_type="mp3"):
    video_id = str(uuid.uuid4())
    filename = f"{video_id}.{format_type}"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if format_type == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'prefer_ffmpeg': True,
            'noplaylist': True,
            'quiet': False
        }
    elif format_type == "mp4":
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': False,
        }
    else:
        raise ValueError("Formato inválido. Use 'mp3' ou 'mp4'.")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        original_file = ydl.prepare_filename(info)
        converted_file = os.path.splitext(original_file)[0] + f'.{format_type}'

        if not os.path.exists(converted_file):
            raise FileNotFoundError(f"Arquivo convertido não encontrado: {converted_file}")

        os.rename(converted_file, filepath)

    return filepath
