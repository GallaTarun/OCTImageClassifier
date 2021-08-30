from django.shortcuts import render,redirect
import os
from . import forms
import numpy as np
import tensorflow as tf
import keras
from tensorflow.keras.models import load_model
import shutil
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def index(request):
    form = forms.InputForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request,'PredictionApp/index.html',context=context)


def predict(request):
    submitbutton = request.POST.get("submit")
    form = forms.InputForm(request.POST or None)
    file_path = ""
    prediction = []
    label = ""
    if form.is_valid():
        # obtain the entered file path
        file_path = form.cleaned_data.get("image_path")
        # preprocessing part ...
        test_data_dir = os.getcwd()+'\Test_Data'
        cnv_dir = test_data_dir + '\CNV'
        # Moving the image from entered location to cnv folder
        shutil.copy(file_path,cnv_dir)
        # renaming the image file to oct_image_n.jpeg
        file_name = file_path.split('\\')[-1]
        source = test_data_dir+'\CNV\\'+file_name
        dest = cnv_dir+'\oct_image_'+str(len(os.listdir(cnv_dir)))+'.jpeg'
        os.rename(source,dest)
        # preprocessing the image using ImageDataGenerator        
        ts_gen = ImageDataGenerator(rescale=1.0/255.0)
        test_data = ts_gen.flow_from_directory(test_data_dir,color_mode='rgb',target_size=(224,224),batch_size=1)
        # loading the model and obtain the prediction for the image
        model = load_model(os.getcwd()+'/Prediction model')
        # obtaining the predictions
        prediction = model.predict_generator(test_data)
        # preparing predicted label
        class_indices = {0:'CNV',1:'DME',2:'DRUSEN',3:'NORMAL'}
        prediction = [round(val,2) for val in prediction[-1]]
        max_acc = round(max(prediction)*100,2)
        label = class_indices[np.argmax(prediction)]
    
    # context dictionary    
    dic = {
        'form' : form,
        'submitbutton' : submitbutton,
        # 'path' : 'oct_image_'+str(len(os.listdir(cnv_dir)))+'.jpeg',
        'path' : file_path, 
        'prediction': prediction,
        'label' : label,
        'acc': max_acc,
    }
    
    return render(request,'PredictionApp/predict.html',context=dic)


def about_us(request):
    return render(request,'PredictionApp/about_us.html',context={})

def architecture(request):
    return render(request,'PredictionApp/architecture.html',context={})