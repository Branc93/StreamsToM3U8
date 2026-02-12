import requests
import re
import json

def get_tvm_live():
    url = "https://tvmi.mt/live/2"
    # This identifies the robot as a modern browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://tvmi.mt/'
    }

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        
        # Look for the 'source' or 'file' inside the script tags
        # TVMi often hides the link in a JSON block called "props" or "state"
        match = re.search(r'https://dist\d\.tvmi\.mt/.*?/master\.m3u8', response.text)
        
        if match:
            return match.group(0)
        else:
            # Plan B: Try to find the token base and build it
            token_match = re.search(r'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9\.[a-zA-Z0-9._-]+', response.text)
            if token_match:
                return f"https://dist7.tvmi.mt/{token_match.group(0)}/live/2/master.m3u8"
                
    except Exception as e:
        print(f"Error: {e}")
    return None

# Create the file
final_link = get_tvm_live()

with open("streams.m3u8", "w") as f:
    f.write("#EXTM3U\n")
    f.write('#EXTINF:-1 tvg-id="TVM.mt" tvg-name="TVM Malta" group-title="General", TVM Malta\n')
    if final_link:
        f.write(final_link + "\n")
        print(f"Success! Found: {final_link}")
    else:
        f.write("# Error: Site blocked the robot. Use manual link.\n")
