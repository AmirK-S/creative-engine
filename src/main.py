import json
import os
from dotenv import load_dotenv
from stability_client import StabilityAIClient
from html_assembler import HTMLAssembler
from image_renderer import ImageRenderer

def main():
    load_dotenv()
    api_key = os.getenv("STABILITY_API_KEY")

    # --- 1. Charger les fichiers d'entrée ---
    with open('inputs/visual_prompt.json', 'r') as f:
        visual_prompt = json.load(f)
    with open('inputs/doc_design.json', 'r') as f:
        doc_design = json.load(f)

    # --- 2. Générer l'image de fond ---
    client = StabilityAIClient(api_key=api_key)
    # Extraire la partie pertinente du prompt pour l'image
    image_prompt = "Bright, sun-lit kitchen interior. A smiling woman in active-wear holds a vertical stack of three NutraGlow “GlowTonic” jars (top peach, middle teal, bottom lavender) centred at mid-torso, angled slightly toward camera. Camera: waist-up, eye-level, shallow depth for soft background blur; jars sharp and heroed."
    
    # Calculer les dimensions de l'image (60% de la largeur du canvas)
    canvas_width = int(doc_design['canvas']['resolution'].split('x'))
    canvas_height = int(doc_design['canvas']['resolution'].split('x')[1])
    image_width = int(canvas_width * 0.6)
    
    background_image_bytes = client.generate_image(
        prompt=image_prompt,
        negative_prompt="text, words, logos, blurry face",
        width=image_width,
        height=canvas_height
    )

    if not background_image_bytes:
        print("Failed to generate background image. Exiting.")
        return

    # --- 3. Assembler le document HTML ---
    assembler = HTMLAssembler()
    html_content = assembler.assemble(doc_design, background_image_bytes)
    
    # (Optionnel) Sauvegarder le HTML pour le débogage
    with open('output/debug.html', 'w') as f:
        f.write(html_content)

    # --- 4. Rendre l'image finale ---
    renderer = ImageRenderer()
    renderer.render(
        html_content=html_content,
        output_path='output/final_creative.png',
        width=canvas_width,
        height=canvas_height
    )

if __name__ == "__main__":
    main()