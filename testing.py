from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chrome Dino Game</title>
        <style type="text/css">
            iframe { position: absolute; width: 100%; height: 100%; z-index: 999; }
            body { margin: 0; overflow: hidden; }
        </style>
    </head>
    <body>
        <iframe src="https://chromedino.com/" frameborder="0" scrolling="no" width="100%" height="100%" loading="lazy"></iframe>
    </body>
    </html>
    '''
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)