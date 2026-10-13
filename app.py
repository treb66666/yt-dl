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
        
        with st.spinner("Connecting directly to Cobalt's v10 API..."):
            try:
                # Cobalt v10 API endpoint
                api_url = "https://api.cobalt.tools/"
                
                # Standard headers for the v10 API
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
                
                # The v10 API uses "downloadMode" instead of the old "isAudioOnly" parameter
                payload = {
                    "url": clean_url,
                    "audioFormat": "mp3",
                    "downloadMode": "audio"
                }
                
                response = requests.post(api_url, json=payload, headers=headers)
                data = response.json()
                
                # Cobalt v10 returns a 'status' key to define the response type
                status = data.get("status")
                
                if status in ["redirect", "tunnel"]:
                    download_url = data.get("url")
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
                    
                elif status == "error":
                    # The error text is nested inside an 'error' dictionary in v10
                    error_text = data.get("error", {}).get("text", "Unknown API error")
                    st.error(f"Cobalt Server Error: {error_text}")
                    
                else:
                    # Print the raw data to the screen so we aren't flying blind if the API changes again
                    st.error(f"Received an unsupported response status '{status}'. Raw data: {data}")
                    
            except Exception as e:
                st.error(f"An API connection error occurred: {e}")
