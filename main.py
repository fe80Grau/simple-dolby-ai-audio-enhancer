import asyncio
import os
import json
import sys
import time
import ffmpeg
import mimetypes
from flask import Flask, render_template, request
from dolbyio_rest_apis import authentication
from dolbyio_rest_apis.media import io
from dolbyio_rest_apis.media import enhance
from sanitize_filename import sanitize
from clases.config import config as c


config = c.config('./config.json').get_config()

APP_KEY = config['APP_KEY']
APP_SECRET = config['APP_SECRET']

app = Flask(__name__, static_folder='static', static_url_path='')
loop = asyncio.get_event_loop()
mimetypes.init()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        
        file = request.files['file']
        filename = sanitize(file.filename).replace(' ','_')
        file_path = f'./tmp/{filename}'
        ffmpeg_path = file_path.replace(filename, f'ffmpeg-{filename}')
        file.save(file_path)

        if 'video' in mimetypes.guess_type(file_path)[0]:
            ffmpeg.input(file_path).output(ffmpeg_path, acodec="aac", vcodec="h264").run()
        else:
            ffmpeg_path = file_path
        
        task = authentication.get_api_token(APP_KEY, APP_SECRET, 2 * 60 * 60)
        at = loop.run_until_complete(task)
        
        input_url = f'dlb://in/{filename}'
        task = io.get_upload_url(access_token=at.access_token, dlb_url=input_url)
        upload_url = loop.run_until_complete(task)
        
        task = io.upload_file(upload_url=upload_url, file_path=ffmpeg_path)
        loop.run_until_complete(task)
        
        output_url = f'dlb://out/{filename}'
        
        content_type = request.form.get('content_type')
        sibilance_reduction = request.form.get('sibilance_reduction')
        click_reduction = bool(request.form.get('click_reduction'))
        plosive_reduction = request.form.get('plosive_reduction')
        noise_reduction = request.form.get('noise_reduction')
        target_level = int(request.form.get('target_level'))
        speech_threshold = int(request.form.get('speech_threshold'))
        dynamics_range_control = bool(request.form.get('dynamics_range_control'))
        
        job = {
            'input': input_url,
            'output': output_url,
            'content': {
                'type': content_type,
            },
            "audio": {
                "speech": {
                    "sibilance": {
                        "reduction": {
                            "amount": sibilance_reduction
                        }
                    },
                    "click": {
                        "reduction": {
                            "enable": click_reduction,
                        }
                    },
                    "plosive": {
                        "reduction": {
                        "amount": plosive_reduction
                        }
                    }
                },
                "noise": {
                    "reduction": {
                        "amount": noise_reduction
                    }
                },
                "loudness": {
                    "target_level": target_level,
                    "speech_threshold": speech_threshold,
                    "peak_reference": "sample",
                    "peak_limit": -2
                },
                "dynamics": {
                    "range_control": {
                        "enable": dynamics_range_control,
                        "amount": "max"
                    }
                }
            }
        }
        
        job_str = json.dumps(job, indent=4)
        
        task = enhance.start(at.access_token, job_str)
        job_id = loop.run_until_complete(task)
        
        task = enhance.get_results(at.access_token, job_id)
        result = loop.run_until_complete(task)
        while result.status in ('Pending', 'Running'):
            print(f'Job status is {result.status}, {result.progress}% taking a 5 second break...')
            time.sleep(5)
        
            task = enhance.get_results(at.access_token, job_id)
            result = loop.run_until_complete(task)
        
        if result.status != 'Success':
            print('There was a problem with processing the file')
            print(json.dumps(result, indent=4))
            sys.exit(1)
        
        output_path = './static'
        output_file = '{}_enhacement.{}'.format(
            filename.split('.',1)[0],
            filename.split('.')[-1]
        )
        output_file_path = f'{output_path}/{output_file}'
        task = io.download_file(access_token=at.access_token, dlb_url=output_url, file_path=output_file_path)
        loop.run_until_complete(task)
        
        os.remove(file_path)
        os.remove(ffmpeg_path)

        return json.dumps({'filename': output_file})
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
