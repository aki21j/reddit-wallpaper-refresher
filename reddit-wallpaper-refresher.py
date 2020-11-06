import requests
import logging
import sys
import os
from argparse import ArgumentParser
import random

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

BASE_URL = "https://www.reddit.com/r/"

AGENT_NAME = 'reddit-wallpaper-refresher 1.0'

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

def fetch_image_and_refresh_background(save_dir):
	
	idx = random.randint(0, len(POPULAR_SUBS) - 1)
	subreddit = POPULAR_SUBS[idx]

	logger.info("Selected subreddit is %s" % subreddit)

	data = fetch_data(subreddit)
	post_idx = random.randint(0, len(data) - 1)
	selected_post = data[post_idx]['data']
	image_file_path = download_image(save_dir, selected_post)
	set_background_image(image_file_path)


def refresh_random_background(save_dir):

	directory_seq = os.listdir(save_dir)

	if not len(directory_seq):
		logger.error("Empty directoy, select a directory with images.")
		sys.exit()

	selected_file = random.choice(os.listdir(save_dir))
	image_file_path = save_dir + selected_file
	set_background_image(image_file_path)


def fetch_data(subreddit):
	try:
		url = BASE_URL + subreddit + ".json?limit=100"
		response = requests.get(url,headers={'User-agent': AGENT_NAME})

		if response.status_code != 200:
			logger.error(response.status_code)
			sys.exit()

		return response.json()['data']['children']

	except Exception as e:
		logger.error(e)

def download_image(save_dir, post_dict):
	url = post_dict['url']
	title = post_dict['title']
	if '.jpg' or '.jpeg' in url:
		extension = '.jpeg'  
	elif '.png' in url:
		extension = '.png'
	else:
		url += '.jpeg'
		extension = '.jpeg'

	file_path = save_dir + title + extension

	if os.path.exists(file_path):
		return file_path

	try:
		response = requests.get(url, allow_redirects = False)

		if response.status_code != 200:
			logger.error("Couldn't download image, exiting.")
			sys.exit()
		output_file = open(file_path, mode='bx')
		output_file.write(response.content)
		return file_path

	except Exception as e:
		logger.error(e)

def set_background_image(image_path):
	try:
		os.system("gsettings set org.gnome.desktop.background picture-uri " + "'" + image_path + "'")
		logger.info('Successfully update desktop background.')  
	except Exception as e:
		logger.error(e)

def main():
	parser = ArgumentParser()
	parser.add_argument("-o","--option", required=True,
					help="""select either option:
									1 to download a new image and refresh desktop background. 
									2 to refresh desktop background from existing collection.""")
	
	args = parser.parse_args()
	selected_option = int(args.option)

	HOME = os.path.expanduser("~")
	DEFAULT_SAVE_DIRECTORY = HOME + "/Pictures/Wallpapers/"

	if not os.path.exists(DEFAULT_SAVE_DIRECTORY):
		os.makedirs(DEFAULT_SAVE_DIRECTORY)

	if selected_option == 1:
		# download and set wallpaper
		fetch_image_and_refresh_background(DEFAULT_SAVE_DIRECTORY)
	elif selected_option == 2:
		# refresh with a random wallpaper
		refresh_random_background(DEFAULT_SAVE_DIRECTORY)
	else:
		logger.error("Select a valid option, 1 or 2.")

if __name__ == "__main__":
	main()