from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import serial

app = Flask(__name__)
app.config.from_object(__name__)
ser = serial.Serial('/dev/ttyACM1', 9600)

@app.route('/')
def index_page():
    return render_template('index.html', title='Pick To Part')

@app.route('/ptp', methods=['GET','POST'])
def ptp():
    coordinates = {
        'LOC1001': '0,0',
        'LOC1005': '0,1',
        'LOC1009': '0.2',
        'LOC10013':'0.3',
        'LOC1003': '1,1',
        'LOC1007': '2,2',
        'LOC1011': '5,3',
        'LOC10015':'7,7'
    }
    pn = request.args.get('part')
    ser.write(coordinates[pn])
    return '1'

@app.route('/off', methods=['GET','POST'])
def off():
    ser.write('z')
    return '1'

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Shutting down...'

if __name__ == '__main__':
    app.run(port=5001)
