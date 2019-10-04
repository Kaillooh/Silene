import os.path
import random
from data.base_dataset import BaseDataset, get_params, get_transform
import torchvision.transforms as transforms
from data.image_folder import make_dataset
from PIL import Image


class AnimDataset(BaseDataset):
    """A dataset class for paired image dataset.

    It assumes that the directory '/path/to/data/train' contains image pairs in the form of {A,B}.
    During test time, you need to prepare a directory '/path/to/data/test'.
    """

    def __init__(self, opt):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseDataset.__init__(self, opt)
        print("ANIM DATASET IN DA PLACE !")
        self.dir_draw = os.path.join(opt.dataroot, "draw")
        print(self.dir_draw)
        self.draw_paths = sorted(make_dataset(self.dir_draw, opt.max_dataset_size))
        self.dir_vid = os.path.join(opt.dataroot, "vid")
        self.vid_paths = sorted(make_dataset(self.dir_vid, opt.max_dataset_size))

        self.phase = opt.phase
        self.vid_format = self.vid_paths[0].split(".")[-1]
        print("FORMAT", self.vid_format)

        # self.dir_AB = os.path.join(opt.dataroot, opt.phase)  # get the image directory
        # self.AB_paths = sorted(make_dataset(self.dir_AB, opt.max_dataset_size))  # get image paths
        print(self.draw_paths)
        print(self.vid_paths)
        assert(self.opt.load_size >= self.opt.crop_size)   # crop_size should be smaller than the size of loaded image
        self.input_nc = self.opt.output_nc if self.opt.direction == 'BtoA' else self.opt.input_nc
        self.output_nc = self.opt.input_nc if self.opt.direction == 'BtoA' else self.opt.output_nc

    def getTrainItem(self, index) :
        B_path = self.draw_paths[index]
        B = Image.open(B_path).convert('RGB')

        A_path = B_path.replace("/draw/", "/vid/")
        if self.vid_format == "png" :
            A_path = A_path.replace(".jpg", ".png")
        A = Image.open(A_path).convert('RGB')

        # apply the same transform to both A and B
        transform_params = get_params(self.opt, A.size)
        A_transform = get_transform(self.opt, transform_params, grayscale=(self.input_nc == 1))
        B_transform = get_transform(self.opt, transform_params, grayscale=(self.output_nc == 1))

        A = A_transform(A)
        B = B_transform(B)

        return {'A': A, 'B': B, 'A_paths': A_path, 'B_paths': B_path}

    def getTestItem(self, index) :
        A_path = self.vid_paths[index]
        A = Image.open(A_path).convert('RGB')

        # apply the same transform to both A and B
        transform_params = get_params(self.opt, A.size)
        A_transform = get_transform(self.opt, transform_params, grayscale=(self.input_nc == 1))

        A = A_transform(A)

        return {'A': A, 'B': A, 'A_paths': A_path, 'B_paths': A_path}


    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index - - a random integer for data indexing

        Returns a dictionary that contains A, B, A_paths and B_paths
            A (tensor) - - an image in the input domain
            B (tensor) - - its corresponding image in the target domain
            A_paths (str) - - image paths
            B_paths (str) - - image paths (same as A_paths)
        """
        
        if self.phase == "train" :
            return self.getTrainItem(index)
        else :
            return self.getTestItem(index)
        

    def __len__(self):
        """Return the total number of images in the dataset."""
        if self.phase == "train" :
            return len(self.draw_paths)
        else :
            return len(self.vid_paths)
