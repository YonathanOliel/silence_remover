import wave

WAV_FORMAT = 1               # mono
WAV_FORMAT_SAMPLE_WIDTH = 2  # 16bits
WAV_FORMAT_FRAMERATE = 44100 # hz

def get_16bits_sample_from_bytes(byte_ls, byte_ms):
    unsigned = byte_ls + (byte_ms * 256)
    signed = unsigned

    if unsigned > 32767:
        signed = unsigned - 65535
    return signed


def get_16bits_samples_from_bytes(bytes):
    samples = []
    for i in range(0, len(bytes) - 1, 2):
        sample = get_16bits_sample_from_bytes(bytes[i], bytes[i + 1])
        samples.append(sample)
    return samples


def get_bytes_sample_from_16bits_sample(sample_16bits):
    unsigned_16bits_sample = sample_16bits
    if sample_16bits < 0:
        unsigned_16bits_sample = sample_16bits + 65536
    byte_ms = unsigned_16bits_sample // 256
    byte_ls = unsigned_16bits_sample - (byte_ms * 256)
    return byte_ls, byte_ms


def get_bytes_samples_from_16bits_samples(samples_16bits):
    bytes = []
    for s in samples_16bits:
        ls, ms = get_bytes_sample_from_16bits_sample(s)
        bytes.append(ls)
        bytes.append(ms)
    return bytes


def wave_file_read_samples(file_name):
    wr = wave.open(file_name, mode = "rb")

    if wr.getnchannels() != WAV_FORMAT:
        print("Error: Use a mono file")
        return None
    
    if wr.getsampwidth() != WAV_FORMAT_SAMPLE_WIDTH:
        print("Error: Use a format 16 bits")
        return None

    if wr.getframerate() != WAV_FORMAT_FRAMERATE:
        print("Error: Use a format 16 bits")
        return None
        
    nframes = wr.getnframes()
    nframes_bytes = wr.readframes(nframes)

    sample_16bits = get_16bits_samples_from_bytes(nframes_bytes)
    wr.close()
    return sample_16bits

# samples -> 16bits
def wave_file_write_samples(file_name, samples):
    ww = wave.open(file_name, mode = "wb")

    ww.setnchannels(WAV_FORMAT)
    ww.setsampwidth(WAV_FORMAT_SAMPLE_WIDTH)
    ww.setframerate(WAV_FORMAT_FRAMERATE)
  
    ww.setnframes(len(samples))
    bytes = get_bytes_samples_from_16bits_samples(samples)
    ww.writeframesraw(bytearray(bytes)) 

    ww.close()