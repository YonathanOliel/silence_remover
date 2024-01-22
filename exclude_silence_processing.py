from wave_file_manager import*

SILENCES_THRESHOLD = 50
GLITCH_MAX_LEN = int(441 * 0.6)   # 6ms
SILENCES_MIN_LEN = 4410 * 4       # 400ms
MARGIN_START = 4410 * 1           # 100ms
MARGIN_END = 4410 * 1             # 100ms

def normalize_samples(samples, max_value):
    max_sample = max(abs(max(samples)), abs(min(samples)))
    f = (max_value / max_sample)
    return [s * f for s in samples]


def get_silences_points(samples, threshold, glitch_max_len, silence_min_len, margin_start, margin_end):
    points = []
    in_silences_zone = False
    chunk_count = 0
    chunk_len = 441
    start = 0

    if (MARGIN_START + MARGIN_END) > SILENCES_MIN_LEN:
        print("Error: MARGIN_START + MARGIN_END greater than SILENCES_MIN_LEN")
        return None
    
    for i in range(len(samples)):
        s = abs(samples[i])
        if not in_silences_zone:
            if s <= threshold:
                if chunk_count == 0:
                    start = i
                chunk_count += 1
                if chunk_count >= chunk_len:
                    in_silences_zone = True
            else:
                chunk_count = 0
        else:
            if s > threshold:
                chunk_count = 0
                in_silences_zone = False
                if len(points) > 0 and start - points[-1][1] <= glitch_max_len:
                    points[-1] = (points[-1][0], i)
                else:
                    points.append((start, i))
        
    points = [(p[0] + margin_start, p[1] - margin_end) for p in points if p[1] - p[0] >= silence_min_len] # filterd points

    return points


def get_amples_without_silences(samples, silences_points):
    out_samples = []
    start = 0

    for p in silences_points:
        if p[0] > start:
            out_samples += samples[start: p[0]]
            start = p[1]
    
    if start < len(samples) - 1:
        out_samples += samples[start:]

    return out_samples



