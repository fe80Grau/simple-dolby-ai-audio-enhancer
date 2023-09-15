FROM python:3.9
WORKDIR /opt/simple-dolby-ai-audio-enhancer
COPY . /opt/simple-dolby-ai-audio-enhancer
RUN pip install --no-cache-dir --upgrade -r /opt/simple-dolby-ai-audio-enhancer/requierments.txt
RUN apt update
RUN apt -y install ffmpeg
CMD ["python", "main.py"]
EXPOSE 80