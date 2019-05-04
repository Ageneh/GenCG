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
light_grey = Color(200, 200, 200)

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
grey_mat = Material(standard, ambLvl=ambi, diffLvl=diff, specLvl=spec, surface=30)
light_grey_mat = Material(light_grey, ambLvl=ambi, diffLvl=diff, specLvl=spec, surface=30)

# materials END

#################################

# textures START

checkerboard_tex = CheckerBoard(size=10, first=black_mat, second=white_mat,
								ambLvl=1.0, diffLvl=0.4, specLvl=1, surface=0)

# textures END


# CONTAINER

default_mat = checkerboard_tex.setsize(15)
materialsContainer = {
	"yellow": yellow_mat,
	"red": red_mat,
	"green": green_mat,
	"blue": blue_mat,
	"grey": grey_mat,
	"darkgrey": dark_grey_mat,
	"lightgrey": light_grey_mat,
	"black": black_mat,
	"white": white_mat,
	"checkerboard": checkerboard_tex,
	"checkers": checkerboard_tex,
	"": default_mat,
	None: default_mat,
	False: default_mat,
	True: default_mat,
}
