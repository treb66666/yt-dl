import streamlit as st
import requests
import os
import uuid

# Configure the Streamlit page
st.set_page_config(page_title="Cloud YT Downloader", page_icon="☁️", layout="centered")

st.title("Cloud YouTube to MP3 ☁️")
st.markdown("This app uses the free **Cobalt API** directly to securely extract audio, bypassing broken wrappers!")

url = st.text_input("Enter YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Extract Audio", type="primary"):
    if url.strip() == "":
        st.warning("Please enter a valid URL.")
    else:
        # Clean the URL of any playlist tags automatically
        clean_url = url.split('&')[0]
        
        with st.spinner("Connecting directly to Cobalt's main API..."):
            try:
                # Cobalt v10 API endpoint
                api_url = "https://api.cobalt.tools/"
                
                # Standard headers to bypass basic bot-protection blocks
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
                
                # Request an MP3 payload
                payload = {
                    "url": clean_url,
                    "audioFormat": "mp3",
                    "isAudioOnly": True
                }
                
                response = requests.post(api_url, json=payload, headers=headers)
                data = response.json()
                
                # Check if Cobalt gave us a direct download link
                if "url" in data:
                    download_url = data["url"]
                    st.info("Extraction successful! Transferring file to your app...")
                    
                    # Download the MP3 to the Streamlit server
                    file_response = requests.get(download_url)
                    file_id = str(uuid.uuid4())
                    file_path = f"{file_id}.mp3"
                    
                    with open(file_path, "wb") as f:
                        f.write(file_response.content)
                        
                    st.success("Ready for download!")
                    
                    # Read into memory for the download button
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="Download MP3",
                            data=file,
                            file_name="cobalt_audio.mp3",
                            mime="audio/mpeg"
                        )
                        
                    # Clean up the server space
                    os.remove(file_path)
                    
                # If Cobalt refused the link, it returns a 'text' error
                elif "text" in data:
                    st.error(f"Cobalt Server Error: {data['text']}")
                else:
                    st.error("Received an unknown response from the server. It may be overloaded.")
                    
            except Exception as e:
                st.error(f"An API connection error occurred: {e}")
