from bs4 import BeautifulSoup
import requests
import re


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


