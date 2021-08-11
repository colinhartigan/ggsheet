import os
from PIL import Image, ImageFont, ImageDraw

class Builder:

    team_red_name = None
    team_blue_name = None

    cur_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    base_image = os.path.join(cur_path,"data/ggsheetreal.png")

    fonts = {
        "ddin": {
            "mvp_agent": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 28),
            "player_agent": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 16),
            "map_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Regular.ttf"), 20),
            "map_text": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 30),
            "win_loss_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 25),
            "player_stat_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Regular.ttf"), 14),
        },
        "tungsten": {
            "mvp_player": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 90),
            "mvp_stats": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 65),
            "mvp_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 40),
            "header_scores": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 165),
            "header_team_name": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 120),
            "player_name": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 45),
            "player_stats": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 43),
        }
    }

    other_side_offsets = {
        "mvps": {
            "text": 1116,
            "images": 368,
            "overrides": {
                "kd": 1127,
                "kills": 1127,
                "combat_score": 1132,
                "mvp_gradient": 335,
                "mvp_label": 107,
            }
        },
        "players": {
            "text": 212,
            "images": 212,
            "team": 239,
        }
    }

    def __init__(self, game_data):
        self.game_data = game_data
        self.img = Image.open(Builder.base_image)
        self.draw = ImageDraw.Draw(self.img)
        self.image_ref_points = {
            "header": {
                "text": {
                    "map_label": {
                        "anchor": (47,215),
                        "dimensions": (64,14), 
                        "color": (255,255,255),
                        "font": Builder.fonts["ddin"]["map_label"],
                        "text": "MAP",
                        "upper": True,
                    },
                    "map_name": {
                        "anchor": (46,236),
                        "dimensions": (164,21), 
                        "color": (255,255,255),
                        "font": Builder.fonts["ddin"]["map_text"],
                        "var_name": lambda *x: self.game_data["match_map_display_name"],
                        "upper": True,
                    }
                },
                "images": {
                    "map": {
                        "anchor": (32,32),
                        "dimensions": (240,240),
                        "file_path": "data/maps/map_{map}.png", 
                    },
                    "event_image": {
                        "anchor": (1648,32),
                        "dimensions": (240,240),
                        "file_path": "data/misc_assets/event_img.png", 
                    }
                }
            },
            "team_details": {
                "text": { 
                    "team_red_score": {
                        "anchor": (724,90),
                        "dimensions": (81,106),
                        "color": (255,70,85),
                        "font": Builder.fonts["tungsten"]["header_scores"],
                        "var_name": lambda *x: self.game_data["teams"][x[0]]["rounds_won"],
                        "justify": "r"
                    },
                    "team_blue_score": {
                        "anchor": (1114,90),
                        "dimensions": (81,106),
                        "color": (13,180,150),
                        "font": Builder.fonts["tungsten"]["header_scores"],
                        "var_name": lambda *x: self.game_data["teams"][x[0]]["rounds_won"],
                        "justify": "l"
                    },
                    "team_red_name": {
                        "anchor": (271,98),
                        "dimensions": (350,92),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["header_team_name"],
                        "var_name": lambda *x: Builder.team_red_name if Builder.team_red_name is not None else self.game_data["teams"][x[0]]["team_alias"],
                        "upper": True,
                        "justify": "r"
                    },
                    "team_blue_name": {
                        "anchor": (1330,98),
                        "dimensions": (350,92),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["header_team_name"],
                        "var_name": lambda *x: Builder.team_blue_name if Builder.team_blue_name is not None else self.game_data["teams"][x[0]]["team_alias"],
                        "upper": True,
                        "justify": "l"
                    },
                    "team_red_wl": {
                        "anchor": (542,80),
                        "dimensions": (80,20),
                        "color": (153,42,51),
                        "font": Builder.fonts["ddin"]["win_loss_label"],
                        "var_name": lambda *x: self.game_data["teams"][x[0]]["won"],
                        "upper": True,
                        "justify": "r"
                    },
                    "team_blue_wl": {
                        "anchor": (1331,80),
                        "dimensions": (80,20),
                        "color": (24,93,88),
                        "font": Builder.fonts["ddin"]["win_loss_label"],
                        "var_name": lambda *x: self.game_data["teams"][x[0]]["won"],
                        "upper": True,
                        "justify": "l"
                    },
                },
                "images": {
                    
                }
            },
            "mvps": {
                "text": {
                    "agent_name": {
                        "anchor": (255,401),
                        "dimensions": (296, 33), 
                        "color": (139,150,154),
                        "font": Builder.fonts["ddin"]["mvp_agent"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["agent_display_name"],
                        "upper": True,
                        "justify": "c"
                    },
                    "player_name": {
                        "anchor": (180,432),
                        "dimensions": (443,63),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["mvp_player"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["display_name"],
                        "upper": True,
                        "justify": "c"
                    },
                    "kd":{
                        "anchor": (149,570),
                        "dimensions": (126,48),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["mvp_stats"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["kd"],
                        "justify": "c"
                    },
                    "combat_score": {
                        "anchor": (330,570),
                        "dimensions": (126,48),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["mvp_stats"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["combat_score"],
                        "justify": "c"
                    },
                    "kills": {
                        "anchor": (518,570),
                        "dimensions": (126,48),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["mvp_stats"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["kills"],
                        "justify": "c"
                    },
                    "mvp_label": {
                        "anchor": (870,628),
                        "dimensions": (72,41),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["mvp_label"],
                        "text": "MVP",
                        "justify": "c"
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
            "players": {
                "text": {
                    "agent_name": {
                        "anchor": (102,697),
                        "dimensions": (204, 20), 
                        "color": (139,150,154),
                        "font": Builder.fonts["ddin"]["player_agent"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["agent_display_name"],
                        "upper": True,
                        "justify": "c"
                    },
                    "player_name": {
                        "anchor": (102,710),
                        "dimensions": (204, 50), 
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["player_name"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["display_name"] if len(self.game_data["players"][int(x[0])][int(x[1])]["display_name"]) < 12 else self.game_data["players"][int(x[0])][int(x[1])]["display_name"][:10]+"...",
                        "upper": True,
                        "justify": "c"
                    },
                    "combatscore_label": {
                        "anchor": (117,943),
                        "dimensions": (174, 26), 
                        "color": (138,148,156),
                        "font": Builder.fonts["ddin"]["player_stat_label"],
                        "text": "combat score",
                        "upper": True,
                        "justify": "l"
                    },
                    "kd_label": {
                        "anchor": (117,943),
                        "dimensions": (174, 26), 
                        "color": (138,148,156),
                        "font": Builder.fonts["ddin"]["player_stat_label"],
                        "text": "KD",
                        "upper": True,
                        "justify": "r"
                    },
                    "combat_score": {
                        "anchor": (117,895),
                        "dimensions": (174, 60), 
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["player_stats"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["combat_score"],
                        "justify": "l"
                    },
                    "kd": {
                        "anchor": (117,895),
                        "dimensions": (174, 60), 
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["player_stats"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["kd"],
                        "justify": "r"
                    },
                },
                "images": {
                    "agent": {
                        "anchor": (57,748),
                        "dimensions": (294,230), 
                        "target_width": 204,
                        "filename": "agent_{agent}.png"
                    },
                    "player_gradient": {
                        "anchor": (102,868),
                        "dimensions": (204,111), 
                        "filename": "player_gradient.png"
                    }
                },
            }
        }


    def draw_team_details(self):
        refs = self.image_ref_points["team_details"]
        #for img_type, image in refs["images"].items():

        for team_id,team in enumerate(self.game_data["teams"]):
            team_name = team["team_name"].lower()

            # draw scores
            score_label = refs["text"][f"team_{team_name}_score"]
            self.__draw_text(score_label,int(team_id))

            team_name_label = refs["text"][f"team_{team_name}_name"]
            self.__draw_text(team_name_label,int(team_id))

            team_wl_label = refs["text"][f"team_{team_name}_wl"]
            self.__draw_text(team_wl_label,int(team_id))


    def draw_header(self):
        refs = self.image_ref_points["header"]
        for img_type, image in refs["images"].items():
            new_img = Image.open(os.path.join(Builder.cur_path,*image["file_path"].format(map=self.game_data['match_map_display_name'].lower()).split("/"))).convert("RGBA")
            width, height = new_img.size
            ratio = width/height
            new_height = image["dimensions"][1]
            new_width = int(ratio * new_height)
            new_img = new_img.resize((new_width,new_height),Image.ANTIALIAS)

            if img_type == "map":
                diff = (426-240)    
                crop_bounds = (diff//2, 0, diff//2 + 240, 240)
                new_img = new_img.crop(crop_bounds)

            self.img.paste(new_img, image["anchor"], new_img)


        for label_type,label in refs["text"].items():
            self.__draw_text(label)

    def draw_players(self):
        player_refs = self.image_ref_points["players"]
        mvp_refs = self.image_ref_points["mvps"]
        for team_id,team in enumerate(self.game_data["players"]):
            # player panels
            if team_id != 0:
                # team offset (players)
                offset = Builder.other_side_offsets["players"]["team"]
                
                for ref,data in player_refs["text"].items():
                    data["anchor"] = (data["anchor"][0]+offset,data["anchor"][1])
                for ref,data in player_refs["images"].items():
                    data["anchor"] = (data["anchor"][0]+offset,data["anchor"][1])

                # team offset (mvps)
                text_offset = Builder.other_side_offsets["mvps"]["text"]
                image_offset = Builder.other_side_offsets["mvps"]["images"]
                for ref,data in mvp_refs["text"].items():
                    if Builder.other_side_offsets["mvps"]["overrides"].get(ref):
                        data["anchor"] = (data["anchor"][0]+Builder.other_side_offsets["mvps"]["overrides"][ref],data["anchor"][1])
                    else:
                        data["anchor"] = (data["anchor"][0]+text_offset,data["anchor"][1])
                for ref,data in mvp_refs["images"].items():
                    if Builder.other_side_offsets["mvps"]["overrides"].get(ref):
                        data["anchor"] = (data["anchor"][0]+Builder.other_side_offsets["mvps"]["overrides"][ref],data["anchor"][1])
                    else:
                        data["anchor"] = (data["anchor"][0]+image_offset,data["anchor"][1])


            for position,player in enumerate(team):

                if position == 0:
                    # mvp player

                    # load images
                    for img_type,image in mvp_refs["images"].items():
                        new_img = None
                        if img_type == "agent": 
                            new_img = Image.open(os.path.join(Builder.cur_path,*f"data/agents/{image['filename'].format(agent=player['agent_display_name'])}".split("/"))).convert("RGBA")
                        elif img_type == "mvp_gradient":
                            new_img = Image.open(os.path.join(Builder.cur_path,*f"data/misc_assets/{image['filename'].format(side=team_id)}".split("/"))).convert("RGBA")


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
                                offset = 6
                                alpha = new_img.getchannel('A')
                                silhouette = Image.new('RGBA', new_img.size, color=(255,70,85,255) if team_id == 0 else (13,180,150,255))
                                silhouette.putalpha(alpha) 

                                if team_id == 0:
                                    crop_bounds = (0,0,image["dimensions"][0]*(2/3),image["dimensions"][1])
                                    silhouette = silhouette.crop(crop_bounds)
                                    self.img.paste(silhouette,(image["anchor"][0]-offset,image["anchor"][1]),silhouette)
                                else:
                                    crop_bounds = (image["dimensions"][0]*(1/3),0,image["dimensions"][0],image["dimensions"][1])
                                    silhouette = silhouette.crop(crop_bounds)
                                    self.img.paste(silhouette,(int(image["anchor"][0]+image["dimensions"][0]*(1/3))+offset,image["anchor"][1]),silhouette)

                            self.img.paste(new_img,image["anchor"],new_img)
                            

                    # load text
                    for label_type,label in mvp_refs["text"].items():
                        self.__draw_text(label,int(team_id),int(position))

                else:
                    # regular player 
                    if position > 1:
                        # player offset
                        text_offset = Builder.other_side_offsets["players"]["text"]
                        image_offset = Builder.other_side_offsets["players"]["images"]
                        
                        for ref,data in player_refs["text"].items():
                            data["anchor"] = (data["anchor"][0]+text_offset,data["anchor"][1])
                        for ref,data in player_refs["images"].items():
                            data["anchor"] = (data["anchor"][0]+image_offset,data["anchor"][1])

                    
                    for img_type,image in player_refs["images"].items():
                        new_img = None
                        if img_type == "agent": 
                            new_img = Image.open(os.path.join(Builder.cur_path,*f"data/agents/{image['filename'].format(agent=player['agent_display_name'])}".split("/"))).convert("RGBA")
                        elif img_type == "player_gradient":
                            new_img = Image.open(os.path.join(Builder.cur_path,*f"data/misc_assets/{image['filename']}".split("/"))).convert("RGBA")

                        if new_img is not None:
                            width, height = new_img.size
                            ratio = height/width
                            new_width = image["dimensions"][0]
                            new_height = int(ratio * new_width)
                            new_img = new_img.resize((new_width,new_height),Image.ANTIALIAS)

                            if image.get("target_width"):
                                crop_bounds = (abs(57-(image["target_width"]//2)),0,57+(new_width-(image["target_width"]//2)),image["dimensions"][1])
                                new_img = new_img.crop(crop_bounds)
                                self.img.paste(new_img,(image["anchor"][0]+45,image["anchor"][1]),new_img)
                            
                            else:
                                crop_bounds = (0,0,image["anchor"][0]+image["dimensions"][0],image["dimensions"][1])
                                new_img = new_img.crop(crop_bounds)
                                self.img.paste(new_img,image["anchor"],new_img)

                            
                         
                


                    for label_type,label in player_refs["text"].items():
                        self.__draw_text(label,int(team_id),int(position))



    def build_image(self):
        

        self.draw_header()
        self.draw_team_details()
        self.draw_players()


        self.img.save("output.png")


    def __draw_text(self,label,*var):
        if label.get("justify"):
            justify = label["justify"]
        else:
            justify = "l"

        if label.get("var_name"):
            text = str(label["var_name"](*var))
        else:
            text = label["text"]
        text = text.upper() if label.get("upper") else text

        coords = label["anchor"]

        w,h = label["font"].getsize(text)
        dimens = label["dimensions"]
        anchor = label["anchor"]

        if justify == "c":
            coords = (((dimens[0]-w)/2)+anchor[0],(((dimens[1]-h)/2)+anchor[1]))
        elif justify == "r":
            coords = ((dimens[0]-w)+anchor[0],(((dimens[1]-h)/2)+anchor[1]))
        elif justify == "l":
            coords = (anchor[0],(((dimens[1]-h)/2)+anchor[1]))


        self.draw.text(coords, text, label["color"], font=label["font"])