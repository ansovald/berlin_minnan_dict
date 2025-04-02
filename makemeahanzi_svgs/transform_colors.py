# read in the SVG file, change the colors, and save it as '{name}_c.svg'

import shutil
import re

INITIAL_FILL = '#00000000'
FILL_COLOR = '#e6e5e6'

def get_codepoints(characters):
    codepoints = {}
    for char in characters:
        codepoints[char] = ord(char)
    return codepoints

def copy_svgs(codepoints):
    file_list = []
    for char in codepoints:
        print(f"Copying SVG for codepoint: {codepoints[char]}")
        file_name = f"svgs_c/{char}.svg"
        shutil.copy(f"svgs/{codepoints[char]}.svg", file_name)
        file_list.append(file_name)
    return file_list

def clean_svg(file):
    with open(file, 'r') as f:
        svg = f.read()
    # find the first group, beginning with `<g stroke="lightgray"`, ending with `</g>`, and remove it
    start = svg.find('<g stroke="lightgray"')
    end = svg.find('</g>', start) + 5
    svg = svg[:start] + svg[end:]
    # Save the cleaned SVG
    with open(file, 'w') as f:
        f.write(svg)

def replace_colors(file):
    with open(file, 'r') as f:
        svg = f.read()
    # Replace "stroke: blue;" and "stroke: black;" with "stroke: {FILL_COLOR};"
    for color in ['blue', 'black']:
        svg = svg.replace(f'stroke: {color};', f'stroke: {FILL_COLOR};')
    # Replace "fill="lightgray"" with "fill="{INITIAL_FILL}"
    svg = svg.replace('fill="lightgray"', f'fill="{INITIAL_FILL}"')
    # Save the SVG
    with open(file, 'w') as f:
        f.write(svg)

def resize_svg(file, width=24, height=24):
    with open(file, 'r') as f:
        svg = f.read()
    # Replace the width and height with the new values, if they exist. Otherwise, add them to the <svg> tag
    if 'height' in svg:
        svg = re.sub(r'height="[0-9]+"', f'height="{height}"', svg)
    else:
        svg = re.sub(r'<svg', f'<svg height="{height}"', svg)
    if 'width' in svg:
        svg = re.sub(r'width="[0-9]+"', f'width="{width}"', svg)
    else:
        svg = re.sub(r'<svg', f'<svg width="{width}"', svg)
    with open(file, 'w') as f:
        f.write(svg)


def combine_svgs(chars):
    svgs = []
    for char in chars:
        with open(f"svgs_c/{char}.svg", 'r') as f:
            print(f"Reading SVG for {char}")
            svgs.append(f.read())

    combined = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {len(chars)*1024} 1024">\n'

    replace_numbers = {
        'keyframes': 0,
        '#make-me-a-hanzi-animation-': 0,
        'make-me-a-hanzi-clip-': 0
    }

    # keyframe_number = 0
    # animation_number = 0
    # clip_number = 0
    for i, svg in enumerate(svgs):
        combined += f'<g transform="translate({i*1024} 0)">\n'

        for key in replace_numbers:
            keys = re.findall(rf'{key}[0-9]+', svg)
            keys = list(set(keys))
            keys.sort()
            key_dict = {}
            for k in keys:
                key_dict[k] = f'{key}{replace_numbers[key]}'
                replace_numbers[key] += 1
            print(f"{key}s: {key_dict}")
            for k in key_dict:
                svg = svg.replace(k, key_dict[k])
        combined += svg
        combined += '</g>\n'
    combined += '</svg>'
    with open(f"svgs_c/{chars}.svg", 'w') as f:
        f.write(combined)

if __name__ == '__main__':
    characters = '搜尋辭典'
    cp = get_codepoints(characters)
    svg_files = copy_svgs(cp)
    for f in svg_files:
        clean_svg(f)
        replace_colors(f)
        resize_svg(f)
    # combine_svgs(characters)