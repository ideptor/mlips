
def filtering(trace_file_name: str, must_include_head: list):

    filtered_lines = []
    with open(trace_file_name, "r") as f:
        filtered_lines = []
        while True:
            line = f.readline()
            if not line: break
            for head in must_include_head:
                if head in line:
                    filtered_lines.append(line)
                    continue
    
    return filtered_lines
