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
        has_talon_and_charm,
        ls_spirit_level):
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
    crit_modifier = 1 + crit_chance * crit_boost_skill[crit_boost_lvl]
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
        element_atk_lvl,
        ls_spirit_level):
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
