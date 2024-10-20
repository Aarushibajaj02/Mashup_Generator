import os
import streamlit as st
from googleapiclient.discovery import build
from pytube import YouTube
from pydub import AudioSegment
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# YouTube Data API credentials
YOUTUBE_API_KEY = 'AIzaSyD8t2XsQ8IZEgeZmTIX6CVyXIdUpVhSbxU'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def search_youtube_videos(query, n):
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=n,
        type='video'
    ).execute()
    
    video_urls = []
    for item in search_response['items']:
        video_id = item['id']['videoId']
        video_urls.append(f"https://www.youtube.com/watch?v={video_id}")
    
    return video_urls

def download_song(video_url):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        file_path = stream.download()  # Downloads the file
        return file_path
    except Exception as e:
        print(f"Error downloading song: {e}")
        return None

def trim_and_merge_songs(file_paths,duration):
    merged_audio = AudioSegment.empty()
    
    for file in file_paths:
        if file.endswith(".mp3"):
            song = AudioSegment.from_file(file, format="mp3")
        elif file.endswith(".wav"):
            song = AudioSegment.from_file(file, format="wav")
        else:
            print(f"Unsupported format for {file}")

        trimmed_song = song[:duration * 1000]  # trim duration in milliseconds
        merged_audio += trimmed_song
    
    merged_output = "merged.mp3"
    merged_audio.export(merged_output, format="mp3/wav")
    return merged_output

def create_zip_file(files, zip="output.zip"):
    with zipfile.ZipFile(zip, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    return zip

def send_email(zip_filepath, recipient_mail):
    sender_email = 'aarushibajaj2004@gmail.com'
    sender_password = 'qupu gcky ptnd yxoq'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_mail
    msg['Subject'] = "Your Downloaded Songs"

    body = "Please find attached the zip file of the trimmed songs."
    msg.attach(MIMEText(body, 'plain'))

    with open(zip_filepath, "rb") as attachment:
        msg.attach(MIMEText(attachment.read(), 'base64', 'zip'))
        msg.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_filepath)}')

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_mail, msg.as_string())
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")

st.markdown("<h1 style='color: orange;'>Mashup Generator</h1>", unsafe_allow_html=True)

singer = st.text_input("Enter singer name", "")
n_songs = st.number_input("Number of songs", min_value=1, max_value=10)
trim_duration = st.number_input("Duration of each song (seconds)", min_value=5, max_value=120)
email = st.text_input("Enter your email address", "")

if st.button("Generate Mashup"):
    if singer:
        st.write(f"Searching for {n_songs} songs by '{singer}'...")

        video_urls = search_youtube_videos(singer, n_songs)
        st.write(f"Found {len(video_urls)} songs.")

        file_paths = []
        for url in video_urls:
            st.write(f"Downloading song")
            song_path = download_song(url)
            file_paths.append(song_path)

        merged_file = trim_and_merge_songs(file_paths, trim_duration)
        st.success("Songs merged successfully!")
       
        zip_file = create_zip_file([merged_file], zip_name=f"{singer}_mashup.zip")
        
        if email:
            send_email(zip_file, email)
            st.success(f"Mashup sent to '{email}'!")
        else:
            st.error("Please enter a valid email address.")
    else:
        st.error("Please enter a valid singer's name")
