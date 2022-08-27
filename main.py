import traceback
from InquirerPy import inquirer

from src import valorant_manager
from src import image_builder
from src.fetch_data import fetch_images, fetch_matches

def main():
    mgr = valorant_manager.Valorant()
    content = mgr.content

    fetch_images('agent')
    fetch_images('map')
    choices = fetch_matches(mgr, content)

    while True:
        match_id = inquirer.select("Pick a match:", choices).execute()
        if match_id == "custom":
            match_id = inquirer.text("Enter match id").execute()
        if match_id is not None and match_id != "":
            try:
                print("Generating image...")
                data = mgr.load_match_data(match_id)
                builder = image_builder.Builder(data)
                builder.build_image()
            except:
                traceback.print_exc()

if __name__ == "__main__":
    main()

    # builder = image_builder.Builder(data)
    # builder.build_image()
    # print("done")
