import os
import re
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
   help="input HTML file name")
ap.add_argument("-o", "--output", required=False,
   help="[optional] output file name, if not set - 'embedded_' prefix will be added")
args = vars(ap.parse_args())

# scripts to be added in html header
preload_scripts = set()

# global encoding
encoding = 'utf-8'

def getIframeContent(src):
  if not os.path.isfile(src):
    raise Exception(f'Error: iframe file "{src}" not found')

  with open(src, 'r', encoding=encoding) as f:
    iframe = f.read()

  # cut iframe body/header if it is full
  start = iframe.find('<body>')
  end = iframe.find('</body>')
  if start != -1 and end != -1:
    iframe = iframe[start + 6 : end] # we don't need '<body>' tag

  # remove redundant scripts from iframes
  end = 0
  while True:
    start = iframe.find('<script', end)
    end = iframe.find('</script>', start + 7)
    if start == -1 or end == -1:
      break
    end += 9 # move `end` to the tag end

    # cut script references as we move them to html header
    script = iframe[start : end]
    if script.startswith('<script src="http'):
      preload_scripts.add(script)
      iframe = iframe.replace(script, '')
      continue

    # cut Plotly function definition and replace it by cdb reference
    if script.find('Plotly=t()') != -1:
      iframe = iframe.replace(script, '')
      preload_scripts.add('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>')
      break

  return iframe

input_file = args['input']
if not os.path.isfile(input_file):
  raise Exception(f'Error: {input_file} not exists')
if not input_file.endswith('.html'):
  raise Exception(f'Error: only HTML files are supported and {input_file} is not HTML')
with open(input_file, 'r', encoding=encoding) as f:
  template = f.read()

# handle if called not near `input_file`
directory = os.path.dirname(input_file)

iframe_end = 0
while True:
  iframe_start = template.find('<iframe', iframe_end + 9)
  iframe_end = template.find('</iframe>', iframe_start + 7)
  if iframe_start == -1 or iframe_end == -1:
    break

  iframe_end += 9 # catch '</iframe>'
  iframe = template[iframe_start : iframe_end]
  match = re.search(r'src="(.*?)"', iframe)
  if not match:
    continue
  content = getIframeContent(os.path.join(directory, match.group(1)))

  template = template.replace(iframe, content)

# add reference to Plotly script right before first script (usually in the header)
add_to_header = ''
for s in preload_scripts:
  add_to_header += s + '\n'
template = template.replace('<script', add_to_header + '<script', 1)


output_file_name = args['output'] if args['output'] else 'embedded_' + os.path.basename(args['input'])
with open(output_file_name, 'w', encoding=encoding) as f:
  f.write(template)
