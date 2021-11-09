import os

from PIL import Image, ImageDraw, ImageFont


class Builder:

    cur_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    base_image = os.path.join(cur_path,"data/ggsheetreal.png")
    output_folder = os.path.join(cur_path,"output")

    fonts = {
        "ddin": {
            "mvp_agent": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 28),
            "player_agent": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 14),
            "map_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Regular.ttf"), 20),
            "map_text": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 30),
            "win_loss_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 25),
            "player_stat_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Regular.ttf"), 12),
            "timestamp": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Regular.ttf"), 22),
        },
        "tungsten": {
            "mvp_player": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 90),
            "mvp_stats": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 65),
            "mvp_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 35),
            "header_scores": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 165),
            "header_team_name": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 120),
            "player_name": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 40),
            "player_stats": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 42),
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
        },
    }

    def __init__(self, game_data):
        self.game_data = game_data
        self.img = Image.open(Builder.base_image)
        self.draw = ImageDraw.Draw(self.img)

        self.team_red_name = "DEF" #defenders
        self.team_blue_name = "ATK" #attackers

        self.image_ref_points = {
            "header_footer": {
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
                    },
                    "timestamp": {
                        "anchor": (1335,1045),
                        "dimensions": (575, 35), 
                        "color": (138,148,156),
                        "font": Builder.fonts["ddin"]["timestamp"],
                        "var_name": lambda *x: self.game_data["timestamp"],
                        "upper": True,
                        "justify": "r"
                    },
                    "credit": {
                        "anchor": (10,1045),
                        "dimensions": (575, 35), 
                        "color": (138,148,156),
                        "font": Builder.fonts["ddin"]["timestamp"],
                        "text": "github.com/colinhartigan/ggsheet",
                        "justify": "l",
                    }
                    # "mode_name": {
                    #     "anchor": (1679,236),
                    #     "dimensions": (164,21), 
                    #     "color": (255,255,255),
                    #     "font": Builder.fonts["ddin"]["map_text"],
                    #     "var_name": lambda *x: self.game_data["match_mode_display_name"],
                    #     "upper": True,
                    #     "justify": "l",
                    # },
                    # "mode_label": {
                    #     "anchor": (1679,215),
                    #     "dimensions": (64,14), 
                    #     "color": (255,255,255),
                    #     "font": Builder.fonts["ddin"]["map_label"],
                    #     "text": "MODE",
                    #     "upper": True,
                    #     "justify": "l",
                    # },
                },
                "images": {
                    "map": {
                        "anchor": (32,32),
                        "dimensions": (240,240),
                        "crop": lambda *x: ((426-240)//2, 0, (426-240)//2 + 240, 240),
                        "file_path": "data/maps/map_{map}.png", 
                    },
                    "mode": {
                        "anchor": (1648,32),
                        "dimensions": (240,240),
                        "target_width": 200,
                        "centered": True,
                        "file_path": "data/modes/mode_{mode}.png", 
                    },
                    # "event_img": {
                    #     "anchor": (1648,32),
                    #     "dimensions": (240,240),
                    #     "centered": True,
                    #     "file_path": "data/misc_assets/event_img.png", 
                    # }
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
                        "var_name": lambda *x: self.team_red_name if self.team_red_name is not None else self.game_data["teams"][x[0]]["team_alias"],
                        "upper": True,
                        "justify": "r"
                    },
                    "team_blue_name": {
                        "anchor": (1330,98),
                        "dimensions": (350,92),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["header_team_name"],
                        "var_name": lambda *x: self.team_blue_name if self.team_blue_name is not None else self.game_data["teams"][x[0]]["team_alias"],
                        "upper": True,
                        "justify": "l"
                    },
                    "team_red_wl": {
                        "anchor": (542,80),
                        "dimensions": (80,20),
                        "color": (255,70,85),
                        "alt_color": (153,42,51),
                        "font": Builder.fonts["ddin"]["win_loss_label"],
                        "var_name": lambda *x: self.game_data["teams"][x[0]]["won"],
                        "upper": True,
                        "justify": "r"
                    },
                    "team_blue_wl": {
                        "anchor": (1331,80),
                        "dimensions": (80,20),
                        "color": (13,180,150),
                        "alt_color": (24,93,88),
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
                        "anchor": (250,398),
                        "dimensions": (301, 33), 
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
                        "anchor": (149,565),
                        "dimensions": (126,48),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["mvp_stats"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["kd"],
                        "justify": "c"
                    },
                    "combat_score": {
                        "anchor": (330,565),
                        "dimensions": (126,48),
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["mvp_stats"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["combat_score"],
                        "justify": "c"
                    },
                    "kills": {
                        "anchor": (518,565),
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
                    "agent_silhouette": {
                        "anchor": (610,360),
                        "dimensions": (332,310), 
                        "crop": lambda *x: (0,0,x[1][0]*(2/3),x[1][1]) if x[0] else (x[1][0]*(1/3),0,x[1][0],x[1][1]),
                    },
                    "agent": {
                        "anchor": (610,360),
                        "dimensions": (332,310), 
                        "target_width": 400,
                        "crop": lambda *x: (0,0,x[1][0],x[1][1]) if x[0] else (x[2]-x[1][0],0,x[2],x[1][1]),
                        "file_path": "data/agents/agent_{agent}.png"
                    },
                    "mvp_gradient": {
                        "anchor": (642,629),
                        "dimensions": (300,41),
                        "file_path": "data/misc_assets/mvp_gradient_{side}.png" 
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
                        "anchor": (102,706),
                        "dimensions": (204, 50), 
                        "color": (255,255,255),
                        "font": Builder.fonts["tungsten"]["player_name"],
                        "var_name": lambda *x: self.game_data["players"][int(x[0])][int(x[1])]["display_name"] if len(self.game_data["players"][int(x[0])][int(x[1])]["display_name"]) < 13 else self.game_data["players"][int(x[0])][int(x[1])]["display_name"][:11]+"...",
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
                        "slot_width": 204,
                        "crop": lambda *x: (abs(57-(x[0]//2)),0,57+(x[1][0]-(x[0]//2)),x[1][1]),
                        "file_path": "data/agents/agent_{agent}.png"
                    },
                    "player_gradient": {
                        "anchor": (102,803),
                        "dimensions": (204,175), 
                        "crop": lambda *x: (0,0,x[0][0]+x[1][0],x[1][1]),
                        "file_path": "data/misc_assets/player_gradient.png"
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
            team_name_label["color"] = (139,140,137) if not team["won_bool"] else team_name_label["color"]
            self.__draw_text(team_name_label,int(team_id))

            team_wl_label = refs["text"][f"team_{team_name}_wl"]
            team_wl_label["color"] = team_wl_label["color"] if team["won_bool"] else team_wl_label["alt_color"]
            self.__draw_text(team_wl_label,int(team_id))


    def draw_header_footer(self):
        refs = self.image_ref_points["header_footer"]
        for img_type, image in refs["images"].items():
            new_img = Image.open(os.path.join(Builder.cur_path,*image["file_path"].format(map=self.game_data['match_map_display_name'].lower(),mode=self.game_data['match_mode'].lower()).split("/"))).convert("RGBA")
            self.__draw_image(image,new_img)


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
                            new_img = Image.open(os.path.join(Builder.cur_path,*image["file_path"].format(agent=player['agent_display_name']).split("/"))).convert("RGBA")
                            crop_v = (True,image["dimensions"]) if team_id == 0 else (False,image["dimensions"],image["target_width"])
                            agent_image, anchor = self.__draw_image(image,new_img,size_axis="x",crop_vars=crop_v,no_draw=True)
                        
                            # draw agent silhouette
                            agent_silhouette = mvp_refs["images"]["agent_silhouette"]
                            offset = 5
                            alpha = agent_image.getchannel('A')
                            silhouette = Image.new('RGBA', agent_image.size, color=(255,70,85,255) if team_id == 0 else (13,180,150,255))
                            silhouette.putalpha(alpha) 

                            s_crop_v = (True,image["dimensions"]) if team_id == 0 else (False,image["dimensions"])
                            anchor_o = (image["anchor"][0]-offset,image["anchor"][1]) if team_id == 0 else (int(image["anchor"][0]+(image["dimensions"][0]*(1/3)))+(offset+1),image["anchor"][1])
                            self.__draw_image(agent_silhouette,silhouette,size_axis="x",crop_vars=s_crop_v,anchor_override=anchor_o)

                            self.__draw_prepared_image(agent_image,anchor)


                        elif img_type == "mvp_gradient":
                            new_img = Image.open(os.path.join(Builder.cur_path,*image['file_path'].format(side=team_id).split("/"))).convert("RGBA")
                            self.__draw_image(image,new_img)
                           

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
                            new_img = Image.open(os.path.join(Builder.cur_path,*image["file_path"].format(agent=player['agent_display_name']).split("/"))).convert("RGBA")
                            self.__draw_image(image,new_img,size_axis="x",crop_vars=(image["slot_width"],image["dimensions"]),anchor_override=(image["anchor"][0]+45,image["anchor"][1]))
                        elif img_type == "player_gradient":
                            new_img = Image.open(os.path.join(Builder.cur_path,*image["file_path"].split("/"))).convert("RGBA")
                            self.__draw_image(image,new_img,crop_vars=(image["anchor"],image["dimensions"]))                   


                    for label_type,label in player_refs["text"].items():
                        self.__draw_text(label,int(team_id),int(position))


    def build_image(self):
        

        self.draw_header_footer()
        self.draw_team_details()
        self.draw_players()


        self.img.save(os.path.join(Builder.cur_path,f"output/{self.game_data['match_id']}.png"))
        

    def __draw_image(self,img_data,new_img,size_axis="y",crop_vars=(),anchor_override=None,no_draw=False):
        width, height = new_img.size
        ratio = width/height if size_axis == "y" else height/width
        new_height = 0
        new_width = 0

        if img_data.get("target_width"):
            new_width = img_data["target_width"]
            new_height = int(ratio * new_width)
        else:
            if size_axis == "y":
                new_height = img_data["dimensions"][1]
                new_width = int(ratio * new_height)
            elif size_axis == "x":
                new_width = img_data["dimensions"][0]
                new_height = int(ratio * new_width)
        
        new_img = new_img.resize((new_width,new_height),Image.ANTIALIAS)

        crop_bounds = None
        if img_data.get("crop"):
            crop_bounds = img_data["crop"](*crop_vars)
            new_img = new_img.crop(crop_bounds)

        anchor = img_data["anchor"]
        if anchor_override is not None:
            anchor = anchor_override
        if img_data.get("centered"):
            anchor = (anchor[0]-new_width//2,anchor[1]-new_height//2)
            anchor = ((img_data["dimensions"][0]//2)+anchor[0],(img_data["dimensions"][1]//2)+anchor[1])
            
            
        if not no_draw:
            self.img.paste(new_img, anchor, new_img)
        return new_img, anchor

    def __draw_prepared_image(self,new_img,anchor):
        self.img.paste(new_img,anchor,new_img)


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
