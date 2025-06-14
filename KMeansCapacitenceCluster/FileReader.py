def extract_sink_capacitances(filename):
    sink_caps = {}
    current_net = None
    in_cap_section = False

    with open(filename, 'r') as file:
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
                    node = parts[1]
                    # Try to find the capacitance value by looking for a numeric value
                    cap_value = None
                    for part in parts[2:]:
                        try:
                            cap_value = float(part)
                            break
                        except ValueError:
                            continue
                    
                    if cap_value is not None and not node.startswith(current_net + ':'):
                        sink_caps[node] = cap_value

    return sink_caps

# Example usage:
sink_capacitances = extract_sink_capacitances('data.txt')

# Print result
for pin, cap in sink_capacitances.items():
    print(f"{pin}: {cap}")

