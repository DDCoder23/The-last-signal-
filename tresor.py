import random
import json
import os
import admin_manager
import jet_de_des as de

pa = 1
po = 10 * pa
pp = 10 * po



class tresor:
    def __init__(self):
        self.loot_par_niveau = {
            1: {"Artefact admin": 1},
            2: {"Artefact commun": 1, "Artefact admin": 1},
            3: {"Artefact commun": 1, "Artefact admin": 1},
            4: {"Artefact commun": 1, "Artefact admin": 1},
            5: {"Artefact commun": 1, "Artefact admin": 1},
            6: {"Artefact commun": 2, "Artefact peu commun": 1, "Artefact admin": 2},
            7: {"Artefact commun": 2, "Artefact peu commun": 1, "Artefact admin": 2},
            8: {"Artefact commun": 2, "Artefact peu commun": 1, "Artefact admin": 2},
            9: {"Artefact commun": 2, "Artefact peu commun": 1, "Artefact admin": 2},
            10: {
                "Artefact commun": 2,
                "Artefact peu commun": 2,
                "Artefact rare": 1,
                "Artefact admin": 2,
            },
            11: {
                "Artefact commun": 2,
                "Artefact peu commun": 2,
                "Artefact rare": 1,
                "Artefact admin": 3,
            },
            12: {
                "Artefact commun": 3,
                "Artefact peu commun": 2,
                "Artefact rare": 1,
                "Artefact admin": 3,
            },
            13: {
                "Artefact commun": 3,
                "Artefact peu commun": 2,
                "Artefact rare": 1,
                "Artefact admin": 3,
            },
            14: {
                "Artefact commun": 3,
                "Artefact peu commun": 2,
                "Artefact rare": 2,
                "Artefact super rare": 1,
                "Artefact admin": 3,
            },
            15: {
                "Artefact commun": 3,
                "Artefact peu commun": 2,
                "Artefact rare": 2,
                "Artefact super rare": 1,
                "Artefact admin": 3,
            },
            16: {
                "Artefact commun": 3,
                "Artefact peu commun": 3,
                "Artefact rare": 2,
                "Artefact super rare": 1,
                "Artefact admin": 4,
            },
            17: {
                "Artefact commun": 3,
                "Artefact peu commun": 3,
                "Artefact rare": 2,
                "Artefact super rare": 1,
                "Artefact admin": 4,
            },
            18: {
                "Artefact commun": 4,
                "Artefact peu commun": 3,
                "Artefact rare": 2,
                "Artefact super rare": 2,
                "Artefact epique": 1,
                "Artefact admin": 4,
            },
            19: {
                "Artefact commun": 4,
                "Artefact peu commun": 3,
                "Artefact rare": 2,
                "Artefact super rare": 2,
                "Artefact epique": 1,
                "Artefact admin": 4,
            },
            20: {
                "Artefact commun": 5,
                "Artefact peu commun": 3,
                "Artefact rare": 3,
                "Artefact super rare": 2,
                "Artefact epique": 1,
                "Artefact admin": 4,
            },
            21: {
                "Artefact commun": 5,
                "Artefact peu commun": 3,
                "Artefact rare": 3,
                "Artefact super rare": 2,
                "Artefact epique": 1,
                "Artefact admin": 5,
            },
            22: {
                "Artefact commun": 5,
                "Artefact peu commun": 4,
                "Artefact rare": 3,
                "Artefact super rare": 2,
                "Artefact epique": 2,
                "Artefact legendaire": 1,
                "Artefact admin": 5,
            },
            23: {
                "Artefact commun": 6,
                "Artefact peu commun": 4,
                "Artefact rare": 3,
                "Artefact super rare": 2,
                "Artefact epique": 2,
                "Artefact legendaire": 1,
                "Artefact admin": 5,
            },
            24: {
                "Artefact commun": 6,
                "Artefact peu commun": 5,
                "Artefact rare": 3,
                "Artefact super rare": 3,
                "Artefact epique": 2,
                "Artefact legendaire": 1,
                "Artefact admin": 5,
            },
            25: {
                "Artefact commun": 6,
                "Artefact peu commun": 5,
                "Artefact rare": 3,
                "Artefact super rare": 3,
                "Artefact epique": 2,
                "Artefact legendaire": 1,
                "Artefact admin": 5,
            },
            26: {
                "Artefact commun": 6,
                "Artefact peu commun": 5,
                "Artefact rare": 4,
                "Artefact super rare": 3,
                "Artefact epique": 2,
                "Artefact legendaire": 2,
                "Artefact admin": 6,
            },
            27: {
                "Artefact commun": 6,
                "Artefact peu commun": 6,
                "Artefact rare": 4,
                "Artefact super rare": 3,
                "Artefact epique": 2,
                "Artefact legendaire": 2,
                "Artefact admin": 6,
            },
            28: {
                "Artefact commun": 7,
                "Artefact peu commun": 6,
                "Artefact rare": 5,
                "Artefact super rare": 3,
                "Artefact epique": 3,
                "Artefact legendaire": 2,
                "Artefact admin": 6,
            },
            29: {
                "Artefact commun": 7,
                "Artefact peu commun": 6,
                "Artefact rare": 5,
                "Artefact super rare": 3,
                "Artefact epique": 3,
                "Artefact legendaire": 2,
                "Artefact admin": 6,
            },
            30: {
                "Artefact commun": 7,
                "Artefact peu commun": 6,
                "Artefact rare": 5,
                "Artefact super rare": 4,
                "Artefact epique": 3,
                "Artefact legendaire": 2,
                "Artefact admin": 6,
            },
            31: {
                "Artefact commun": 7,
                "Artefact peu commun": 6,
                "Artefact rare": 6,
                "Artefact super rare": 4,
                "Artefact epique": 3,
                "Artefact legendaire": 2,
                "Artefact admin": 7,
            },
            32: {
                "Artefact commun": 7,
                "Artefact peu commun": 7,
                "Artefact rare": 6,
                "Artefact super rare": 5,
                "Artefact epique": 3,
                "Artefact legendaire": 3,
                "Artefact admin": 7,
            },
            33: {
                "Artefact commun": 7,
                "Artefact peu commun": 7,
                "Artefact rare": 6,
                "Artefact super rare": 5,
                "Artefact epique": 3,
                "Artefact legendaire": 3,
                "Artefact admin": 7,
            },
            34: {
                "Artefact commun": 7,
                "Artefact peu commun": 7,
                "Artefact rare": 6,
                "Artefact super rare": 5,
                "Artefact epique": 4,
                "Artefact legendaire": 3,
                "Artefact admin": 7,
            },
            35: {
                "Artefact commun": 8,
                "Artefact peu commun": 7,
                "Artefact rare": 6,
                "Artefact super rare": 6,
                "Artefact epique": 4,
                "Artefact legendaire": 3,
                "Artefact admin": 7,
            },
            36: {
                "Artefact commun": 8,
                "Artefact peu commun": 7,
                "Artefact rare": 7,
                "Artefact super rare": 6,
                "Artefact epique": 5,
                "Artefact legendaire": 3,
                "Artefact admin": 8,
            },
            37: {
                "Artefact commun": 8,
                "Artefact peu commun": 7,
                "Artefact rare": 7,
                "Artefact super rare": 6,
                "Artefact epique": 5,
                "Artefact legendaire": 3,
                "Artefact admin": 8,
            },
            38: {
                "Artefact commun": 8,
                "Artefact peu commun": 7,
                "Artefact rare": 7,
                "Artefact super rare": 6,
                "Artefact epique": 5,
                "Artefact legendaire": 4,
                "Artefact admin": 8,
            },
            39: {
                "Artefact commun": 8,
                "Artefact peu commun": 8,
                "Artefact rare": 7,
                "Artefact super rare": 6,
                "Artefact epique": 6,
                "Artefact legendaire": 4,
                "Artefact admin": 8,
            },
            40: {
                "Artefact commun": 8,
                "Artefact peu commun": 8,
                "Artefact rare": 7,
                "Artefact super rare": 7,
                "Artefact epique": 6,
                "Artefact legendaire": 5,
                "Artefact admin": 8,
            },
            41: {
                "Artefact commun": 8,
                "Artefact peu commun": 8,
                "Artefact rare": 7,
                "Artefact super rare": 7,
                "Artefact epique": 6,
                "Artefact legendaire": 5,
                "Artefact admin": 9,
            },
            42: {
                "Artefact commun": 8,
                "Artefact peu commun": 8,
                "Artefact rare": 7,
                "Artefact super rare": 7,
                "Artefact epique": 6,
                "Artefact legendaire": 5,
                "Artefact admin": 9,
            },
            43: {
                "Artefact commun": 8,
                "Artefact peu commun": 8,
                "Artefact rare": 8,
                "Artefact super rare": 7,
                "Artefact epique": 6,
                "Artefact legendaire": 6,
                "Artefact admin": 9,
            },
            44: {
                "Artefact commun": 8,
                "Artefact peu commun": 8,
                "Artefact rare": 8,
                "Artefact super rare": 7,
                "Artefact epique": 7,
                "Artefact legendaire": 6,
                "Artefact admin": 9,
            },
            45: {
                "Artefact commun": 9,
                "Artefact peu commun": 8,
                "Artefact rare": 8,
                "Artefact super rare": 7,
                "Artefact epique": 7,
                "Artefact legendaire": 6,
                "Artefact admin": 9,
            },
            46: {
                "Artefact commun": 9,
                "Artefact peu commun": 8,
                "Artefact rare": 8,
                "Artefact super rare": 7,
                "Artefact epique": 7,
                "Artefact legendaire": 6,
                "Artefact admin": 10,
            },
            47: {
                "Artefact commun": 9,
                "Artefact peu commun": 8,
                "Artefact rare": 8,
                "Artefact super rare": 8,
                "Artefact epique": 7,
                "Artefact legendaire": 6,
                "Artefact admin": 10,
            },
        }

        self.objets_garantis = {
            1: {
                **{
                    "argent": de.jet_de_des(6, 2) * pa,
                    "torche": 2,
                    "sac": 3,
                    "épée de bois": 3,
                },
                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 18 else {}),
                **({"pain": random.randint(3, 5)} if de.jet_de_des(20, 1) >= 4 else {}),
            },
            2: {
                **{
                    "argent": de.jet_de_des(6, 4) * pa,
                    "torche": 1,
                    "sac": 2,
                    "épée de pierre": 1,
                },
                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 16 else {}),
            },
            3: {
                **{
                    "argent": de.jet_de_des(6, 1) * 10 * pa,
                    "torche": 2,
                    "sac": 1,
                    "épée de pierre": 1,
                },
                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 14 else {}),
            },
            4: {
                **{"argent": de.jet_de_des(6, 2) * 10 * pa},
                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 12 else {}),
            },
            5: {
                **{"argent": de.jet_de_des(6, 3) * 10 * pa},
                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 10 else {}),
            },
            6: {
                **{"argent": de.jet_de_des(6, 4) * 10 * pa},
                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 8 else {}),
            },
            7: {
                **{"argent": de.jet_de_des(6, 5) * 10 * pa},
                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 6 else {}),
            },
            8: {
                **{"argent": de.jet_de_des(6, 1) * 100 * pa},
                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 4 else {}),
            },
            9: {
                **{"argent": de.jet_de_des(6, 2) * 100 * pa},
                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 2 else {}),
            },
            10: {"argent": de.jet_de_des(6, 3) * 100 * pa, "gemmes": 1},
            11: {"argent": de.jet_de_des(6, 4) * 100 * pa, "gemmes": 1},
            12: {"argent": de.jet_de_des(6, 5) * 100 * pa, "gemmes": 1},
            13: {"argent": de.jet_de_des(6, 1) * 100 * po, "gemmes": 1},
            14: {"argent": de.jet_de_des(6, 2) * 100 * po, "gemmes": 1},
            15: {"argent": de.jet_de_des(6, 3) * 100 * po, "gemmes": 1},
            16: {"argent": de.jet_de_des(6, 4) * 100 * po, "gemmes": 1},
            17: {"argent": de.jet_de_des(6, 5) * 100 * po, "gemmes": 1},
            18: {"argent": de.jet_de_des(6, 1) * 100 * pp, "gemmes": 1},
            19: {"argent": de.jet_de_des(6, 2) * 100 * pp, "gemmes": 1},
            20: {"argent": de.jet_de_des(6, 3) * 100 * pp, "gemmes": 2},
            21: {"argent": de.jet_de_des(6, 4) * 100 * pp, "gemmes": 2},
            22: {"argent": de.jet_de_des(6, 5) * 100 * pp, "gemmes": 2},
            23: {"argent": de.jet_de_des(6, 6) * 100 * pp, "gemmes": 2},
            24: {"argent": de.jet_de_des(6, 7) * 100 * pp, "gemmes": 2},
            25: {"argent": de.jet_de_des(6, 8) * 100 * pp, "gemmes": 2},
            26: {"argent": de.jet_de_des(6, 9) * 100 * pp, "gemmes": 2},
            27: {"argent": de.jet_de_des(6, 10) * 100 * pp, "gemmes": 2},
            28: {"argent": de.jet_de_des(6, 11) * 100 * pp, "gemmes": 2},
            29: {"argent": de.jet_de_des(6, 12) * 100 * pp, "gemmes": 2},
            30: {"argent": de.jet_de_des(6, 13) * 100 * pp, "gemmes": 3},
            31: {"argent": de.jet_de_des(6, 14) * 100 * pp, "gemmes": 3},
            32: {"argent": de.jet_de_des(6, 15) * 100 * pp, "gemmes": 3},
            33: {"argent": de.jet_de_des(6, 16) * 100 * pp, "gemmes": 3},
            34: {"argent": de.jet_de_des(6, 17) * 100 * pp, "gemmes": 3},
            35: {"argent": de.jet_de_des(6, 18) * 100 * pp, "gemmes": 3},
            36: {"argent": de.jet_de_des(6, 19) * 100 * pp, "gemmes": 3},
            37: {"argent": de.jet_de_des(20, 6) * 100 * pp, "gemmes": 3},
            38: {"argent": de.jet_de_des(20, 7) * 100 * pp, "gemmes": 3},
            39: {"argent": de.jet_de_des(20, 8) * 100 * pp, "gemmes": 3},
            40: {"argent": de.jet_de_des(20, 9) * 100 * pp, "gemmes": 4},
            41: {
                **{"argent": de.jet_de_des(20, 10) * 100 * pp, "gemmes": 4},
                **(
                    {"livre enchant niv 1": random.randint(1, 9)}
                    if de.jet_de_des(20, 1) >= 20
                    else {}
                ),
            },
            42: {
                **{"argent": de.jet_de_des(20, 11) * 100 * pp, "gemmes": 4},
                **(
                    {"livre enchant niv 1": random.randint(1, 9)}
                    if de.jet_de_des(20, 1) >= 18
                    else {}
                ),
            },
            43: {
                **{"argent": de.jet_de_des(20, 12) * 100 * pp, "gemmes": 4},
                **(
                    {"livre enchant niv 1": random.randint(1, 9)}
                    if de.jet_de_des(20, 1) >= 16
                    else {}
                ),
            },
            44: {
                **{"argent": de.jet_de_des(20, 13) * 100 * pp, "gemmes": 4},
                **(
                    {"livre enchant niv 1": random.randint(1, 9)}
                    if de.jet_de_des(20, 1) >= 14
                    else {}
                ),
            },
            45: {
                **{"argent": de.jet_de_des(20, 14) * 100 * pp, "gemmes": 4},
                **(
                    {"livre enchant niv 1": random.randint(1, 9)}
                    if de.jet_de_des(20, 1) >= 12
                    else {}
                ),
            }, 
            46: {
                **{"argent": de.jet_de_des(20, 15) * 100 * pp, "gemmes": 4},
                **(
                    {"livre enchant niv 1": random.randint(1, 9)}
                    if de.jet_de_des(20, 1) >= 10
                    else {}
                ),
            },
            47: {
                **{"argent": de.jet_de_des(20, 16) * 100 * pp, "gemmes": 4},
                **(
                    {"livre enchant niv 1": random.randint(1, 9)}
                    if de.jet_de_des(20, 1) >= 8
                    else {}
                ),
            },
        }
        self.quantite_objets = {
            "cuivre": random.randint(2, 9),
            "fer": random.randint(2, 9),
            "lapiz": random.randint(2, 9),
            "or": random.randint(2, 9),
            "redstone": random.randint(2, 9),
            "netherite": random.randint(2, 9),
            "diamant": random.randint(2, 9),
            "balles": random.randint(2, 9),
            "carreau d'arbalète ": random.randint(2, 9),
            "chargeur": random.randint(2, 9),
            "flèches communes": random.randint(2, 9),
            "flèches peu rares": random.randint(2, 9),
            "flèches rares": random.randint(2, 9),
            "flèches super rares": random.randint(2, 9),
            "flèches exotiques": random.randint(2, 9),
            "flèches épiques": random.randint(2, 9),
            "flèches légendaire": random.randint(2, 9),

        }
        self.sous_loot = {
            "Artefact commun": {"food": 80, "minerais": 19, "équi": 1},
            "Artefact peu commun": {"food": 50, "minerais": 40, "équi": 10},
            "Artefact rare": {"minerais": 50, "équi": 25, "potion": 25},
            "Artefact super rare": {
                "potion": 50,
                "équi": 40,
                "minerais": 9.9,
                "livre enchant": 0.1,
            },
            "Artefact epique": {"potion": 15, "équi": 75, "livre enchant": 10},
            "Artefact legendaire": {"potion": 5, "équi": 75, "livre enchant": 20},
            "Artefact admin": {"livre enchant": 100},
            "livre enchant": {
                "livre enchant niv 1": 45 if admin_manager.IS_ADMIN else 70,
                "livre enchant niv 2": 15 if admin_manager.IS_ADMIN else 20,
                "livre enchant niv 3": 13 if admin_manager.IS_ADMIN else 5,
                "livre enchant niv 4": 12 if admin_manager.IS_ADMIN else 3,
                "livre enchant niv 5": 8 if admin_manager.IS_ADMIN else 1.5,
                "livre enchant niv 6": 7 if admin_manager.IS_ADMIN else 0.5,
            },
            "équi": {"armes": 20, "outils": 20, "armure": 20,"véhicules" :20,"batiments":20},
            "armes": {
                "explosifs": 20,
                "armes tranchantes": 30,
                "armes à feu": 1.5,
                "armes perforantes": 20,
                "munitions": 8,
                "armes contendantes": 20,
                "artillerie lourde": 0.5,
            },
             "explosifs": {
                "grenades" : 20,
                "C4": 20,
                "dynamite": 20,
                "TNT": 20,
                "bombe": 15,
                "mine antichar":5
            },
            "grenades": {
                "grenade" : 20,
                "grenade à fragmentation": 20,
                "grenade sainte": 20,
                "Super grenade": 20,
                "grenade banane": 20,
            },
            "munitions": {
                "flèches": 60,
                "chargeur": 5,
                "carreau d'arbalète": 20,
                "balles": 15,
            },
           "flèches": {
                "flèches communes": 50,
                "flèches peu rares": 20,
                "flèches rares": 10,
                "flèches super rares": 9,
                "flèches exotiques":6 ,
                "flèches épiques":4.5 ,
                "flèches légendaire": 0.5,

                

            },
            "minerais": {
                "cuivre": 60,
                "fer": 20,
                "lapiz": 10,
                "or": 7,
                "redstone": 3,
                "netherite": 2,
                "diamant": 1,
            },
            "food": {
                "viande": 10,
                "pain": 70,
                "fruit et légumes": 10,
                "herbes et racines": 10,
            },
            "potion": {"potion de soin": 90, "potion de mana": 9, "potion rare": 1},
            "potion de soin": {
                "potion de soin léger": 50,
                "potion de soin modéré": 33.32,
                "potion de délivrance": 16.68,
            },
        }

        self.seuil_artefact_commun = {
            2: 20,
            3: 19,
            4: 17,
            5: 15,
            6: 15,
            7: 14,
            8: 13,
            9: 12,
            10: 11,
            11: 10,
            12: 10,
            13: 9,
            14: 9,
            15: 7,
            16: 6,
            17: 5,
            18: 5,
            19: 5,
            20: 5,
            21: 5,
            22: 5,
            23: 5,
            24: 5,
            25: 5,
            26: 5,
            27: 5,
            28: 5,
            29: 5,
            30: 5,
            31: 5,
            32: 5,
            33: 5,
            34: 5,
            35: 5,
            36: 5,
            37: 5,
            38: 5,
            39: 5,
            40: 5,
            41: 5,
            42: 5,
            43: 5,
            44: 5,
            45: 5,
            46: 5,
            47: 5,
        }
        self.seuil_artefact_peu_commun = {
            6: 20,
            7: 19,
            8: 17,
            9: 15,
            10: 15,
            11: 14,
            12: 13,
            13: 12,
            14: 11,
            15: 10,
            16: 10,
            17: 9,
            18: 8,
            19: 7,
            20: 6,
            21: 5,
            22: 5,
            23: 5,
            24: 5,
            25: 5,
            26: 5,
            27: 5,
            28: 5,
            29: 5,
            30: 5,
            31: 5,
            32: 5,
            33: 5,
            34: 5,
            35: 5,
            36: 5,
            37: 5,
            38: 5,
            39: 5,
            40: 5,
            41: 5,
            42: 5,
            43: 5,
            44: 5,
            45: 5,
            46: 5,
            47: 5,
        }
        self.seuil_artefact_rare = {
            10: 20,
            11: 19,
            12: 17,
            13: 15,
            14: 15,
            15: 14,
            16: 13,
            17: 12,
            18: 11,
            19: 10,
            20: 10,
            21: 9,
            22: 8,
            23: 7,
            24: 6,
            25: 5,
            26: 5,
            27: 5,
            28: 5,
            29: 5,
            30: 5,
            31: 5,
            32: 5,
            33: 5,
            34: 5,
            35: 5,
            36: 5,
            37: 5,
            38: 5,
            39: 5,
            40: 5,
            41: 5,
            42: 5,
            43: 5,
            44: 5,
            45: 5,
            46: 5,
            47: 5,
        }
        self.seuil_artefact_super_rare = {
            14: 20,
            15: 19,
            16: 17,
            17: 15,
            18: 15,
            19: 14,
            20: 13,
            21: 12,
            22: 11,
            23: 10,
            24: 10,
            25: 9,
            26: 8,
            27: 7,
            28: 6,
            29: 5,
            30: 5,
            31: 5,
            32: 5,
            33: 5,
            34: 5,
            35: 5,
            36: 5,
            37: 5,
            38: 5,
            39: 5,
            40: 5,
            41: 5,
            42: 5,
            43: 5,
            44: 5,
            45: 5,
            46: 5,
            47: 5,
        }
        self.seuil_artefact_epique = {
            18: 20,
            19: 19,
            20: 17,
            21: 15,
            22: 15,
            23: 14,
            24: 13,
            25: 12,
            26: 11,
            27: 10,
            28: 10,
            29: 9,
            30: 8,
            31: 7,
            32: 6,
            33: 5,
            34: 5,
            35: 5,
            36: 5,
            37: 5,
            38: 5,
            39: 5,
            40: 5,
            41: 5,
            42: 5,
            43: 5,
            44: 5,
            45: 5,
            46: 5,
            47: 5,
        }
        self.seuil_artefact_legendaire = {
            22: 20,
            23: 19,
            24: 17,
            25: 15,
            26: 15,
            27: 14,
            28: 13,
            29: 12,
            30: 11,
            31: 10,
            32: 10,
            33: 9,
            34: 8,
            35: 7,
            36: 6,
            37: 5,
            38: 5,
            39: 5,
            40: 5,
            41: 5,
            42: 5,
            43: 5,
            44: 5,
            45: 5,
            46: 5,
            47: 5,
        }

        self.fichier_sauvegarde = "echecs.json"
        self._charger_echecs()
        self.loot_admin = []
        for i in range(1, 101):
            self.loot_admin.append(i)

    def _tirer_sous_loot(self, resultat, objet, niveau):
        if objet in self.sous_loot:
            loot = self.sous_loot[objet]
            if objet not in self.echecs_par_niveau:
                self.echecs_par_niveau[objet] = {k: 0 for k in loot}
            table = []
            total_base = sum(loot.values()) or 1
            for sous_objet, base_chance in loot.items():
                echec_count = self.echecs_par_niveau[objet].get(sous_objet, 0)
                bonus = 0
                pourcentage = (base_chance / total_base) * 100
                if pourcentage < 10:
                    bonus += min(echec_count, 10)
                table.append((sous_objet, base_chance + bonus))

            total = sum(ch for _, ch in table)
            r = random.uniform(0, total)
            cumul = 0
            for sous_objet, chance in table:
                cumul += chance
                if r <= cumul:
                    # Met à jour les échecs pour ce niveau/sous_loot
                    for key in self.echecs_par_niveau[objet]:
                        if key == sous_objet:
                            self.echecs_par_niveau[objet][key] = 0
                        else:
                            self.echecs_par_niveau[objet][key] += 1
                    self._tirer_sous_loot(resultat, sous_objet, niveau)
                    return
        else:
            quantite = self.quantite_objets.get(objet, 1)
            resultat[objet] = resultat.get(objet, 0) + quantite

    def _tirage_avec_bonus(self, niveau):
        """Tirage aléatoire pondéré avec ajustement automatique pour objets rares"""
        loot = self.loot_par_niveau.get(niveau, {})
        if niveau not in self.echecs_par_niveau:
            self.echecs_par_niveau[niveau] = {k: 0 for k in loot}

        table = []
        total_base = sum(loot.values()) or 1
        for objet, base_chance in loot.items():
            echec_count = self.echecs_par_niveau[niveau].get(objet, 0)
            bonus = 0
            pourcentage = (base_chance / total_base) * 100
            if pourcentage <= 15:
                bonus += min(echec_count, 15)
                if pourcentage <= 10:
                    bonus += min(echec_count, 10)
                    if pourcentage <= 5:
                        bonus += min(echec_count, 5)
                        if pourcentage < 1:
                            bonus += min(echec_count, 15)
                            if pourcentage < 0.1:
                                bonus += min(echec_count, 30)

            table.append((objet, base_chance + bonus))

        total = sum(ch for _, ch in table)
        r = random.uniform(0, total)
        cumul = 0
        for objet, chance in table:
            cumul += chance
            if r <= cumul:
                self._mettre_a_jour_echecs(niveau, objet)
                return objet

    def _mettre_a_jour_echecs(self, niveau, objet_obtenu):
        rare_objects = self.echecs_par_niveau.get(niveau, {})
        for obj in rare_objects:
            if obj == objet_obtenu:
                rare_objects[obj] = 0
            else:
                rare_objects[obj] += 1
        self.echecs_par_niveau[niveau] = rare_objects

    def _sauvegarder_echecs(self):
        with open(self.fichier_sauvegarde, "w") as f:
            json.dump(self.echecs_par_niveau, f)

    def _charger_echecs(self):
        if os.path.exists(self.fichier_sauvegarde):
            with open(self.fichier_sauvegarde, "r") as f:
                self.echecs_par_niveau = json.load(f)
        else:
            self.echecs_par_niveau = {}

    def ouvrir_tresor(self, niveau=1):
        global resultat
        resultat = {}

        for obj, quantite in self.objets_garantis.get(niveau, {}).items():
            resultat[obj] = quantite
        if niveau in self.seuil_artefact_commun:
            quantite = self.loot_par_niveau[niveau].get("Artefact commun", 0)
            for _ in range(quantite):
                if de.jet_de_des(20, 1) >= self.seuil_artefact_commun[niveau]:
                    objet_rare = self._tirage_avec_bonus(niveau)
                    if objet_rare:
                        self._tirer_sous_loot(resultat, objet_rare, niveau)
            self._sauvegarder_echecs()
        if niveau in self.seuil_artefact_peu_commun:
            quantite = self.loot_par_niveau[niveau].get("Artefact peu commun", 0)
            for _ in range(quantite):
                if de.jet_de_des(20, 1) >= self.seuil_artefact_peu_commun[niveau]:
                    objet_rare = self._tirage_avec_bonus(niveau)
                    if objet_rare:
                        self._tirer_sous_loot(resultat, objet_rare, niveau)
            self._sauvegarder_echecs()
        if niveau in self.seuil_artefact_rare:
            quantite = self.loot_par_niveau[niveau].get("Artefact rare", 0)
            for _ in range(quantite):
                if de.jet_de_des(20, 1) >= self.seuil_artefact_rare[niveau]:
                    objet_rare = self._tirage_avec_bonus(niveau)
                    if objet_rare:
                        self._tirer_sous_loot(resultat, objet_rare, niveau)
            self._sauvegarder_echecs()
        if niveau in self.seuil_artefact_super_rare:
            quantite = self.loot_par_niveau[niveau].get("Artefact super rare", 0)
            for _ in range(quantite):
                if de.jet_de_des(20, 1) >= self.seuil_artefact_super_rare[niveau]:
                    objet_rare = self._tirage_avec_bonus(niveau)
                    if objet_rare:
                        self._tirer_sous_loot(resultat, objet_rare, niveau)
            self._sauvegarder_echecs()
        if niveau in self.seuil_artefact_epique:
            quantite = self.loot_par_niveau[niveau].get("Artefact epique", 0)
            for _ in range(quantite):
                if de.jet_de_des(20, 1) >= self.seuil_artefact_epique[niveau]:
                    objet_rare = self._tirage_avec_bonus(niveau)
                    if objet_rare:
                        self._tirer_sous_loot(resultat, objet_rare, niveau)
            self._sauvegarder_echecs()
        if niveau in self.seuil_artefact_legendaire:
            quantite = self.loot_par_niveau[niveau].get("Artefact legendaire", 0)
            for _ in range(quantite):
                if de.jet_de_des(20, 1) >= self.seuil_artefact_legendaire[niveau]:
                    objet_rare = self._tirage_avec_bonus(niveau)
                    if objet_rare:
                        self._tirer_sous_loot(resultat, objet_rare, niveau)
            self._sauvegarder_echecs()

        return resultat

    @admin_manager.admin_only
    def ouvrir_tresor_admin(self, niveau=1):
        resultat = self.ouvrir_tresor(niveau)

        if niveau in self.loot_admin:
            quantite = self.loot_par_niveau[niveau].get("Artefact admin", 0)

            for _ in range(quantite):

                objet_rare = self._tirage_avec_bonus(niveau)
                if objet_rare:
                    self._tirer_sous_loot(resultat, objet_rare, niveau)
            self._sauvegarder_echecs()

        return resultat


coffre = tresor()


def create_tresor(niveau):
    return (
        coffre.ouvrir_tresor_admin(niveau)
        if admin_manager.IS_ADMIN
        else coffre.ouvrir_tresor(niveau)
    )
