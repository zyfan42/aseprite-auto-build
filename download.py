import requests
import os

ASEPRITE_REPOSITORY = "aseprite/aseprite"
SKIA_REPOSITORY = "aseprite/skia"
SKIA_RELEASE_FILE_NAME = "Skia-Windows-Release-x64.zip"
CHINESE_STRINGS_URL = "https://raw.githubusercontent.com/aseprite/strings/main/zh_Hans.ini"


def get_latest_tag_aseprite():
    response = requests.get(
        f"https://api.github.com/repos/{ASEPRITE_REPOSITORY}/releases"
    )
    response_json = response.json()

    for release in response_json:
        if "beta" not in release["tag_name"].lower():
            return release["tag_name"]

    return None


def save_aseprite_tag(tag):
    with open("version.txt", "w") as f:
        f.write(tag)


def clone_aseprite(tag):
    clone_url = f"https://github.com/{ASEPRITE_REPOSITORY}.git"
    git_cmd = f"git clone -b {tag} {clone_url} src/aseprite --depth 1"
    os.system(git_cmd)
    os.system("cd src/aseprite && git submodule update --init --recursive")


def get_latest_tag_skia():
    # response = requests.get(f'https://api.github.com/repos/{SKIA_REPOSITORY}/releases/latest')
    # response_json = response.json()
    # return response_json['tag_name']
    return "m124-08a5439a6b"


def download_skia_for_windows(tag):
    download_url = f"https://github.com/{SKIA_REPOSITORY}/releases/download/{tag}/{SKIA_RELEASE_FILE_NAME}"

    file_response = requests.get(download_url)
    file_response.raise_for_status()

    with open(f"src/{SKIA_RELEASE_FILE_NAME}", "wb") as f:
        f.write(file_response.content)

    os.system(f"7z x src/{SKIA_RELEASE_FILE_NAME} -osrc/skia")


def download_chinese_strings():
    print(f"Downloading Chinese strings from {CHINESE_STRINGS_URL}")
    response = requests.get(CHINESE_STRINGS_URL)
    response.raise_for_status()

    # Path relative to where this script is run (root of repo)
    # src/aseprite should be cloned by now
    output_path = "src/aseprite/data/strings/zh_Hans.ini"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    aseprite_tag = get_latest_tag_aseprite()
    clone_aseprite(aseprite_tag)
    save_aseprite_tag(aseprite_tag)

    download_chinese_strings()

    skia_tag = get_latest_tag_skia()
    download_skia_for_windows(skia_tag)
