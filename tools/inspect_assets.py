import os
from PIL import Image

output_html = r"FACTORY_RESET-main\assets_preview.html"
thumb_dir = r"FACTORY_RESET-main\thumbs"
os.makedirs(thumb_dir, exist_ok=True)

html = ['''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { background: #18191c; color: #e0e0e0; font-family: monospace; padding: 20px; }
h2 { color: #4af; border-bottom: 2px solid #333; padding-bottom: 6px; margin-top: 30px; }
.grid { display: flex; flex-wrap: wrap; gap: 12px; }
.card { background: #22252a; border: 1px solid #3a3f48; border-radius: 6px; padding: 8px; width: 220px; text-align: center; }
.card img { max-width: 100%; height: auto; border-radius: 4px; border: 1px solid #111; }
.name { font-size: 11px; margin-top: 6px; word-break: break-all; color: #aaa; }
.dims { font-size: 10px; color: #ffaa33; }
</style>
</head>
<body>
<h1>FACTORY RESET - Asset Inspection Gallery</h1>
''']

categories = ['agent_new', 'Craft_new', 'day_back', 'Drone', 'Gun', 'monsters', 'night_back']

for cat in categories:
    folder = os.path.join(r"art (2)\art", cat)
    if not os.path.exists(folder):
        continue
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png'))]
    html.append(f'<h2>{cat} ({len(files)} items)</h2><div class="grid">')
    for idx, f in enumerate(files):
        p = os.path.join(folder, f)
        try:
            with Image.open(p) as im:
                w, h = im.size
                t_name = f"{cat}_{idx}.jpg"
                t_path = os.path.join(thumb_dir, t_name)
                im_copy = im.copy()
                im_copy.thumbnail((320, 200))
                im_copy.save(t_path, "JPEG", quality=75)
                html.append(f'''<div class="card">
                    <img src="thumbs/{t_name}">
                    <div class="name">{f}</div>
                    <div class="dims">{w}x{h}</div>
                </div>''')
        except Exception as e:
            print(f"Error reading {f}: {e}")
    html.append('</div>')

html.append('</body></html>')

with open(output_html, 'w', encoding='utf-8') as f_out:
    f_out.write('\n'.join(html))

print(f"Generated asset preview at {output_html}")
