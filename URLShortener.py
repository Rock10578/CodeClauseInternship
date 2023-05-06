import pyshorteners as s

URL = input('Enter URL : ')
shortenedURL = s.Shortener().tinyurl.short(URL)
print('Shortened URL : ',shortenedURL)