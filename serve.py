from flask import Flask, render_template, request
import sys
import logging
sys.path.append("..")
import run_generation
app = Flask(__name__, template_folder='./', static_folder='./build')

genny = run_generation.Genny('../../language-modeling/genout/')
for handler in app.logger.handlers:
   app.logger.removeHandler(handler)
handler = logging.FileHandler('./app.log')
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
   args = request.args
   #print(args)
   #licen = '\/\/ The MIT License\n\/\/ Copyright \u00A9 2013 Inigo Quilez\n\/\/ Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and\/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
   #show_code = licen + '\nvoid main() {\n    // Normalized pixel coordinates (from 0 to 1)\n    vec2 uv = gl_FragCoord.xy/iResolution.xy;\n    // Time varying pixel color\n    vec3 col = 0.5 + 0.5*cos(iTime+uv.xyx+vec3(0,2,4));'#\n\n    gl_FragColor = vec4(color,1.0);\n}'
   show_code = '\/\/ Basic Raymarching example by pwhiddy (http:\/\/transdimensional.xyz)\n\/\/ License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License\n\n\/\/ Fist add color to the scene'
   generated = ''
   if 'code' in args:
      show_code = args['code']
      app.logger.info('Called with code: ' + args['code'])
      prepped = show_code.replace('void main () {', 'void mainImage( out vec4 fragColor, in vec2 fragCoord )\n{')
      prepped = prepped.replace('gl_FragCoord', 'fragCoord')
      prepped = prepped.replace('gl_FragColor', 'fragColor')
      generated = genny.main(prepped)[0]
      generated = generated.replace('void mainImage( out vec4 fragColor, in vec2 fragCoord )\n{','void main () {')
      generated = generated.replace('fragCoord','gl_FragCoord')
      generated = generated.replace('fragColor', 'gl_FragColor')
      generated = generated.split('","')[0]
      if (len(generated) > 0 and generated[-1] == '\\'):
         generated = generated[:-1]
   return render_template('index.html', code=show_code+generated)

if __name__ == '__main__':
   app.run(debug = True)