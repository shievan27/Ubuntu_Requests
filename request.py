import requests
import os
from urllib.parse import urlparse


def fetch_image(url):
    try:
        # Send HEAD request first to check headers
        head_response=requests.head(url, timeout=30, allow_redirects=True)
        head_response.raise_for_status()

        #check the header content-type
        content_type = head_response.headers.get('Content-type', '')
        if content_type.startswith("/image"):
            print(f"skipping (not an image):(url)")
            return
        
        # create directory if it doesn't exists
        os.makedirs("Fetched_Images", exist_ok=True)

        #extract file name from the url

        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"

        filepath = os.path.join("Fetched_Images", filename)

        # prevent duplicate downloads
        if os.path.exists(filepath):
            print(f"skipping duplicate: {filename}")
            return
        
         # fetch actual image
        response = requests.get(url, timeout= 15, stream= True)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

            print(f"succesfully fetched: {filename}")
            print(f"image saved to {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"connectio error: {e}")
    except Exception as e:
        print(f"error occured: {e}")
            



def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    urls = input("Please enter one or more image URLs (separated by spaces): ").split()
    
    for url in urls:
        fetch_image(url)
    
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()