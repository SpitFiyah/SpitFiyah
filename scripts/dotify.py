import os
from PIL import Image

def image_to_dot_matrix_svg(image_path, output_svg_path, cols=100, dot_size=4, gap=2):
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    aspect = height / width
    rows = int(cols * aspect)
    
    img_resized = img.resize((cols, rows), Image.Resampling.LANCZOS)
    
    cell_total = dot_size + gap
    svg_width = cols * cell_total
    svg_height = rows * cell_total
    
    svg_elements = []
    svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_elements.append('<style>circle { transition: all 0.2s; }</style>')
    
    radius = dot_size / 2.0
    
    for y in range(rows):
        for x in range(cols):
            r, g, b, a = img_resized.getpixel((x, y))
            if a < 30:
                continue
            
            # Calculate brightness for dot size modulation if desired, or keep uniform grid with original color / matrix tint
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            
            # Use original RGB color or matrix green tint based on alpha/brightness
            if luminance > 0.05:
                # Add nice subtle glowing dot effect
                cx = x * cell_total + radius
                cy = y * cell_total + radius
                r_effective = radius * (0.3 + 0.7 * luminance)
                color_hex = f"#{r:02x}{g:02x}{b:02x}"
                svg_elements.append(f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_effective:.1f}" fill="{color_hex}" opacity="{a/255.0:.2f}" />')

    svg_elements.append('</svg>')
    
    os.makedirs(os.path.dirname(output_svg_path), exist_ok=True)
    with open(output_svg_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_elements))
    print(f"Generated SVG: {output_svg_path}")

if __name__ == '__main__':
    image_to_dot_matrix_svg('avatar.png', 'assets/portrait.svg', cols=90, dot_size=5, gap=2)
