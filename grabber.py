import requests
import re

# This is the "User-Agent" that tricks the site into thinking we are a browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get_tvm_link():
    try:
        # Visit the live page
        response = requests.get("https://tvmi.mt/live/2", headers=headers, timeout=10)
        # Search for the .m3u8 link in the page source
        match = re.search(r'https://[a-zA-Z0-9.-]+/.*?/master\.m3u8', response.text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Error grabbing link: {e}")
    return None

# Generate the M3U file
link = get_tvm_link()
with open("streams.m3u8", "w") as f:
    f.write("#EXTM3U\n")
    f.write('#EXTINF:-1 tvg-id="TVM.mt" tvg-name="TVM Malta" group-title="General", TVM Malta\n')
    if link:
        f.write(link + "\n")
    else:
        # Fallback message so you know it failed
        f.write("# Error: Could not grab fresh link\n")

print("Grabber finished.")
