from playwright.sync_api import sync_playwright

class ImageRenderer:
    def render(self, html_content: str, output_path: str, width: int, height: int):
        print(f"Initializing renderer for output at {output_path}...")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            try:
                page.set_viewport_size({"width": width, "height": height})
                page.set_content(html_content, wait_until='networkidle')
                
                print("Capturing screenshot...")
                page.screenshot(path=output_path, type='png', full_page=False)
                
                print(f"Successfully rendered image to {output_path}")
            finally:
                browser.close()