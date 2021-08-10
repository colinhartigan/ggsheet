import os
from PIL import Image, ImageFont, ImageDraw

class Builder:

    cur_path = os.path.dirname(__file__)
    base_image = os.path.join(cur_path,"../data/ggsheetreal.png")

    fonts = {
        "ddin": {
            "mvp_agent": ImageFont.truetype(os.path.join(cur_path,"../data/fonts/DINNextLTPro-Regular.ttf"), 28),
        },
        "anton": {
            "mvp_player": ImageFont.truetype(os.path.join(cur_path,"../data/fonts/Anton-Regular.ttf"), 70),
            "mvp_stats": ImageFont.truetype(os.path.join(cur_path,"../data/fonts/Anton-Regular.ttf"), 50),
            "mvp_label": ImageFont.truetype(os.path.join(cur_path,"../data/fonts/Anton-Regular.ttf"), 30),
        }
    }

    image_ref_points = {
        "mvps": {
            "text": {
                "agent_name": {
                    "anchor": (255,401),
                    "dimensions": (296, 33), 
                    "color": (139,150,154),
                    "font": fonts["ddin"]["mvp_agent"],
                    "var_name": "agent_display_name",
                    "upper": True,
                },
                "player_name": {
                    "anchor": (180,425),
                    "dimensions": (443,63),
                    "color": (255,255,255),
                    "font": fonts["anton"]["mvp_player"],
                    "var_name": "display_name",
                    "upper": True,
                },
                "kd":{
                    "anchor": (149,565),
                    "dimensions": (126,48),
                    "color": (255,255,255),
                    "font": fonts["anton"]["mvp_stats"],
                    "var_name": "kd",
                },
                "combat_score": {
                    "anchor": (330,565),
                    "dimensions": (126,48),
                    "color": (255,255,255),
                    "font": fonts["anton"]["mvp_stats"],
                    "var_name": "combat_score",
                },
                "kills": {
                    "anchor": (518,565),
                    "dimensions": (126,48),
                    "color": (255,255,255),
                    "font": fonts["anton"]["mvp_stats"],
                    "var_name": "kills",
                },
                "mvp_label": {
                    "anchor": (832,625),
                    "dimensions": (110,41),
                    "color": (255,255,255),
                    "font": fonts["anton"]["mvp_label"],
                    "text": "MVP",
                }
            },
            "images": {
                "agent": {
                    "anchor": (610,365),
                    "dimensions": (332,305), 
                    "target_width": 400,
                    "filename": "agent_{agent}.png"
                },
                "mvp_gradient": {
                    "anchor": (642,629),
                    "dimensions": (300,41),
                    "filename": "mvp_gradient_{side}.png" 
                }
            }
        },
    }

    other_side_offsets = {
        "mvps": {
            "text": 1126,
            "images": 368,
            "overrides": {
                "combat_score": 1132,
                "mvp_gradient": 335,
                "mvp_label": 145,
            }
        }
    }

    def __init__(self, game_data):
        self.game_data = game_data

    def build_image(self):
        img = Image.open(Builder.base_image)
        draw = ImageDraw.Draw(img)

        for team_id,team in enumerate(self.game_data["players"]):
            for position,player in enumerate(team):

                if position == 0:
                    # mvp player

                    refs = Builder.image_ref_points["mvps"].copy()
                    if team_id != 0:
                        # if it's the other side apply the offset
                        text_offset = Builder.other_side_offsets["mvps"]["text"]
                        image_offset = Builder.other_side_offsets["mvps"]["images"]
                        for ref,data in refs["text"].items():
                            if ref in Builder.other_side_offsets["mvps"]["overrides"].keys():
                                data["anchor"] = (data["anchor"][0]+Builder.other_side_offsets["mvps"]["overrides"][ref],data["anchor"][1])
                            else:
                                data["anchor"] = (data["anchor"][0]+text_offset,data["anchor"][1])
                        for ref,data in refs["images"].items():
                            if ref in Builder.other_side_offsets["mvps"]["overrides"].keys():
                                data["anchor"] = (data["anchor"][0]+Builder.other_side_offsets["mvps"]["overrides"][ref],data["anchor"][1])
                            else:
                                data["anchor"] = (data["anchor"][0]+image_offset,data["anchor"][1])


                    # load images
                    for img_type,image in refs["images"].items():
                        new_img = None
                        if img_type == "agent": 
                            new_img = Image.open(os.path.join(Builder.cur_path,f"../data/agents/{image['filename'].format(agent=player['agent_display_name'])}")).convert("RGBA")
                        elif img_type == "mvp_gradient":
                            new_img = Image.open(os.path.join(Builder.cur_path,f"../data/{image['filename'].format(side=team_id)}")).convert("RGBA")


                        if new_img is not None:
                            if image.get("target_width"):
                                width, height = new_img.size
                                ratio = height/width
                                new_width = image["target_width"]
                                new_height = int(ratio * new_width)
                                new_img = new_img.resize((new_width,new_height),Image.ANTIALIAS)

                                if team_id == 0:
                                    crop_bounds = (0,0,image["dimensions"][0],image["dimensions"][1])
                                else:
                                    crop_bounds = (new_width-image["dimensions"][0],0,new_width,image["dimensions"][1])
                                new_img = new_img.crop(crop_bounds)

                            if img_type == "agent":
                                alpha = new_img.getchannel('A')
                                silhouette = Image.new('RGBA', new_img.size, color=(255,70,85,255) if team_id == 0 else (13,180,150,255))
                                silhouette.putalpha(alpha) 

                                if team_id == 0:
                                    img.paste(silhouette,(image["anchor"][0]-7,image["anchor"][1]),silhouette)
                                else:
                                    img.paste(silhouette,(image["anchor"][0]+7,image["anchor"][1]),silhouette)

                            img.paste(new_img,image["anchor"],new_img)
                            

                    # load text
                    for label_type,label in refs["text"].items():
                        if label.get("var_name"):
                            text = str(player[label["var_name"]])
                        else:
                            text = label["text"]

                        text = text.upper() if label.get("upper") else text
                        coords = self.__get_centered_coords(text,label["font"],label["anchor"],label["dimensions"])
                        draw.text(coords, text, label["color"], font=label["font"])

            #break



        img.save("test.png")


    def __get_centered_coords(self, text, font, anchor, dimens):
        w,h = font.getsize(text)
        return (((dimens[0]-w)/2)+anchor[0],((dimens[1]-h)/2)+anchor[1])