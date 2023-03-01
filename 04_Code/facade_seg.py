from keras_segmentation.models.unet import vgg_unet
import numpy as np 
import pandas as pd

print("test22")

model = vgg_unet(n_classes=12 ,  input_height=416, input_width=608  )

model.train(
    train_images =  "./content/images_prepped_train/",
    train_annotations = "./content/label/",
    checkpoints_path = "./tmp/vgg_unet_2", 
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