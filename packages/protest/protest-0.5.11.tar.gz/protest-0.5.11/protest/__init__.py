# protest.py
# by aaron montoya-moraga

# dependencies
import os
from os import system
import sys
import time
import string
import random
import urllib
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import youtube_dl


def images(subject):
    '''this function creates protesting material using images from google'''

    # print message
    print "open new google chrome window"

    # new driver using google chrome
    driver = webdriver.Chrome()

    # set the window size of the driver
    driver.set_window_size(1200, 800)

    # wait for 5 seconds
    time.sleep(2)

    # url to be scraped
    base_url = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1044&bih=584&q="

    # retrieve the argument from the function
    handle = subject

    # reconstruct the complete url
    complete_url = base_url + handle

    #print message
    print "go to google and search for images"

    # go to the url
    driver.get(complete_url)

    # wait for 2 seconds
    time.sleep(2)

    # print message
    print "scrolling up and down to load a lot of pics"

    # scroll up and down to make more images appear
    for i in range(10):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.1)

    #print message
    print "click on the show more results button"

    #retrieve buttons
    buttons = driver.find_elements_by_id("smb")

    #print buttons
    print buttons

    #click on the button
    buttons[0].click()

    # scroll up and down to make more images appear
    for i in range(10):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.1)

    # scroll down
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")

    # print message
    print "create folders for storing pics"

    # create folder for storing pics
    picsFolder = "pics_" + subject
    system("mkdir " + picsFolder)
    system("cd " + picsFolder)

    # print message
    print "find all of the images"

    # find images
    images = driver.find_elements_by_tag_name("img")

    # reset counter
    counter = 0

    # print message
    print "download every image"

    # iterate through all of the images
    for image in images:
        imageSrc = image.get_attribute('currentSrc')
        print imageSrc
        try:
            # save the images to the pics folder, as counter.png
            urllib.urlretrieve(imageSrc, "./pics_" + subject + "/" + str(counter) + ".png")
            counter = counter + 1
        except:
            print "this image couldn't be downloaded"


    #list of protest words
    protestWords = ["OH NO", "STOP THIS", "UGH", "NOPE"]

    #define extensions
    prePath = "./pics_" + subject + "/"
    pngExtension = ".png"


    print (os.getcwd() + "\n")

    #pick font
    #fnt = ImageFont.truetype('Comic_Sans_MS.ttf', 30)
    #fnt = ImageFont.truetype('./Comic_Sans_MS.ttf.ttf', 30)
    #fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
    #fnt = ImageFont.truetype("arial.ttf", 15)
    fnt = ImageFont.load_default()
    #fnt = ImageFont.truetype("arial")

    print "put protest stuff on top"
    # iterate through every pic in the folder
    for counter in range(len(os.listdir(prePath)) - 1):
        # build path to pic
        path = prePath + str(counter)
        print path
        # open the image
        img = Image.open(path + pngExtension)
        img = img.convert('RGB')
        # retrieve dimensions of pic
        picWidth, picHeight = img.size
        # canvas element is an instace of ImageDraw
        canvas = ImageDraw.Draw(img)
        # fnt element is an instance of ImageFont
        text = protestWords[random.randint(1, len(protestWords) - 1)]
        # get text size
        text_size = fnt.getsize(text)

        # button
        button_size = (text_size[0]+30, text_size[1]+30)
        button_img = Image.new('RGB', button_size, "black")
        button_draw = ImageDraw.Draw(button_img)
        button_draw.text((10, 10), text, font=fnt)
        img.paste(button_img, (random.randint(0, picWidth), random.randint(0, picHeight)))

        #canvas.text((random.randint(0, 300), random.randint(0, 500)), text, fill=(0, 0, 0), font=fnt)
        #canvas.text((random.randint(0, picWidth), random.randint(0, picHeight)), text, font=fnt, fill=(0,0,0,255))
        img.save(path + pngExtension)

    # print message
    print "close browser"

    # close the browser
    driver.quit()

def videos(subject):

    # print message
    print "open new google chrome window"

    # new driver using google chrome
    driver = webdriver.Chrome()

    # set the window size of the driver
    driver.set_window_size(1200, 800)

    # wait for 5 seconds
    time.sleep(2)

    # url to be scraped
    base_url = "https://www.youtube.com/results?search_query="

    #retrieve the argument from the function
    handle = subject

    # reconstruct the complete url
    complete_url = base_url + handle

    # print message
    print "go to youtube and search for videos"

    # go to the url
    driver.get(complete_url)

    # wait for 2 seconds
    time.sleep(2)

    #print message
    print "retrieve videos"

    #retrieve videos
    videos = driver.find_elements_by_css_selector('h3 > a')

    #print message
    print "create folder for storing videos"

    #create folder for storing pics
    videosFolder = "videos_" + subject
    system("mkdir " + videosFolder)
    system("cd " + videosFolder)

    counter = 0

    #download videos
    for video in videos:
        address = video.get_attribute("href")
        print address
        if len(address) < 45:
            youtube_dl.YoutubeDL({'format': 'mp4'}).download([address])

#function for sending protest emails
def emails(subject):
    '''this function creates protesting emails'''

#function for sending protest tweets
def tweets(subject):
    '''this function creates protesting tweets'''

#function for creating avatars, profile pics and banners for social media
def social_media(subject):
    '''this function creates social media protesting avatars'''
