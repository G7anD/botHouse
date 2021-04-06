import numpy as np
from PIL import Image
from ISR.models import RRDN, RDN

name = None
rdn = RDN(arch_params={'C':6, 'D':20, 'G':64, 'G0':64, 'x':2})
rdn.model.load_weights('./models/noise.hdf5')

while name!="q":
    name = input('Nomini kiriting: ')
    img = Image.open(name)
    lr_img = np.array(img)
    sr_img = rdn.predict(lr_img, by_patch_of_size=50)
    imga = Image.fromarray(sr_img)
    imga.save("enhanced_"+name)



def get_photo_url(url):
    r = requests.get(url)

    response = requests.post(
            'https://telegra.ph/upload',
            files={'file': ('file', r.content, 'image/jpg')}
        )
    return response.json()