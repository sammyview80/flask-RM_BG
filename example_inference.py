from skimage import io
import torch, os
from PIL import Image
from briarmbg import BriaRMBG
from utilities import preprocess_image, postprocess_image
from huggingface_hub import hf_hub_download

def example_inference(im_path, transprent_bg=False):

    net = BriaRMBG()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = BriaRMBG.from_pretrained("briaai/RMBG-1.4")
    net.to(device)
    net.eval()    

    # prepare input
    model_input_size = [1024,1024]
    orig_im = io.imread(im_path)
    orig_im_size = orig_im.shape[0:2]
    image = preprocess_image(orig_im, model_input_size).to(device)

    # inference 
    result=net(image)

    # post process
    result_image = postprocess_image(result[0][0], orig_im_size)
    bgColor = (0,0,0, 0) if transprent_bg else (255,255,255, 255)
    # save result
    pil_im = Image.fromarray(result_image)
    no_bg_image = Image.new("RGBA", pil_im.size, bgColor)
    orig_image = Image.open(im_path)
    no_bg_image.paste(orig_image, mask=pil_im)
    no_bg_image.save("images/rm_image.png")
    return 'rm_image.png'