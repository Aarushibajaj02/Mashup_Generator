# Mashup Generator 

Welcome to the Mashup Generator! This Streamlit web application empowers you to create personalized mashups by combining your favorite songs from YouTube. Just input an artist’s name, and let the app do the rest—searching for songs, downloading them, trimming to your desired length, and merging them into a single audio file. You can even receive your mashup directly in your inbox!

**Usage**

-Enter the artist's name to search for songs.

-Specify how many songs to retrieve (1 to 10).

-Set the duration for trimming each song (5 to 120 seconds).

-Provide your email address for sending the mashup.

-Click on "Generate Mashup" to start the process.

**Interface**

![Screenshot 2024-10-20 230947](https://github.com/user-attachments/assets/aee46797-25eb-40cc-a2b2-e52fe99b35bc)

![Screenshot 2024-10-20 230742](https://github.com/user-attachments/assets/85150ef5-4849-45a3-9409-24c3b45f7445)


**Key Features**

-_YouTube Integration_: Utilizes the YouTube Data API to search and retrieve audio content from videos.

-_Audio Processing_: Trims and merges audio files using the powerful pydub library.

-_Email Delivery_: Sends the final mashup as a zip file to your email via Gmail’s SMTP server.


Run the app

1.Clone the repository or download the code files.

2.Navigate to the directory in your terminal.

3.Launch the app using Streamlit:

   ``` streamlit run streamlit_app.py
   ```
