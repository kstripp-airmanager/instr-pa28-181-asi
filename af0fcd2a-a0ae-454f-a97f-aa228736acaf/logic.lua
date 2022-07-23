-- AIRSPEED INDICATOR
-- based on logic from Florian Kleinau's PA28R-201 dual ASI, v1.00

as_card = img_add_fullscreen("gauge_card.png")

img_add_fullscreen("gauge_face.png")
as_needle =  img_add("needle.png",0,0,512,512)

prop_BG = user_prop_add_boolean("Background Display",true,"Display background?")
if user_prop_get(prop_BG) == false then
	img_add_fullscreen("bezel_min.png")
else
	img_add_fullscreen("bezel.png")
end	

img_add("airknobshadow.png",31,400,85,85)

local card = 0

AS_val = {0, 20, 40, 70, 110, 130, 150, 170, 190, 210, 230, 330}
AS_rot = {0, 0,  32, 95, 172, 209, 240, 270, 297, 332, 355, 455}

function sim_callback(speed)
    speed = var_cap(speed, 0, 330)
    for i = 2, #AS_val do
        if speed <= AS_val[i] then
            local rot = AS_rot[i-1] + (speed - AS_val[i-1]) / (AS_val[i] - AS_val[i-1]) * (AS_rot[i] - AS_rot[i-1])
            rotate(as_needle, rot)
            return
        end
    end
end

-- This function isn't setup yet.  FSX doesn't appear
-- to expose this value.  X-Plane might expose it as 
-- sim/aircraft/view/acf_asi_kts    int    y    enum    air speed indicator knots calibration
-- but I have not tested it.  For now, we just allow manual manipulation on the screen by 
-- clicking on the knob.
function calibration_callback(degrees)
    rotate(as_card, degrees)
end

function knob_callback(value)
    card = card + value
    card = var_cap(card, -90, 25)
    rotate(as_card, card)
end

-- DIALS ADD --
dial_knob = dial_add("airknob.png", 31, 395, 85, 85, knob_callback)
dial_click_rotate(dial_knob,6)

function knob_left()
	knob_callback(-1)
end
function knob_right()
	knob_callback(1)
end
si_command_subscribe("PA28_AIRSPEED_TAS_LFT",knob_left)
si_command_subscribe("PA28_AIRSPEED_TAS_RGT",knob_right)

xpl_dataref_subscribe("sim/cockpit2/gauges/indicators/airspeed_kts_pilot", "FLOAT", sim_callback)
fsx_variable_subscribe("AIRSPEED INDICATED", "Knots", sim_callback)
-- end AIRSPEED INDICATOR


-- Hardware --
dial_hw = hw_dial_add("TAS Dial", 5, knob_callback)
