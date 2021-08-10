from src import valorant_manager
from src import image_builder

if __name__ == "__main__":
    mgr = valorant_manager.Valorant()
    data = mgr.load_match_data()

    builder = image_builder.Builder(data)
    builder.build_image()