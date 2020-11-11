# Update all the things!

This little django project helps you to keep your devices firmware up to date.

**But why?**   
Todays Laptops and Smartphone have an automated integrated update mechanism to keep the Software and firmware up to date (if there are patches provided). For my other equipment I have to manually check if there is an update and download it.
For example WLAN-Router or Switch Firmware are painful to keep track. making things worse, there is usually no API which you can query.

So this project aims to provide a plugin system for scraping the manufacturers support sites for new firmware updates.
New Firmware Versions of configured products can generate email or pushover notifications.

the webui is an unnecessary gimmick.

## Features
* plugin-system for easy extending for unlimited amount of manufacturers
* pull mechanism to download firmware
* notifications on new versions (email, pushover)

## Plugins
Available plugins (my device coverage) [see also [src/plugins](src/plugins/)]:   
* Supermicro Firmware Plugin for BIOS and BMC
* Zyxel Firmware Plugin
* Grandstream Firmware Plugin
* Ubiquiti Firmware Plugin


![](img/update-all-the-things.jpg)