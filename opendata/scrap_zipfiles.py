import requests
import os

# Base URL of the site
base_url = "https://opendata.justice-administrative.fr"

# List of relative paths to the ZIP files as found in the HTML snippet
zip_paths = [
    "/DCE/2021/06/CE_202106.zip",
    "/DCE/2021/07/CE_202107.zip",
    "/DCE/2021/09/CE_202109.zip",
    "/DCE/2021/10/CE_202110.zip",
    "/DCE/2021/11/CE_202111.zip",
    "/DCE/2021/12/CE_202112.zip",
    "/DCE/2022/01/CE_202201.zip",
    "/DCE/2022/02/CE_202202.zip",
    "/DCE/2022/03/CE_202203.zip",
    "/DCE/2022/04/CE_202204.zip",
    "/DCE/2022/05/CE_202205.zip",
    "/DCE/2022/06/CE_202206.zip",
    "/DCE/2022/07/CE_202207.zip",
    "/DCE/2022/08/CE_202208.zip",
    "/DCE/2022/09/CE_202209.zip",
    "/DCE/2022/10/CE_202210.zip",
    "/DCE/2022/11/CE_202211.zip",
    "/DCE/2022/12/CE_202212.zip",
    "/DCE/2023/01/CE_202301.zip",
    "/DCE/2023/02/CE_202302.zip",
    "/DCE/2023/03/CE_202303.zip",
    "/DCE/2023/04/CE_202304.zip",
    "/DCE/2023/05/CE_202305.zip",
    "/DCE/2023/06/CE_202306.zip",
    "/DCE/2023/07/CE_202307.zip",
    "/DCE/2023/08/CE_202308.zip",
    "/DCE/2023/09/CE_202309.zip",
    "/DCE/2023/10/CE_202310.zip",
    "/DCE/2023/11/CE_202311.zip",
    "/DCE/2023/12/CE_202312.zip",
    "/DCE/2024/01/CE_202401.zip",
    "/DCE/2024/02/CE_202402.zip",
    "/DCE/2024/03/CE_202403.zip",
    "/DCE/2024/04/CE_202404.zip",
    "/DCE/2024/05/CE_202405.zip",
    "/DCE/2024/06/CE_202406.zip",
    "/DCE/2024/07/CE_202407.zip",
    "/DCE/2024/08/CE_202408.zip",
]

# Loop through each path, construct the full URL, and download the file
for path in zip_paths:
    full_url = base_url + path
    filename = os.path.basename(path)
    print(f"Downloading {filename}...")
    
    # Download the file
    response = requests.get(full_url, verify=False)
    
    # Save the file
    with open(filename, 'wb') as f:
        f.write(response.content)
    
    print(f"Finished downloading {filename}")

print("All files downloaded.")
