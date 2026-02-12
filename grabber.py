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
        
        # Search for the full URL first
        match = re.search(r'https://dist\d\.tvmi\.mt/.*?/master\.m3u8', response.text)
        if match:
            return match.group(0)
        
        # Plan B: Look for the token and build the URL
        token_match = re.search(r'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9\.[a-zA-Z0-9._-]+', response.text)
        if token_match:
            return f"https://dist7.tvmi.mt/{token_match.group(0)}/live/2/master.m3u8"
                
    except Exception as e:
        print(f"Error: {e}")
    return None

# 1. Grab the fresh link
final_link = get_tvm_live()

# 2. Add security headers for the IPTV player
# We add |Referer= and |User-Agent= to the end of the link
if final_link:
    headers_suffix = '|Referer=https://tvmi.mt/&User-Agent=Mozilla/5.0'
    final_link_with_headers = final_link + headers_suffix
else:
    final_link_with_headers = None

# 3. Create the final M3U file
with open("streams.m3u8", "w") as f:
    f.write("#EXTM3U\n")
    f.write('#EXTINF:-1 tvg-id="TVM.mt" tvg-name="TVM Malta" group-title="Malta", TVM Malta\n')
    
    if final_link_with_headers:
        # Standard VLC options
        f.write('#EXTVLCOPT:http-referrer=https://tvmi.mt/\n')
        f.write('#EXTVLCOPT:http-user-agent=Mozilla/5.0\n')
        # The actual link with headers for 9Xtream/TiviMate
        f.write(final_link_with_headers + "\n")
        print(f"Success! Generated link with headers.")
    else:
        f.write("# Error: Could not grab fresh link\n")
