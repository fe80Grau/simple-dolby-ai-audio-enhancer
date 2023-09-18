# Simple Dolby AI Audio Enhancer
* Test the power here.. https://dashboard.dolby.io/media-demo/ (Only enhance 30 secs, original sample)
* Login in Dolby.io Dashboard to get App key and App secret. (https://docs.dolby.io/media-apis/docs/guides-api-authentication#generating-an-api-token)
* Clone this repo and rename config.example.json to config.json, enter your Dolby key and secret
* Deploy with docker (or running python main.py)
* Enjoy a simple web AI Enhancer with no time limits 😋 (Uploaded videos will be compressed with h264)
* A guide to understand the params in GUI. https://docs.dolby.io/media-apis/docs/audio-quality (look for the Audio Guide section of the left menu)
![image](https://github.com/fe80Grau/simple-dolby-ai-audio-enhancer/assets/6680464/31b0a041-3311-451e-af8a-a51b131ffd05)
![image](https://github.com/fe80Grau/simple-dolby-ai-audio-enhancer/assets/6680464/bf94d103-71d7-4a6e-bc5e-f30620d515d1)


<a href="https://www.buymeacoffee.com/fe80grau" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="width: 120px !important;" ></a>

## Installation
# Docker

```console
cd /opt && git clone https://github.com/fe80Grau/simple-dolby-ai-audio-enhancer.git
```

```console
cd /opt/simple-dolby-ai-audio-enhancer
```

* Rename and edit config.json (paste here your key and secret from Dolby.io Dashboard)
```console
mv config.example.json config.json && vim config.json
```

```console
docker build . -t "simple-dolby-ai-audio-enhancer" 
```

```console
docker run -p 8080:80 --restart=always --name simple-dolby-ai-audio-enhancer simple-dolby-ai-audio-enhancer
```

* Check the GUI in the browser
```console
http://localhost:8080/
```


