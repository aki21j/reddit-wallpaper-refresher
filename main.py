import requests
import logging
import sys

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

BASE_URL = "https://www.reddit.com/r/"

POPULAR_SUBS = [
  "wallpapers",
  "wallpaper",
  "EarthPorn", 
  "CityPorn", 
  "SkyPorn", 
  "WeatherPorn",
  "BotanicalPorn",
  "LakePorn",
  "VillagePorn",
  "BeachPorn",
  "WaterPorn",
  "SpacePorn"
]

def fetch_data(subreddit):
  try:
    url = BASE_URL + subreddit + ".json"
    response = requests.get(url,headers={'User-agent': 'your-bot-name 0.1'})

    if response.status_code != 200:
      logger.error(response.status_code)
      sys.exit()

    return response.json()['data']['children']

  except Exception as e:
    logger.error(e)

def download_image(post_dict):
  url = post_dict['url']
  title = post_dict['title']
  if '.jpg' or '.jpeg' in url:
    extension = '.jpeg'  
  elif '.png' in url:
    extension = '.png'
  else:
    url += '.jpeg'
    extension = '.jpeg'

  try:
    response = requests.get(url, allow_redirects = False)

    if response.status_code != 200:
      logger.error("Couldn't download image, exiting.")
      sys.exit()
    output_file = open(title + extension, mode='bx')
    output_file.write(response.content)
    return

  except Exception as e:
    logger.error(e)


def main():
  subreddit = "wallpapers"
  data = fetch_data(subreddit)
  first_post = data[0]['data']
  download_image(first_post)
  

if __name__ == "__main__":
  main()