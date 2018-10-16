from dh_segment.post_processing.PAGE import Region

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

    Parallel(n_jobs=10)(delayed(download_image)(e.url, outDir) for e in tqdm(lu, desc='downloading'))

    # the simple solution:
    # for e in lu:
    #     if not download_image(e.url, outDir):
    #         print('could not download: ' + e.url)

    print('hey, ho - i am done downloading', str(len(lu)), 'images...')

# def create_page_xmls(csvPath: str, outDir: str):

#     # parse the csv
#     data = read_csv(csvPath)

#     # make image urls unique
#     lu = list(set(data))




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
        self.Region = Region().from_str(regionStr)

    def __eq__(self, other) -> bool:
        return self.url == other.url

    def __hash__(self):
        import zlib
        
        return zlib.crc32(self.url.encode())
