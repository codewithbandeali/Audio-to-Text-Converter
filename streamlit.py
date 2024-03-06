import streamlit as st
from gtts import gTTS
import os
import base64

# Function to generate download link
def get_download_link(file_path, file_name):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
        download_link = f'<a href="data:audio/mp3;base64,{b64}" download="{file_name}">Click here to download</a>'
        return download_link

# Page configuration
st.set_page_config(page_title="Text to Audio App", layout="wide")

# Streamlit app title
st.title("Text to Audio Converter")

# User input for text
text_input = st.text_area("Enter your text:")

# Button to trigger text-to-audio conversion
if st.button("Convert to Audio"):
    # Split the text into chunks of 500 characters (you can adjust this number)
    chunk_size = 500
    text_chunks = [text_input[i:i + chunk_size] for i in range(0, len(text_input), chunk_size)]

    # Create a folder to save the audio files
    output_folder = "audio_chunks"
    os.makedirs(output_folder, exist_ok=True)

    # Generate and save audio for each chunk
    for i, chunk in enumerate(text_chunks):
        tts = gTTS(text=chunk, lang='en', slow=False)
        audio_file_path = os.path.join(output_folder, f"chunk_{i+1}.mp3")
        tts.save(audio_file_path)

    # Concatenate the audio files into a single file
    concatenated_audio_path = os.path.join(output_folder, "output.mp3")
    with open(concatenated_audio_path, 'wb') as outfile:
        for i in range(len(text_chunks)):
            chunk_path = os.path.join(output_folder, f"chunk_{i+1}.mp3")
            with open(chunk_path, 'rb') as infile:
                outfile.write(infile.read())

    # Provide download link for the generated audio file
    if os.path.exists(concatenated_audio_path):
        # Play the audio on the page
        audio_bytes = open(concatenated_audio_path, 'rb').read()
        st.audio(audio_bytes, format='audio/mp3')

        # Provide download link
        download_link = get_download_link(concatenated_audio_path, "output.mp3")
        st.markdown(download_link, unsafe_allow_html=True)
    else:
        st.error(f"Audio file '{concatenated_audio_path}' not found.")
