import base64
from jinja2 import Environment, FileSystemLoader

class HTMLAssembler:
    def __init__(self, template_dir: str = 'src/templates'):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template('template.html.j2')

    def _encode_image_to_data_uri(self, image_bytes: bytes) -> str:
        b64_string = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:image/png;base64,{b64_string}"

    def assemble(self, design_spec: dict, background_image: bytes) -> str:
        # Convertir les coordonnées en % pour le CSS
        for zone in design_spec.get('zones',):
            bbox = zone.get('bbox', {})
            zone['css_style'] = {
                'top': f"{bbox.get('top_pct', 0)}%",
                'left': f"{bbox.get('left_pct', 0)}%",
                'width': f"{bbox.get('width_pct', 0)}%",
                'height': f"{bbox.get('height_pct', 0)}%",
                'z-index': zone.get('z_index', 1)
            }
            # Ajouter d'autres styles
            style_tokens = zone.get('style', {})
            if style_tokens.get('text_token') == 'brand/sun-gold':
                zone['css_style']['color'] = '#FFB300'
            elif style_tokens.get('text_token') == 'brand/white':
                 zone['css_style']['color'] = '#FFFFFF'
            #... ajouter d'autres mappages de tokens de couleur ici

        template_data = {
            'canvas': design_spec.get('canvas', {}),
            'zones': design_spec.get('zones',),
            'background_image_uri': self._encode_image_to_data_uri(background_image)
        }
        return self.template.render(template_data)