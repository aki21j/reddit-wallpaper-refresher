# reddit-wallpaper-refresher
Python app that can download images from the following subreddits: 
- wallpapers
- wallpaper
- EarthPorn 
- CityPorn 
- SkyPorn 
- WeatherPorn
- BotanicalPorn
- LakePorn
- VillagePorn
- BeachPorn
- WaterPorn
- SpacePorn

It has two available options:
1. Download an image and set it as the active desktop background.
2. To refresh your desktop background from the list of images available under ```${HOME}/Pictures/Wallpapers```.

#### Steps to install:
- clone repo
- pip3 install -r requirements.txt
- To select option 1, run ```python reddit-wallpaper-refresher.py -o 1```.
- For option 2, run ```python reddit-wallpaper-refresher.py -o 2```
- To open the cli help, run ```python reddit-wallpaper-refresher.py -o --help```

#### Supported OS:
- Ubuntu