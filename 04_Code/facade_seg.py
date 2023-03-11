from keras_segmentation.models.pspnet import resnet50_pspnet
import numpy as np 
import pandas as pd

print("test22")

model = resnet50_pspnet(n_classes=12 ,  input_height=384, input_width=576  )

model.train(
    train_images =  "./content/images_prepped_train/",
    train_annotations = "./content/label/",
    checkpoints_path = "./tmp/resnet50_pspnet_1", 
    steps_per_epoch=2048,
    auto_resume_checkpoint=True,
    epochs=15
)

out = model.predict_segmentation(
    inp="./content/images_prepped_train/cmp_b0025.jpg",
    out_fname="./tmp/out.png"
)

# import matplotlib.pyplot as plt
# plt.imshow(out)

# evaluating the model 
print(model.evaluate_segmentation( inp_images_dir="./content/images_prepped_train/"  , annotations_dir="./content/annotations_prepped_train/" ) )