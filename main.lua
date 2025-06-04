-- Creates an atlas for cards to use
SMODS.Atlas {
    -- Key for code to find it with
    key = "ModdedVanilla",
    -- The name of the file, for the code to pull the atlas from
    path = "ModdedVanilla.png",
    -- Width of each sprite in 1x size
    px = 71,
    -- Height of each sprite in 1x size
    py = 95
}

SMODS.Atlas {
    -- Key for code to find it with
    key = "mcjokers",
    -- The name of the file, for the code to pull the atlas from
    path = "mcjokers.png",
    -- Width of each sprite in 1x size
    px = 71,
    -- Height of each sprite in 1x size
    py = 95
}

SMODS.Sound:register_global()

SMODS.Joker {
    key = 'creeper',
    loc_txt = {
        name = 'Creeper',
        text = {"{C:mult}X#1#{} Mult", "{C:red,E:2}self destroys{}"}
    },
    config = {
        extra = {
            Xmult = 7 -- ref: blast radius of creeper
        }
    },
    loc_vars = function(self, info_queue, card)
        return {
            vars = {card.ability.extra.Xmult}
        }
    end,
    rarity = 2,
    atlas = 'mcjokers',
    pos = {
        x = 0,
        y = 0
    },
    cost = 6,
    calculate = function(self, card, context)
        if context.joker_main then
            -- Tells the joker what to do. In this case, it pulls the value of mult from the config, and tells the joker to use that variable as the "mult_mod".
            return {
                Xmult_mod = card.ability.extra.Xmult,
                -- This is a localize function. Localize looks through the localization files, and translates it. It ensures your mod is able to be translated. I've left it out in most cases for clarity reasons, but this one is required, because it has a variable.
                -- This specifically looks in the localization table for the 'variable' category, specifically under 'v_dictionary' in 'localization/en-us.lua', and searches that table for 'a_mult', which is short for add mult.
                -- In the localization file, a_mult = "+#1#". Like with loc_vars, the vars in this message variable replace the #1#.
                message = localize {
                    type = 'variable',
                    key = 'a_xmult',
                    vars = {card.ability.extra.Xmult}
                }
                -- Without this, the mult will stil be added, but it'll just show as a blank red square that doesn't have any text.
            }
        end

        if context.end_of_round and not context.repetition and context.game_over == false and not context.blueprint then
            -- This part plays the animation.
            G.E_MANAGER:add_event(Event({
                func = function()
                    play_sound('mc__random__explode')
                    card.T.r = -0.2
                    card:juice_up(0.3, 0.4)
                    card.states.drag.is = true
                    card.children.center.pinch.x = true
                    -- This part destroys the card.
                    G.E_MANAGER:add_event(Event({
                        trigger = 'after',
                        delay = 0.3,
                        blockable = false,
                        func = function()
                            G.jokers:remove_card(card)
                            card:remove()
                            card = nil
                            return true;
                        end
                    }))
                    return true
                end
            }))

            return {
                message = 'Oh no!'
            }
        end
    end
}
