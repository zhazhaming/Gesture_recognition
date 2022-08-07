import torch.utils.data
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
import torch as nn

# 标准化
transform_BZ = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],  # 取决于数据集
    std=[0.229, 0.224, 0.225]
)

class LoadDate(Dataset):
    def __init__(self,txt_path,train_flag = True):
        self.img_info = self.get_imgs(txt_path)
        self.train_flag = train_flag

        self.train_tf = transforms.Compose([
            transforms.Resize(32),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.ToTensor(),
            transform_BZ
        ])
        self.val_tf = transforms.Compose([
            transforms.Resize(32),
            transforms.ToTensor(),
            transform_BZ
        ])

    def get_imgs(self,txt_path):
        with open(txt_path,'r',encoding='UTF-8') as f:
            imgs_info = f.readlines()
            imgs_info = list(map(lambda x:x.strip().split('\t'),imgs_info))
        return imgs_info

    def padding_black(self,img):
        w,h = img.size
        scale = 32/max(w,h)
        img_fg = img.resize([int(x) for x in [w*scale,h*scale]])
        size_fg = img_fg.size
        size_bg = 32
        img_bg = Image.new("RGB",(size_bg,size_bg))
        img_bg.paste(img_fg,((size_bg-size_fg[0])//2,
                             (size_bg-size_fg[1])//2))
        img = img_bg
        return img

    def __getitem__(self, index):
        img_path,label = self.img_info[index]
        img = Image.open(img_path)
        img = img.convert('RGB')
        img = self.padding_black(img)
        if self.train_flag:
            img = self.train_tf(img)
        else:
            img = self.val_tf(img)
        label = int(label)
        return img, label

    def __len__(self):
        return (len(self.img_info))

if __name__ == '__main__':
    train_dataset = LoadDate("train.txt",True)
    print("数据个数",len(train_dataset))
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                               batch_size=64,
                                               shuffle=True)
    for imge,label in train_loader:
        print(imge.shape)
        print(imge)
        print(label)
