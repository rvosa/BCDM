import sys
import argparse
from PIL import  Image, ImageDraw
import operator
import ujson as json
import requests
from io import BytesIO

#colour definition
purple = (255, 0, 255)
red = (255, 0, 0)
orange_red = (255, 50, 0)
yellow = (255, 255, 0)
orange = (255, 140, 0)

#size factor
def typeSizeFactor(i):
    msg = 'sizefactor: must be a number greater than or equal to 0.'
    if not isFloat(i):
        raise argparse.ArgumentTypeError(msg)
    iFloat = float(i)
    if iFloat < 0:
        raise argparse.ArgumentTypeError(msg)
    return iFloat

def typeCrop(i):
    if i[0] != '[' or i[-1] != ']':
        raise argparse.ArgumentTypeError('Coordinates must be placed between square brackets.')
    iSplit = i.strip().strip('[]').split(',')
    if len(iSplit) != 4:
        raise argparse.ArgumentTypeError('You must provide exactly 2 pairs of lattitude and longitude coordinates.')
    if not all(isFloat(x) for x in iSplit):
        raise argparse.ArgumentTypeError('A NAN was provided.')
    iFloats = list(float(x) for x in iSplit)
    if iFloats[0] > 90 or iFloats[0] < -90 or iFloats[2] > 90 or iFloats[2] < -90:
        raise argparse.ArgumentTypeError('Lattitude coordinates are not within the valid range.')
    if iFloats[1] > 180 or iFloats[1] < -180 or iFloats[3] > 180 or iFloats[3] < -180:
        raise argparse.ArgumentTypeError('Longitude coordinates are not within the valid range.')
    return iFloats

def typeAlpha(i):
    msg = 'Alpha factor must be an integer between 0 and 255.'
    if not isInt(i):
        raise argparse.ArgumentTypeError(msg)
    iInt = int(i)
    if iInt > 255 or iInt < 0:
        raise argparse.ArgumentTypeError(msg)
    return iInt

def typeIMFormat(i):
    msg = 'Must be either jpeg, png or gif.'
    iLower = i.lower()
    if iLower != 'jpeg' and iLower != 'png' and iLower != 'gif':
        raise argparse.ArgumentTypeError(msg)
    
    return iLower.lower()

def typeSortOrder(i):
    msg = 'Must be either lh or hl'
    iLower = i.lower()
    if iLower != 'lh' and iLower != 'hl':
        raise argparse.ArgumentTypeError(msg)
    return iLower

def typeDelimiter(i):
    msg = 'Must be either tab or comma.'
    iLower = i.lower()
    if iLower != 'tab' and iLower != 'comma':
        raise argparse.ArgumentTypeError(msg)
    if iLower == 'tab':
        return '\t'
    return ','



def logError(myString):
    print(myString, file=sys.stderr)
    exit(1)

def isFloat(i):
    try:
        float(i)
        return True
    except ValueError:
        return False

def isInt(i):
    try:
        int(i)
        return True
    except ValueError:
        return False

# rescales coordinates to pixel coordinates
def getLocationCoords(lat, lon, width, height):
    x = (lon + 180) * (width / 360)
    y = ((lat * -1) + 90) * (height / 180)
    return {
        'x': round(x),
        'y': round(y)
    }
    
    
def drawCircle(p, w, color, alpha):
    global drawImg
    halfW = round(w / 2)
    drawImg.ellipse((p['x'] - halfW, p['y'] - halfW, p['x'] + halfW, p['y'] + halfW), fill=(color[0], color[1], color[2], alpha), outline=(255, 52, 52, alpha))


