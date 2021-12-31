from pathlib import Path
from datetime import datetime
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
from geoalert_unify.data_read import get_rgb

app = Flask(__name__)
upload_path = Path(__file__).parent.joinpath('uploads')
results_path = Path(__file__).parent.joinpath('results')
app.config['UPLOAD_DIRECTORY'] = upload_path
app.config['RESULTS_DIRECTORY'] = results_path
ALLOWED_EXTENIONS = {'.jp2', '.tiff', '.tif'}

@app.route('/get_rgb/', methods=['GET','POST'])
def return_rgb():
	if len(request.files.keys()) != 3:
		return f'3 files must be sumitted (b1, b2, b3), {len(request.files.keys())} were submitted.'
	
	b1 = request.files['b1']
	b2 = request.files['b2']
	b3 = request.files['b3']
	
	imgs = [b1, b2, b3]


	for i in request.files.values():
		ext = Path(str(i.filename)).suffix
		if ext not in ALLOWED_EXTENIONS:
			return f'unknown extension {ext}'
	
	for img in imgs:
		img.save(app.config['UPLOAD_DIRECTORY'].joinpath(secure_filename(img.filename)))
	
	img_pathes = []
	for img in imgs:
		img_path = str(Path(app.config['UPLOAD_DIRECTORY']).joinpath(img.filename))
		img_pathes.append(img_path)

	dt, dt_str = datetime.utcnow(), ''
	for i in dt.timetuple():
		dt_str += str(i)+'_'
	dt_str = dt_str[:-4]	

	get_rgb(img_pathes[0],img_pathes[1],img_pathes[2],str(app.config['RESULTS_DIRECTORY']),f'/output_{dt_str}')
	send_from_directory(app.config['RESULTS_DIRECTORY'], f'output_{dt_str}.tif')
	return 'done !'	

if __name__ == '__main__':
    app.run(debug = True)
