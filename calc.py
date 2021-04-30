# IMPORTANT: Displayed numbers in MHR are ROUNDED DOWN.

###############################################################################
# RAW ATTACK CALCULATIONS
###############################################################################

# LS spirit level modifies base raw (of weapon) by 1.05/1.10/1.20 for white,
# yellow, and red. Base modifier occurs before all other attack modifiers.
#
# Powertalon adds 9 raw. Powercharm adds 6. Both is 15.
#
# Petalace ATK value is the maximum raw that can be gained from collecting
# spiribirds. E.g. Demon Petalace is 20 ATK, 4 per bird. Each bird provides 4
# raw, up to 5 birds total. Collecting N birds, add 4N raw.
#
# Attack Boost adds a fixed amount of raw and a percentage of base raw. Note
# that base raw modifiers are applied beforehand. E.g. 180 base raw on weapon
# with LS red spirit and AB7 is an additional (180*1.2)*0.10 raw.
#
# Palico Power Drum adds a fixed 10 raw.
#
# Dango Booster adds 9 raw.
#
# Demondrug adds 5 raw. Mega demondrug adds 7 raw.
#
# Might Seed adds 10 raw. Demon Powder adds 10.
#

# Compute the modified base raw by taking the weapon's attack value and
# multiplying by 1 plus the sum of all base raw modifiers (LS, HH, etc.).
#
# Add to the modified base raw all fixed values. Add the percent increase from
# AB as a fraction of the modified base raw.
#
# modified_base_raw = weapon.base_raw * (1 + sum(base_raw_modifier_i))
# total_raw = modified_base_raw * (1 + AB.percentage) + sum(fixed_value_i)

atk_boost_skill = [
        (0, 0),
        (3, 0),
        (6, 0),
        (9, 0),
        (7, 0.05),
        (8, 0.06),
        (9, 0.08),
        (10, 0.10)
]

ls_spirit_raw = [1.0, 1.05, 1.1, 1.2];

def compute_total_raw(
        base_raw,
        atk_boost_lvl,
        petalace_atk,
        has_talon_and_charm=True,
        ls_spirit_level=0):
    # spirit base raw boost occurs before all other buffs
    base_raw = base_raw * ls_spirit_raw[ls_spirit_level]
    raw = (base_raw +
    # add petalace boost
        petalace_atk +
    # add powertalon and powercharm
        (15 if has_talon_and_charm else 0) +
    # add attack boost fixed
        atk_boost_skill[atk_boost_lvl][0] +
    # add attack boost percent on new base raw
        base_raw * atk_boost_skill[atk_boost_lvl][1]
    )

    # TODO add buffs
    return raw

###############################################################################
# EFFECTIVE RAW CALCULATIONS
###############################################################################

# Attack palico Rousing Roar adds 30% affinity.

# Effective Raw is an averaged raw value based on crit chance and sharpness.
# EfR = total_raw * (1 + crit_chance * crit_boost).

# 0: Red
# 1: Orange
# 2: Yellow
# 3: Green
# 4: Blue
# 5: White
sharpness_raw = [0.50, 0.75, 1.00, 1.05, 1.20, 1.32]
crit_boost_skill = [0.25, 0.30, 0.35, 0.40]

def compute_effective_raw(
        total_raw,
        crit_boost_lvl,
        crit_chance,
        sharpness_lvl=2):
    if crit_chance >= 0:
        crit_modifier = 1 + crit_chance * crit_boost_skill[crit_boost_lvl]
    else:
        crit_modifier = 1 + crit_chance * 0.75
    sharpness_modifier = sharpness_raw[sharpness_lvl]
    return total_raw * crit_modifier * sharpness_modifier

###############################################################################
# EFFECTIVE ELEMENT CALCULATIONS
###############################################################################

# LS spirit level modifies base element by 1.05/1.10/1.20 based on spirit
# level. The multiplier is applied directly to base element.
#
# Elemental attack boost skills add a fixed amount to the modified base
# element. The percentage is applied to the modified base element.
# This is analogous to AB with raw damage.
#
# Crit element raises the modifier for critical hits above 0%.

sharpness_element = [0.25, 0.50, 0.75, 1.00, 1.0625, 1.15]
crit_element_skill = [0.00, 0.05, 0.10, 0.15]

element_atk_skill = [
        (0, 0),
        (2, 0),
        (3, 0),
        (4, 0.05),
        (4, 0.10),
        (4, 0.20)
]

ls_spirit_element = [1.00, 1.05, 1.10, 1.20]

def compute_total_element(
        base_element,
        element_atk_lvl=5,
        ls_spirit_level=0):
    if base_element == 0:
        return 0
    # base element modifiers
    base_element = base_element * ls_spirit_element[ls_spirit_level]
    # elemental attack boost
    EAB = element_atk_skill[element_atk_lvl]
    return base_element + EAB[0] + base_element * EAB[1]

def compute_effective_element(
        total_element,
        crit_element_lvl,
        crit_chance,
        sharpness_lvl=3):
    crit_chance = 0 if crit_chance < 0 else crit_chance
    crit_modifier = 1 + crit_chance * crit_element_skill[crit_element_lvl]
    sharpness_modifier = sharpness_element[sharpness_lvl]
    return total_element * crit_modifier * sharpness_modifier

###############################################################################
# DAMAGE CALCULATION
###############################################################################

# Total damage dealt to a monster is computed using effective raw and effective
# element. EfR and EfE are modified by the monster's hitzone value (HZV) and
# elemental hitzone value (EZV). Values are displayed as PERCENTAGES in the
# Hunter's Notes.
#
# EfR is affected by the Motion Value (MV) of the move. MV is displayed as a
# PERCENTAGE. EfE is affected by the Elemental Modifier (EM) of the move, a
# value that is normally 1 or close to 1.

