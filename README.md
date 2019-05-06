# Generative Computergrafik

### Raytracer
*A simple recursive raytracer with Phong-shading.*


<br/>

##### Prerequisites 

1. Python 3
2. Pillow
3. PIL
4. NumPy

##### Execution

Simply run `python3 render.py`. Will render the scene as a JPEG image.

<br/>

Available arguments:

`-res=WIDTH,HEIGHT`: set the resolution of the output image
    
`-quality=`: set the quality of the output image; default value is 75
    
`-ftype=STR`: set the file type of the output image; default value is JPEG; for a list of supported filetypes please refer to PIL.Image documentation
    
`-dirout=PATH`: set the directory of the output image
    
`-processes=INT`: set the number of parallel running processes for multicore performance
    
`-noshow`: set, to not display the image after succesful renderering process
    
`-export`: set, to not display the image after succesful renderering process
    
`-reflection=FLOAT`: set the reflectiveness of materials; best results can be achieved when staying in the range of 0.1 to 0.5
    
`-rdepth=INT`: set the maximum recursion depth for tracing reflected rays
    
`-lightintensity=INT`: set the intensity of the light source

`-lightpos=[X,Y,Z]`: a vector with the coordinates of the light source

`-lightcolor=(RGB)|<color-name>`: the rgb color value of the light source
    
`-spherecolors=(<color-left>,<color-top>,<color-right>)`: set the colors for each sphere

`-floormat=[(RGB),AMBIENT,DIFFUSE,SPECULAR]|[MATERIAL]`: set the material for the floor    
- RGB: a rgb color value <br/>
- AMBIENT: float from 0.0 to 1.0 <br/>
- DIFFUSE: float from 0.0 to 1.0 <br/>
- SPECULAR: float from 0.0 to 1.0 <br/>

>If you are interested in what these values AMBIENT, DIFFUSE and SPECULAR mean and do please refer to the Phong-Shading wiki.







