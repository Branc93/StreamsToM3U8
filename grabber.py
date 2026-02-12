import requests
import re

def get_tvm_live():
    url = "https://tvmi.mt/live/2"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://tvmi.mt/'
    }

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        
        # Extract the m3u8 link
        match = re.search(r'https://dist\d\.tvmi\.mt/.*?/master\.m3u8', response.text)
        if match:
            return match.group(0)
        
        # Plan B: Build from token
        token_match = re.search(r'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9\.[a-zA-Z0-9._-]+', response.text)
        if token_match:
            return f"https://dist7.tvmi.mt/{token_match.group(0)}/live/2/master.m3u8"
                
    except Exception as e:
        print(f"Error: {e}")
    return None

link = get_tvm_live()

# Generate the M3U with bypass headers
with open("streams.m3u8", "w") as f:
    f.write("#EXTM3U\n")
    f.write('#EXTINF:-1 tvg-id="TVM.mt" tvg-name="TVM Malta" group-title="Malta", TVM Malta\n')
    
    if link:
        # 1. Header for VLC (using #EXTVLCOPT)
        f.write('#EXTVLCOPT:http-referrer=https://tvmi.mt/\n')
        f.write('#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\n')
        
        # 2. Header for 9Xtream/TiviMate (using pipe | format)
        # Note: No spaces around the pipe or equals signs
        headers_pipe = '|Referer=https://tvmi.mt/&User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        f.write(link + headers_pipe + "\n")
        print(f"Success! Generated link with bouncer bypass.")
    else:
        f.write("# Error: Could not grab fresh link\n")
