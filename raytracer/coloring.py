from raytracer.objects import CheckerBoard, Color, Material


# colors START

black = Color(0, 0, 0)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(0, 0, 255)
white = red + green + blue
yellow = red + green
grey = Color(100, 100, 100)
standard = Color()
dark_grey = Color(79, 79, 79)

# colors END

#################################

# materials START

ambi = .4
diff = .9
spec = .0
red_mat = Material(red, ambLvl=ambi, diffLvl=diff, specLvl=spec, surface=5)
green_mat = Material(green, ambLvl=ambi, diffLvl=diff, specLvl=spec, surface=5)
blue_mat = Material(blue, ambLvl=ambi, diffLvl=diff, specLvl=spec, surface=5)
yellow_mat = Material(yellow, ambLvl=ambi, diffLvl=diff, specLvl=spec, surface=30)
black_mat = Material(black, ambLvl=ambi, diffLvl=diff, specLvl=spec, surface=30)
white_mat = Material(white, ambLvl=ambi, diffLvl=diff, specLvl=spec, surface=30)
dark_grey_mat = Material(dark_grey, ambLvl=ambi, diffLvl=diff, specLvl=spec, surface=30)

# materials END

#################################

# textures START

checkerboard_tex = CheckerBoard(size=8, first=black_mat, second=white_mat,
								ambLvl=1.0, diffLvl=0.4, specLvl=1, surface=0)

# textures END
