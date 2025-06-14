import re

class XYCoordinateExtractor:
    def __init__(self, coord_file, cap_file):
        self.coord_file = coord_file
        self.cap_file = cap_file
        self.xy_values = []
        self.capacitances = {}
        self.label_to_id = {}

    def extract_label_mapping(self):
        """Extract mapping between labels and their numeric IDs from capacitance file"""
        try:
            with open(self.cap_file, 'r') as file:
                for line in file:
                    if line.startswith('*I') or line.startswith('*P'):
                        parts = line.split()
                        if len(parts) >= 4:
                            numeric_id = parts[1]  # e.g., *10559
                            label = parts[2]      # e.g., IF_ID_Pipeline_PC_Out_reg[10]
                            self.label_to_id[label] = numeric_id
        except FileNotFoundError:
            print(f"❌ Error: Capacitance file not found at path: {self.cap_file}")

    def extract_capacitances(self):
        """Extract capacitance values for each numeric ID"""
        try:
            with open(self.cap_file, 'r') as file:
                current_net = None
                in_cap_section = False

                for line in file:
                    line = line.strip()

                    if line.startswith('*D_NET'):
                        parts = line.split()
                        current_net = parts[1]
                        in_cap_section = False

                    elif line.startswith('*CAP'):
                        in_cap_section = True

                    elif line.startswith('*RES') or line.startswith('*END'):
                        in_cap_section = False

                    elif in_cap_section and line:
                        parts = line.split()
                        if len(parts) >= 3:
                            try:
                                node = parts[1]
                                cap = float(parts[2])
                                # Store capacitance with the numeric ID (e.g., *10559)
                                if node.startswith('*'):
                                    self.capacitances[node] = cap
                                # Also store with the full node name (e.g., *10559:Q)
                                self.capacitances[node] = cap
                            except ValueError:
                                # Skip lines that don't have valid capacitance values
                                continue

        except FileNotFoundError:
            print(f"❌ Error: Capacitance file not found at path: {self.cap_file}")

    def extract_coordinates(self):
        """Extract coordinates and match with capacitance values"""
        try:
            # First get the label to ID mapping
            self.extract_label_mapping()
            
            # Then get the capacitance values
            self.extract_capacitances()
            
            # Now extract coordinates and match with capacitances
            with open(self.coord_file, 'r') as file:
                text = file.read()

            pattern = r"^(.*?)\s*:\s*X\s*=\s*{([\d.]+),\s*Y\s*=\s*([\d.]+)}"
            matches = re.findall(pattern, text, re.MULTILINE)
            
            for label, x, y in matches:
                label = label.strip()
                numeric_id = self.label_to_id.get(label)
                
                # Try to get capacitance using different possible keys
                capacitance = 0.0
                if numeric_id:
                    # Try with just the numeric ID
                    capacitance = self.capacitances.get(numeric_id, 0.0)
                    # If not found, try with common suffixes
                    if capacitance == 0.0:
                        for suffix in [':A', ':Q', ':Z', ':Y']:
                            full_id = f"{numeric_id}{suffix}"
                            if full_id in self.capacitances:
                                capacitance = self.capacitances[full_id]
                                break
                
                self.xy_values.append({
                    "label": label,
                    "x": float(x),
                    "y": float(y),
                    "numeric_id": numeric_id,
                    "capacitance": capacitance
                })
            
            print(f"Total coordinates extracted: {len(self.xy_values)}")
            return self.xy_values

        except FileNotFoundError:
            print(f"❌ Error: Coordinate file not found at path: {self.coord_file}")
            return []

            
            
