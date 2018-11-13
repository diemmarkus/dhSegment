
from dh_segment.post_processing.PAGE import Region, TextRegion, SeparatorRegion, Point

def download_images_using_csv(csvPath: str, outDir: str):
    import os
    from joblib import Parallel, delayed
    from tqdm import tqdm

    from dh_segment.utils import download_image

    if not csvPath:
        print('csv path is empty, please specify the path to a valid csv file')
        return
        
    elif not os.path.exists(csvPath):
        print(csvPath, 'does not exist...')
        return

    # parse the csv
    data = read_csv(csvPath)
    
    # make image urls unique
    lu = list(set(data))

    print('downloading', len(lu), 'images')

    Parallel(n_jobs=10)(delayed(download_image)(e.url, outDir, filename_from_url(e.url)) for e in tqdm(lu, desc='downloading'))

    # the simple solution:
    # for e in lu:
    #     if not download_image(e.url, outDir):
    #         print('could not download: ' + e.url)

    print('hey, ho - i am done downloading', str(len(lu)), 'images...')

def create_page_xmls(csvPath: str, outDir: str):
    from dh_segment.post_processing.PAGE import Page
    import os
    from imageio import imread

    if not csvPath:
        print('csv path is empty, please specify the path to a valid csv file')
        return

    elif not os.path.exists(csvPath):
        print(csvPath, 'does not exist...')
        return

    # parse the csv
    data = read_csv(csvPath)

    # make image urls unique
    lu = list(set(data))

    for e in lu:

        fname = filename_from_url(e.url)
        ca = list(filter(lambda x: x.url == e.url, data))

        # convert to PAGE TextRegions
        trs = [(lambda re: re.toTextRegion())(re)       for re in ca]
        sps = [(lambda re: re.toSeparatorRegion())(re)  for re in ca]
        lsps = [(lambda re: re.toLeftSeparatorRegion())(re) for re in ca]

        # load the image
        imgPath = os.path.join(outDir, fname)
        
        if os.path.exists(imgPath):

            try:
                img = imread(imgPath)
                imgShape = img.shape
            except:
                print('error while loading', imgPath)

        else:
            print('sorry, I could not find', imgPath)
            imgShape = (0, 0)

        pname = filename_from_url(e.url, '.xml')
        pageXml = Page(text_regions=trs, separator_regions=sps+lsps,
                    image_width=imgShape[1], 
                    image_height=imgShape[0], 
                    image_filename=fname)
        
        pageXml.write_to_file(os.path.join(outDir, pname))

        print(fname, '(', imgShape[1], 'x', imgShape[0], ') has', len(ca), 'articles')


def filename_from_url(url: str, ext: str = '') -> str:

    us = url.split('/')
    nIdx = us.index('image')+1

    if not ext:
        ext = '.' + us[-1].split('.')[1]

    # create filename with extension
    filename = us[nIdx] + ext
    
    return filename


def read_csv(csvPath: str):
    import csv

    with open(csvPath, "r", encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=";")

        header = ()
        entries = list()

        for row in reader:

            if not header:
                header = row
                continue
            re = RegionEntry(row[header.index('page_url')], 
            row[header.index('region')])
            entries.append(re)

        return entries

class RegionEntry:
    
    def __init__(self, url: str, regionStr: str):
        self.url = url
        self.region = Region().from_rect_str(regionStr)

    def __eq__(self, other) -> bool:

        if isinstance(other, str):
            return self.url == str

        return self.url == other.url

    def __hash__(self):
        import zlib
        
        return zlib.crc32(self.url.encode())
   
    def toSeparatorRegion(self):
        
        if len(self.region.coords) < 4:
            return SeparatorRegion(self.region.id)

        p1 = self.region.coords[0]
        p2 = self.region.coords[3]

        cn = list()
        cn.append(Point(p1.y-20, p1.x))
        cn.append(Point(p2.y-20, p2.x))
        cn.append(Point(p2.y+20, p2.x))
        cn.append(Point(p1.y+20, p1.x))

        return SeparatorRegion(self.region.id, cn)

    def toLeftSeparatorRegion(self):

        if len(self.region.coords) < 4:
            return SeparatorRegion(self.region.id)

        p1 = self.region.coords[0]
        p2 = self.region.coords[1]

        cn = list()
        cn.append(Point(p1.y, p1.x-20))
        cn.append(Point(p2.y, p2.x-20))
        cn.append(Point(p2.y, p2.x+20))
        cn.append(Point(p1.y, p1.x+20))

        return SeparatorRegion(self.region.id, cn)


    def toTextRegion(self) -> TextRegion:
        return TextRegion(self.region.id, self.region.coords)
