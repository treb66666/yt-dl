import streamlit as st
import asyncio
import os
from pybalt import download

# Configure the Streamlit page
st.set_page_config(page_title="Cloud YT Downloader", page_icon="☁️", layout="centered")

st.title("Cloud YouTube to MP3 ☁️")
st.markdown("This app uses the free **Cobalt API network** to securely extract audio, completely bypassing YouTube's server blocks!")

url = st.text_input("Enter YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")

async def fetch_audio(video_url):
    # pybalt handles finding a working Cobalt server and downloading the file
    # We request the MP3 format and a 320kbps bitrate target
    return await download(
        video_url,
        audioFormat="mp3",
        audioBitrate="320",
        filenameStyle="pretty"
    )

if st.button("Extract Audio", type="primary"):
    if url.strip() == "":
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Sending request to Cobalt servers... (This is usually much faster than local extraction!)"):
            try:
                # Streamlit is synchronous, so we run the async pybalt function using asyncio
                file_path = asyncio.run(fetch_audio(url))
                
                if file_path and os.path.exists(file_path):
                    st.success("Successfully processed by Cobalt!")
                    
                    # Read file into memory for the download button
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="Download MP3",
                            data=file,
                            file_name=os.path.basename(file_path),
                            mime="audio/mpeg"
                        )
                        
                    # Clean up the file from the Streamlit server to save space
                    os.remove(file_path)
                else:
                    st.error("Conversion failed. The Cobalt network might be overloaded or the video is restricted.")
            except Exception as e:
                st.error(f"An API error occurred: {e}")
