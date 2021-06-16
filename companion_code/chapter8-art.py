import minecraft
import sys

mc = minecraft.Minecraft.create()

height = 10

start_x = 0
start_z = 0

canvas = "horizontal"

r = 246
g = 18
b = 22

picture = [["R", "R", "R"],
           ["G", "G", "G"],
           ["B", "B", "B"]]


if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        picture = f.readlines()

posn_z = start_x
for line in picture:
    posn_x = start_z
    for block in line:

        if canvas == "horizontal":
            x = posn_x
            y = height
            z = posn_z
        else:
            x = height
            y = posn_x
            z = posn_z

        if block == "R":
            mc.setBlock(x,y,z,r)
        if block == "G":
            mc.setBlock(x,y,z,g)
        if block == "B":
            mc.setBlock(x,y,z,b)
        posn_x = posn_x + 1
    posn_z = posn_z + 1

