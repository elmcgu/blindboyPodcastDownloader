from bs4 import BeautifulSoup
import requests
import re
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


rssFeedSource="https://feeds.acast.com/public/shows/9d5c107b-68d6-4c1b-8c80-45ee6a84c947"
rssFeedXML = "podcastPageXML"

print('fetching')
r = requests.get(rssFeedSource)
f = open(rssFeedXML+".xml","wb")
f.write(r.text.encode('utf-8'))
f.close()




# Reading the data inside the xml file to a variable under the name  data
with open(rssFeedXML +'.xml', 'r') as n:
    data = n.read()

# Passing the stored data inside the beautifulsoup parser
bs_data = BeautifulSoup(data, 'xml')




podTitle = bs_data.find("title")
print("**PODCAST TITLE**")
#remove pesky xml tags(re = regular expression module)
podTitleString = re.sub(r'<.*?>', '', str(podTitle))
print(podTitleString)
podDesc = bs_data.find("itunes:subtitle")
print("**PODCAST DESCRIPTION**")
podDescString = re.sub(r'<.*?>', '', str(podDesc))
print(podDescString)

#Info on latest Episode (.find always gets first instance)
print("**LATEST EPISODE**")
epItem = bs_data.find("item")
latestTitle=epItem("itunes:title")
latestTitleString = re.sub(r'<.*?>', '', str(latestTitle))
print(latestTitleString)
latestDesc=epItem("itunes:subtitle")
latestDescString = re.sub(r'<.*?>', '', str(latestDesc))
print(latestDescString)
latestDate=epItem("pubDate")
latestDateString = re.sub(r'<.*?>', '', str(latestDate))
print(latestDateString)




episodes = bs_data.findAll('itunes:title')

#How many episodes
print("There are this many episodes in total - " + str(len(episodes)))
print("**ALL EPISODE TITLES**")
for episode in episodes:
    epTitleString = re.sub(r'<.*?>', '', str(episode))
    print(epTitleString)



#Get the Url for mp3 download of latest episode
latestEnc=bs_data.find("enclosure")
urlMp3=latestEnc["url"]
print(urlMp3)




r = requests.get(urlMp3)


filename = latestTitleString+ ".mp3"

with open(filename, 'wb') as f:
        # You will get the file in base64 as content
        f.write(r.content)
print(latestTitleString +" has been downloaded to the location of this py file.")

def convert2Wav(filename):
    # assign files
    inputFile = filename
    outputFile = latestTitleString + ".wav"

    # convert mp3 file to wav file
    sound = AudioSegment.from_mp3(inputFile)
    sound.export(outputFile, format="wav", parameters=["-ac","2","-ar","8000"])

def get_large_audio_transcription(outputFile):
    # create a speech recognition object
    r = sr.Recognizer()

    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(outputFile)
    # split audio sound where silence is 300 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 300,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=300,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected


    with open(latestTitleString+'transcript.txt', 'w') as f:

            f.write(whole_text)


ask1=input("Would you like to transcribe the podcast episode? ")
if ask1.lower() == "yes":
    convert2Wav(latestTitleString + ".mp3")
    get_large_audio_transcription(latestTitleString + ".wav")
else:
    exit(0)






