import streamlit as st
import yt_dlp
import os
import uuid

# Configure the Streamlit page
st.set_page_config(page_title="YT to MP3", page_icon="🎧", layout="centered")

st.title("YouTube to MP3 Downloader 🎧")
st.markdown("Enter a YouTube URL below to extract the highest quality audio.")

# Create a temporary directory for processing
temp_dir = "temp_downloads"
os.makedirs(temp_dir, exist_ok=True)

url = st.text_input("Enter YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Extract Audio", type="primary"):
    if url.strip() == "":
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Downloading and converting to MP3... This might take a minute depending on the video length."):
            # Generate a unique ID for the file to prevent server conflicts
            file_id = str(uuid.uuid4())
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320', # Highest standard quality
                }],
                'outtmpl': f'{temp_dir}/{file_id}.%(ext)s',
                'quiet': True,
                'no_warnings': True
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract info and download
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', 'youtube_audio')
                    
                    # yt-dlp appends .mp3 after the ffmpeg conversion
                    file_path = f"{temp_dir}/{file_id}.mp3"

                    # Check if the file was created successfully
                    if os.path.exists(file_path):
                        st.success(f"Successfully processed: **{video_title}**")
                        
                        # Read file into memory for the download button
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="Download MP3",
                                data=file,
                                file_name=f"{video_title}.mp3",
                                mime="audio/mpeg"
                            )
                            
                        # Clean up the file from the server immediately to save space
                        os.remove(file_path)
                    else:
                        st.error("Conversion failed. Please try a different video.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
