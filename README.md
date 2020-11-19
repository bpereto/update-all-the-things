# Update all the things!

This little django project helps you to keep your devices firmware up to date.

**But why?**   
Todays Laptops and Smartphone have an automated integrated update mechanism to keep the Software and firmware up to date (if there are patches provided). For my other equipment I have to manually check if there is an update and download it.
For example WLAN-Router or Switch Firmware are painful to keep track. making things worse, there is usually no API which you can query.

So this project aims to provide a plugin system for scraping the manufacturers support sites for new firmware updates.
New Firmware Versions of configured products can generate email or pushover notifications.

the webui is an unnecessary gimmick.   
Admittedly a script could also do the job, but with django its smooth and very easy to accomplish a simple application with CLI, database and Webui.   
enjoy.

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

### Supermicro Firmware Plugin for BIOS
Plugin Config for Supermicro Firmware BIOS. The Product ID and Product Name from the Search Request on [https://www.supermicro.com/support/resources/?mlg=0](https://www.supermicro.com/support/resources/?mlg=0) is needed.
```
{
    "supermicro_product_name": "A2SDi-8C+-HLN4F+",
    "supermicro_product_id": "86099"
}
```

### Supermicro Firmware Plugin for BMC
Plugin Config for Supermicro BMC Firmware. the Product ID and Product Name from the Search Request on [https://www.supermicro.com/support/resources/?mlg=0](https://www.supermicro.com/support/resources/?mlg=0) is needed.
```
{
    "supermicro_product_name": "A2SDi-8C+-HLN4F+",
    "supermicro_product_id": "86099"
}
```

### Zyxel Firmware Plugin
Plugin Config for Zyxel Firmware Plugin. Product Name is needed.
```
{
    "zyxel_product_name":"GS1900-8"
}
```

### Grandstream Firmware Plugin
Plugin Config for Grandstream Firmware Plugin. Product Name is needed.
```
{
    "grandstream_product_name": "HT801"
}
```

### Ubiquiti Firmware Plugin
Plugin Config for Ubiquiti Firmware Plugin. Product Filter name is needed from download site.   
ex. https://www.ui.com/download/edgemax/edgerouter-4/er-4 -> `er-4`
```
{
    "ubiquiti_product_filter":"er-4"
}
```

![](img/update-all-the-things.jpg)

## Install
* Install on k8s, see [helm/README.md](helm/README.md)
* There is a fixture to add some products. [src/upd/fixtures/setup/products.yaml](src/upd/fixtures/setup/products.yaml)

## Develop
```
docker-compose -f docker-compose.dev.yml up
```

## Todos / Future Features
* Trigger for update of the metadata
* eventually, background tasks for metadata update. this is overkill for managing a few products.