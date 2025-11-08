import os
from urllib.parse import urlparse as urlParse


LORA_PATH = "/root/working/ComfyUI/models/loras"
CLIP_PATH = "/root/working/ComfyUI/models/clip"
VAE_PATH = "/root/working/ComfyUI/models/vae"
UNET_PATH = "/root/working/ComfyUI/models/unet"
SD_PATH = "/root/working/ComfyUI/models/sd"


def get_model_paths():
    return {
        "lora": LORA_PATH,
        "clip": CLIP_PATH,
        "vae": VAE_PATH,
        "unet": UNET_PATH,
        "sd": SD_PATH,
    }

def get_hf_token():
    with open("hf_token.txt", "r") as f:
        return f.read().strip()

def get_file_name(url):
    parsed_url = urlParse(url)
    return os.path.basename(parsed_url.path)


def run_installer():
    with open("index.json", "r") as f:
        import json

        data = json.load(f)

        for model in data:
            model_type = model["destination"]
            model_url = model["model"]
            model_platform = model.get("platform")
            file_name = get_file_name(model_url)
            model_path = os.path.join(get_model_paths()[model_type], file_name)

            if not os.path.exists(model_path):
                if model_platform == "huggingface":
                    # Construct the wget command and run it
                    wget_command = "wget --quiet --show-progress"
                    wget_command += f' --header="Authorization: Bearer {get_hf_token()}"'
                    wget_command += " --content-disposition"
                    # Use -O to save directly to the full file path (model_path)
                    wget_command += f' -O "{model_path}" "{model_url}"'
                    os.system(wget_command)
                elif model_platform == "civitai":
                    os.system(f'wget --quiet --show-progress -O "{model_path}" "{model_url}"')
                else:
                    print(f"Unknown platform for model: {model_url}")
                    
if __name__ == "__main__":
    run_installer()
