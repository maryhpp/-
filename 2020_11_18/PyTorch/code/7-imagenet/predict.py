import torch
from PIL import  Image
from classes_name import classes
import torch.nn.functional as F
from torchvision import models,transforms
from torch.autograd import Variable

def classify(model,img):
    outputs=model(Variable(img))#.cuda()
    pred,ind=torch.max(F.softmax(outputs,dim=1).data,1)
    return pred.item(),ind.item()

#导入resnet50模型
model = models.resnet50(pretrained=False)

#使用GPU加速
#model=model#.cuda()

#模型进入验证状态
model.eval()

#加载预训练模型，download from https://download.pytorch.org/models/resnet50-19c8e357.pth
weight_path='resnet50.pth'
model.load_state_dict(torch.load(weight_path))

#图片预处理
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
  ])
img_path="car.jpg"
pil_img=Image.open(img_path)


img=preprocess(pil_img)#.cuda()
img=img.unsqueeze(0)
pred,ind=classify(model,img)
print("The probablity is :",pred)
print("The class belongs to :",classes[ind])