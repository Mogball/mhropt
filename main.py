import calc as mhropt

class obj(object):
    def __init__(self, d):
        self.__dict__ = d

finsword = obj({
    "dist": [100, 70, 50, 50, 30, 50],
    "base": 300,
    "raw": 216,
    "crit": 0.15,
    "ele": 0,
    "silkbind_boost": False,
})

narga = obj({
    "dist": [70, 40, 100, 90, 70, 30],
    "base": 400,
    "raw": 188,
    "crit": 0.40,
    "ele": 0,
    "silkbind_boost": False,
})

tigrine = obj({
    "dist": [50, 40, 120, 130, 40, 20],
    "base": 400,
    "raw": 230,
    "crit": -0.20,
    "ele": 0,
    "silkbind_boost": True,
})

rimeblossom = obj({
    "dist": [70, 70, 70, 50, 70, 20],
    "base": 300,
    "raw": 210,
    "crit": 0,
    "ele": 27,
    "silkbind_boost": True,
})

goss_atk = obj({
    "dist": [100, 30, 100, 40, 70, 10],
    "base": 300,
    "raw": 234,
    "crit": -0.15,
    "ele": 20,
    "silkbind_boost": False,
})

goss_aff = obj({
    "dist": [100, 30, 100, 40, 70, 10],
    "base": 300,
    "raw": 230,
    "crit": -0.09,
    "ele": 20,
    "silkbind_boost": False,
})

narga_gs = obj({
    "dist": [70, 40, 120, 90, 60, 20],
    "base": 400,
    "raw": 188,
    "crit": 0.35,
    "ele": 0,
    "silkbind_boost": False,
})

tigrex_gs_atk = obj({
    "dist": [50, 40, 120, 120, 50, 20],
    "base": 400,
    "raw": 218,
    "crit": -0.15,
    "ele": 0,
    "silkbind_boost": False,
})

tigrex_gs_aff = obj({
    "dist": [50, 40, 120, 120, 50, 20],
    "base": 400,
    "raw": 210,
    "crit": -0.09,
    "ele": 0,
    "silkbind_boost": False,
})

rampage_gs = obj({
    "dist": [10, 10, 10, 20, 30, 50],
    "base": 80,
    "raw": 200,
    "crit": 0.20,
    "ele": 0,
    "silkbind_boost": False,
})

rampage_gs_atk = obj({
    "dist": [10, 10, 10, 20, 30, 50],
    "base": 80,
    "raw": 230,
    "crit": -0.30,
    "ele": 0,
    "silkbind_boost": False,
})

rampage_ls = obj({
    "dist": [10, 10, 10, 20, 30, 50],
    "base": 80,
    "raw": 200,
    "crit": 0.20,
    "ele": 0,
    "silkbind_boost": False,
})

params_ls1 = obj({
    "mMV": 0.836,
    "mEM": 1.96,
    "mHZV": 0.524,
    "mEZV": 0.202,
    "SBmMV": 0.869,
    "SBmEM": 2.01,
    "hits_to_sharpen": 39,
})

params_gs1 = obj({
    "mMV": 1.04,
    "mEM": 1.57,
    "mHZV": 0.536,
    "mEZV": 0.224,
    "SBmMV": 1.04,
    "SBmEM": 1.57,
    "hits_to_sharpen": 20,
})

# example usage:

build1 = obj({
    "weapon": tigrine,
    "crit_eye": 7,
    "crit_boost": 3,
    "wex": 3,
    "max_might": 3,
    "attack_boost": 0,
    "handicraft": 0,
    "razor_sharp": 0,
    "masters_touch": 0,
    "crit_element": 0,
})

print(mhropt.evaluate_build(build1, params_ls1))
