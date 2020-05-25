# Project Write-Up

## Explaining Custom Layers
The process behind converting custom layers involves...
Some of the potential reasons for handling custom layers are...

There is a list of known layers . Loading models inside OpenVINO application may reuslt in functions that have different operations such as loss functions. This will result in the custom layers contained in the topoloy and not included in the in known layers are calssfied as custom by the model optimizer because each supported framework has its own list of knownlayers.

The model optimizer convert pre-trained models to feed them to the inference engine in the intermediate represenation form . The orignal framework can be Tensorflow, MXNet or Caffe. Hence, conversion is done via adding an extension to both the model optimiser and the inference engine during iplementatin custom layer of the model used. To register custom layer each supported framework is registered via its unique steps.

In our model , tensorflow object detection model zoo is used and tensorflow layers are supported by the model optimiser so there is no actual need to handle any custome layers in this project as tensorflow model achieve suitable direct intermediate reprenesaion and does not present any unsupported layers at the time of the inference. 

 

## Comparing Model Performance.........

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

Image size:There is a proportional relationship between iamge size and image resolution. The output result for a model with higher resolution will be much better. In contrast a mdoel with less resoultion will give less acccurate results but will consume less memory size. Hence, depending on the specfications of the machine the end eser is operating the results will differ so the end user cana accout for some delay with more accurate results for an image with higher resoltion and bigger image size. 

Lighting : Good predeictions require a place with good lighting provided and to enhance our results dark areas will reuslt in less accurate results. 

Model Accuracy : less accurate models will result in more invalid predictions and coutings as the end user deals with an application that is deployed for real time results we will requrie higher model accuracy for much accurate outcomes. 

Camera focal length: depending of the size of the place monitored by the cammera  we can decide wether we look for a camera with high focal lenght or low focal length. This is becuase a high focal lenght will result in narrow angle image and focus on spesfic object. On the other hand a camere with low focal length will result in a wider angle . So a wider place will require high focal cammera length but this will give less exctracted information about objects in camera. 

## Model Research.......
In order to get the application running I used two different models . One that is avaible from open-vino pretrained models and the other one is MobileNetSSD. For the purpose of the write up for this project for the openvnino model I used the toolkit to deploy it while for the MobileNetSSD I used my local machine to inference with opencv2. Hence , we will compare elapsed time and approximate fps for MobileNetSSD model while for openvino pretrained model a study will be conducted on .....

In investigating potential people counter models, I tried each of the following two models:

- Model 1: [MobileNetSSD]
  - [Model Source]:https://drive.google.com/file/d/0B3gersZ2cHIxRm5PMWRoTkdHdHc/view
  I did not convert this model into intermediate representartion instead I was trying to get results by doing inference only on opencv2 and python environment on my loacal machine. 
  
  The results for this mdoel were elapsed time of 32.63 and approximate 42.72 FPS . 
  To get the output video I run the following command: 
  
  python people_counter.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt \
	--model mobilenet_ssd/MobileNetSSD_deploy.caffemodel \
	--input videos/Pedestrian_Detect_2_1_1.mp4 --output output/output_01.avi
 
 
 The result for the output video can be found here :  https://www.dropbox.com/s/bsi46q683l8e9ub/output_02.avi?dl=0
 
  
- Model 2: The model is coverted using the openvnio toolkit and the inference is done through openvino 
In order to feed the model the inference engine we have to converete it to the intermediate representation (IR) . Here we are using SSD MobileNet V2 COCO from Tensorflow. Firstly we download the model in the workspace by using the following command: 

wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
 
 Next tp the download of the model to the workspace , it has to be extracted using the follwoing command: 
 
 tar -xvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz 
 
Following extacting the files we generate our xml file and bin file using the following command: 

python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json

Once we success converting our model succedded a message will be shown stating there are two files generated which are xml file and bin file also the time it took around 72.00 seconds to acheive the conversion process.  


  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...

- Model 3: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
