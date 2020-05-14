# Project Write-Up

You can use this document as a template for providing your project write-up. However, if you
have a different format you prefer, feel free to use it as long as you answer all required
questions.

## Explaining Custom Layers
The process behind converting custom layers involves...
Some of the potential reasons for handling custom layers are...

There is a list of known layers . Loading models inside OpenVINO application may reuslt in functions that have different operations such as loss functions. This will result in the custom layers contained in the topoloy and not included in the in known layers are calssfied as custom by the model optimizer because each supported framework has its own list of knownlayers.

The model optimizer convert pre-trained models to feed them to the inference engine in the intermediate represenation form . The orignal framework can be Tensorflow, MXNet or Caffe. Hence, conversion is done via adding an extension to both the model optimiser and the inference engine during iplementatin custom layer of the model used. To register custom layer each supported framework is registered via its unique steps.

In our model , tensorflow object detection model zoo is used and tensorflow layers are supported by the model optimiser so there is no actual need to handle any custome layers in this project as tensorflow model achieve suitable direct intermediate reprenesaion and does not present any unsupported layers at the time of the inference. 

 

## Comparing Model Performance

My method(s) to compare models before and after conversion to Intermediate Representations
were...

The difference between model accuracy pre- and post-conversion was...

The size of the model pre- and post-conversion was...

The inference time of the model pre- and post-conversion was...

## Assess Model Use Cases

Some of the potential use cases of the people counter app are : 
There are many areas where a person detection/counting model can be used : 

For retail people  couting model can play a role in protection against theft, understand peak times optimise store layout and organise merchandise in aisles.Hence, this model can assist the retail store in marketing , queue managment and staffing. 

For safety the poople for example during covid-19 the stores can allow certain number of people entrance to the store to avoid crowding within the stores . Also it can be used in high risk areas where only certain number of peopel is allowed to be inside for example to allow easy evacuation such as condfined spaces to determine and check the number of staff who got inside the confied space. 

For infrastructure palnning the model will allow us to understand how crowded are public places at a given time or how many people are using a particular street crossing everyday.  

Each of these use cases would be useful because...
By using the counting model we are able to get results about number of people count and duration that people spent in certain places, also we can define a spefic timw rhat the model count for example in bus doors the doors can be shut autotically after the specifided time is over and by using a threshold for a specific number of people for example in case of elevator that the elvevator give an alarm once the totoal number of people has been exceeded. 
   
## Assess Effects on End User Needs

Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. The potential effects of each of these are as follows...

## Model Research

[This heading is only required if a suitable model was not found after trying out at least three
different models. However, you may also use this heading to detail how you converted 
a successful model.]

In investigating potential people counter models, I tried each of the following three models:

- Model 1: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
  
- Model 2: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...

- Model 3: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
