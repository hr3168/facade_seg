from keras_segmentation.models.unet import resnet50_pspnet
import numpy as np 
import pandas as pd
import os
import pdb
from keras_segmentation.predict import model_from_checkpoint_path
from keras_segmentation.models.unet import unet_mini
from keras_segmentation.models.model_utils import transfer_weights

arcade_seg = resnet50_pspnet(n_classes=15 ,  input_height=416, input_width=608  )

# pdb.set_trace()

model_origin = model_from_checkpoint_path( "D:\HKUST\\00_Work\\04_Facade\\facade_seg\\04_Code\\tmp\\resnet50_pspnet_1" )

transfer_weights( model_origin , arcade_seg  ) 

# pdb.set_trace()

arcade_seg.train(
    train_images =  "./qilou_dataset/image/",
    train_annotations = "./qilou_dataset/anote/",
    checkpoints_path = "./qilou_seg/resnet50_pspnet_1" , 
    steps_per_epoch=2048,
    auto_resume_checkpoint=True,
    epochs=15
)

out = arcade_seg.predict_segmentation(
    inp="./qilou_dataset/image/Snipaste_2023-02-21_12-13-00.png",
    out_fname="./qilou_seg/out_1.png"
)

'''
 python -m keras_segmentation predict --checkpoints_path="D:\HKUST\00_Work\04_Facade\facade_seg\04_Code\qilou_seg\resnet50_pspnet_2" --input_path="D:\HKUST\00_Work\04_Facade\facade_seg\04_Code\content\T_001.jpg" --output_path="D:\HKUST\00_Work\04_Facade\facade_seg\04_Code\qilou_seg\T001.png"
 '''