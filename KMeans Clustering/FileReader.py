import re
import numpy as np

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
                in_name_map = False
                for line in file:
                    line = line.strip()
                    
                    # Check for section markers
                    if line == '*NAME_MAP':
                        in_name_map = True
                        continue
                    elif line == '*PORTS':
                        in_name_map = False
                        continue
                    
                    # Only process lines within the name map section
                    if in_name_map and re.match(r'^\*\d+', line):
                        parts = line.split()
                        if len(parts) >= 2:
                            numeric_id = parts[0]  # e.g., *8688
                            # Join the rest of the parts to get the full label and unescape brackets
                            label = ' '.join(parts[1:])  # e.g., Data_Memory_inst_memory_reg\[3\]\[28\]
                            # Replace escaped brackets with regular brackets
                            label = label.replace('\\[', '[').replace('\\]', ']')
                            self.label_to_id[label] = numeric_id
        except FileNotFoundError:
            print(f"❌ Error: Capacitance file not found at path: {self.cap_file}")

    def extract_capacitances(self):
        """Extract capacitance values for each numeric ID"""
        try:
            with open(self.cap_file, 'r') as file:
                in_cap_section = False

                for line in file:
                    line = line.strip()

                    if line.startswith('*D_NET') or line.startswith('*RES') or line.startswith('*END') or line.startswith('*CONN'):
                        in_cap_section = False
                    elif line.startswith('*CAP'):
                        in_cap_section = True
                        continue

                    if in_cap_section and line:
                        parts = line.split()
                        # Skip if we don't have enough parts
                        if len(parts) < 3:
                            continue

                        try:
                            # The format can be either:
                            # "1378 *9570:CK 3.67885e-05" or
                            # "*9570:Q 3.68013e-05"
                            # So we need to check if the first part is a number
                            if parts[0].isdigit():
                                # Skip the number and use the next parts
                                node = parts[1]
                                cap = np.float64(parts[2])
                            else:
                                # No number at start, use first two parts
                                node = parts[0]
                                cap = np.float64(parts[1])

                            # Only store if the node has a CK suffix
                            if node.startswith('*') and node.endswith(':CK'):
                                # Extract just the numeric ID part (e.g., *9570 from *9570:CK)
                                numeric_id = node.split(':')[0]
                                self.capacitances[numeric_id] = cap

                        except (ValueError, IndexError):
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

            
            