parser = argparse.ArgumentParser(description = """Accepts a BCDM file through stdin and plots them on map. Reference basemaps: 
(233MP - https://bold-reference-files-public.us-east-1.linodeobjects.com/NE2_HR_LC_SR_W_21600.jpg), 
(58MP - https://bold-reference-files-public.us-east-1.linodeobjects.com/NE2_HR_LC_SR_W_10300.jpg),
(12.5MP - https://bold-reference-files-public.us-east-1.linodeobjects.com/NE2_HR_LC_SR_W_5000.jpg),
(1.6MP - https://bold-reference-files-public.us-east-1.linodeobjects.com/NE2_HR_LC_SR_W_1800.jpg) 
""")
parser.add_argument('--basemap', help='URL(must start with http(s)://) to basemap or local file')
parser.add_argument('--out', help='Path to output map image. Will be in JPG format unless specified.')
parser.add_argument('--sizefactor', help='Factor to scale circle size. Range between 0 and 1 - smaller to scale down. default is 1', type=typeSizeFactor, required=False, default=1)
parser.add_argument('--crop', help='Two latitude/longitude pairs to crop the image to. Place the coordinates in [] separated by commas.', type=typeCrop, required=False, default=None)
parser.add_argument('--alpha', help='Used in transpaprency of points. can be 0 - 255.', type=typeAlpha, required=False, default=255)
parser.add_argument('--imformat', help='Specify output image format. Can be jpeg, png or gif.', type=typeIMFormat, required=False, default='jpeg')
parser.add_argument('--sortorder', help='Order to layer the coordinates. Either lh (low on bottom and high on top) or hl (high on bottom and low on top).', type=typeSortOrder, required=False, default='hl')
parser.add_argument('--delimiter', help='Delimiter to separate data in input stream. Enter \'comma\'(default) or \'tab\'.', type=typeDelimiter, required=False, default='comma')
args = parser.parse_args()


try:
    #if the provided images is online
    if args.basemap.lower().startswith('http'):
        response = requests.get(args.basemap)
        inMapImg = Image.open(BytesIO(response.content))
    else:
        inMapImg = Image.open(args.basemap)
except:
    logError('mapin: Image could not be loaded. Check if it exists.')

sizeFactor = args.sizefactor
cropLocsFloat = args.crop
alphaFactor = args.alpha
imFormat = args.imformat
sortOrder = args.sortorder
delimiter = args.delimiter

outImg = inMapImg.copy()
inMapImg.close()
inWidth = inMapImg.width
inHeight = inMapImg.height

# sets up drawing to output image
drawImg = ImageDraw.Draw(outImg, 'RGBA')


#Process coordinates
coordsCount = dict()
# sys.stdin.readline()

encountered_processids={}
for line in sys.stdin:
    row=json.loads(line)
    
    coord=row.get("coord",[])
    
    if coord!=None and len(coord)==2 and row["processid"] not in encountered_processids:
        key = "|".join([f"{c:.3f}" for c in coord])
     
        coordsCount.setdefault(key,0) 
        coordsCount[key] +=1

        encountered_processids[row["processid"]]=True

sortCoordsCount = list(coordsCount.items())
if sortOrder == 'lh':
    sortCoordsCount = sorted(coordsCount.items(), key=operator.itemgetter(1), reverse=False)
elif sortOrder == 'hl':
    sortCoordsCount = sorted(coordsCount.items(), key=operator.itemgetter(1), reverse=True)


#Rasterize points
for coord in sortCoordsCount:
 
    lat, lon = coord[0].split('|')
    lat = float(lat)
    lon = float(lon)
    point = getLocationCoords(lat, lon, inWidth, inHeight)
    count = int(coord[1])

    if count >= 10000:
        drawCircle(point, 60 * sizeFactor, purple, alphaFactor)
    elif count >= 1000:
        drawCircle(point, 60 * sizeFactor, red, alphaFactor)
    elif count >= 100:
        drawCircle(point, 40 * sizeFactor, orange_red, alphaFactor)
    elif count >= 10:
        drawCircle(point, 24 * sizeFactor, orange, alphaFactor)
    elif count >= 1:
        drawCircle(point, 12 * sizeFactor, yellow, alphaFactor)

#crop to a region if defined
if cropLocsFloat is not None:
    p1 = getLocationCoords(cropLocsFloat[0], cropLocsFloat[1], inWidth, inHeight)
    p2 = getLocationCoords(cropLocsFloat[2], cropLocsFloat[3], inWidth, inHeight)
    outImg.crop((min(p1['x'], p2['x']), min(p1['y'], p2['y']), max(p1['x'], p2['x']), max(p1['y'], p2['y']))).save(args.out, format=imFormat)


#save output
else:
    outImg.save(args.out, format=imFormat)


outImg.close()