# Values provided as fractions.
def compute_total_damage(
        EfR, EfE,
        HZV, EZV,
        MV, EM):
    return EfR * HZV * MV + EfE * EZV * EM

###############################################################################
# EFFECTIVE DAMAGE CALCULATION
###############################################################################

razor_sharp_skill = [0, 0.10, 0.25, 0.50]
masters_touch_skill = [0, 0.20, 0.40, 0.80]

def estimate_damage(
        monster_hp,
        EfR, EfE,
        avg_mv, avg_em,
        avg_hzv, avg_ezv,
        sharpness_dist,
        base_sharpness,
        handicraft_lvl,
        razor_sharp_lvl,
        masters_touch_lvl,
        crit_chance,
        hits_to_sharpen):
    base_hit_sharp = []
    # handicraft provides 10 hits per level
    base_sharpness += handicraft_lvl * 10
    # fill in the sharpness bar based on the base sharpness
    for i in range(0, 6):
        nhits = sharpness_dist[i]
        if nhits > base_sharpness:
            base_hit_sharp.append((base_sharpness, i))
            base_sharpness = 0
        else:
            base_hit_sharp.append((nhits, i))
            base_sharpness -= nhits
    # widen the bar based on the razor sharp and master's touch level
    crit_chance = 0 if crit_chance < 0 else crit_chance
    razor_mul = 1 / (1 - razor_sharp_skill[razor_sharp_lvl])
    master_mul = 1 / (1 - masters_touch_skill[masters_touch_lvl] * crit_chance)
    hit_sharp = []
    for bar in base_hit_sharp:
        new_hits = bar[0] * razor_mul * master_mul
        if new_hits > 0:
            hit_sharp.append((new_hits, bar[1]))
    # append the first N hits before sharpen
    if hits_to_sharpen > 0:
        extra = []
        for bar in reversed(hit_sharp):
            if hits_to_sharpen <= bar[0]:
                extra.append((hits_to_sharpen, bar[1]))
                break
            else:
                extra.append((bar[0], bar[1]))
                hits_to_sharpen -= bar[0]
        hit_sharp += reversed(extra)
    # do the simulation (TODO make faster with bulk)
    hit_order = list(reversed(hit_sharp))
    hit_idx = 0
    tEfR = 0
    tEfE = 0
    nhits = 0
    while monster_hp > 0:
        if hit_order[hit_idx][0] <= 0:
            hit_idx += 1
        bar = hit_order[hit_idx]
        sraw = sharpness_raw[bar[1]]
        sele = sharpness_element[bar[1]]
        # weighted average
        tEfR += EfR * sraw
        tEfE += EfE * sele
        nhits += 1
        # subtract HP
        monster_hp -= compute_total_damage(
                EfR * sraw, EfE * sele,
                avg_hzv, avg_ezv,
                avg_mv, avg_em)
        # reduce sharpness
        hit_order[hit_idx] = (bar[0] - 1, bar[1])

    return tEfR / nhits, tEfE / nhits

###############################################################################
# CRIT CALCULATION
###############################################################################

crit_eye_skill = [0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40]
max_might_skill = [0, 0.10, 0.20, 0.30]
wex_skill = [0, 0.15, 0.30, 0.50]
latent_power_skill = [0, 0.10, 0.20, 0.30, 0.40, 0.50]

def compute_crit_chance(
        base_crit,
        crit_eye_lvl,
        max_might_lvl,
        wex_lvl,
        latent_power_lvl=0,
        latent_power_uptime=0.5,
        rousing_roar=False,
        rousing_roar_uptime=0.33,
        max_might_uptime=1.0,
        wex_uptime=1.0):
    crit = base_crit
    crit += crit_eye_skill[crit_eye_lvl]
    crit += max_might_skill[max_might_lvl] * max_might_uptime
    crit += wex_skill[wex_lvl] * wex_uptime
    crit += latent_power_skill[latent_power_lvl] * latent_power_uptime
    crit += (0.30 if rousing_roar else 0) * rousing_roar_uptime
    crit = 1 if crit > 1 else crit
    return crit

# Assume attack buffs: Might Seed +10, Demon Powder +10, Mega Demondrug +7,
#                      Booster +9
# For most speedruns, might seed and demon powder have close to 100% uptime.

def evaluate_build(build, params, atk_buff=36):
    tR = compute_total_raw(
            build.weapon.raw,
            build.attack_boost,
            atk_buff)
    tE = compute_total_element(build.weapon.ele)
    crit = compute_crit_chance(
            build.weapon.crit,
            build.crit_eye,
            build.max_might,
            build.wex)
    EfR = compute_effective_raw(
            tR,
            build.crit_boost,
            crit)
    EfE = compute_effective_element(
            tE,
            build.crit_element,
            crit)
    SB = build.weapon.silkbind_boost
    mMV = params.SBmMV if SB else params.mMV
    mEM = params.SBmEM if SB else params.mEM
    eEfR, eEfE = estimate_damage(
            13500,
            EfR, EfE,
            mMV, mEM,
            params.mHZV, params.mEZV,
            build.weapon.dist,
            build.weapon.base,
            build.handicraft,
            build.razor_sharp,
            build.masters_touch,
            crit,
            params.hits_to_sharpen)
    eDmg = eEfR * params.mHZV * mMV + eEfE * params.mEZV * mEM
    return eEfR, eEfE, eDmg

