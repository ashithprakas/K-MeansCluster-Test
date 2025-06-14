import re

class XYCoordinateExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.xy_values = []

    def extract_coordinates(self):
        try:
            with open(self.file_path, 'r') as file:
                text = file.read()

            pattern = r"^(.*?)\s*:\s*X\s*=\s*{([\d.]+),\s*Y\s*=\s*([\d.]+)}"
            matches = re.findall(pattern, text , re.MULTILINE)
            self.xy_values = [{"label": label.strip(), "x": float(x), "y": float(y)} for label, x, y in matches]
            print(f"Total coordinates extracted: {len(self.xy_values)}")
            return self.xy_values

        except FileNotFoundError:
            print(f"❌ Error: File not found at path: {self.file_path}")
            return []

            
            
