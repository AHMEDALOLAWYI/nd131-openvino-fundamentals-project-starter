# Project Write-Up

## Explaining Custom Layers
The process behind converting custom layers involves...
Some of the potential reasons for handling custom layers are...

There is a list of known layers . Loading models inside OpenVINO application may result in functions that have different operations such as loss functions. This will result in the custom layers contained in the topology and not included in the in known layers are classified  as custom by the model optimizer because each supported framework has its own list of known layers.

The model optimizer convert pre-trained models to feed them to the inference engine in the intermediate representation form . The original framework can be Tensorflow, MXNet or Caffe. Hence, conversion is done via adding an extension to both the model optimizer and the inference engine during implementation custom layer of the model used. To register custom layer each supported framework is registered via its unique steps.

In our model , tensorflow object detection model zoo is used and tensorflow layers are supported by the model optimizer so there is no actual need to handle any custom layers in this project as tensorflow model achieve suitable direct intermediate representation and does not present any unsupported layers at the time of the inference.

## Comparing Model Performance
The criteria used in order to compare model performance was based on accuracy, size of the model and inference time . 

For accuracy the deploying of the model from the model zoo  and using the openvino tool kit and converted TensorFlow model achieved better accuracy than just using opencv library and python environment to accomplish people counting. For example converted model and model zoo while inference using OpenVINO was faster in detecting. However, all model correctly detected the number of people signing up the sheet. 

The model size after conversion was 65.3 MB and before conversion 64.8 MB so there is a small difference between two sizes . It is noticed that the IR OpenVINO achieved smaller size which is ideal for internet of things devices to implement in due to memory restrictions. 

In terms of inference time the mode from the open model zoo had less time than both the converted model and the opencv using python . This due to the fact that the model from open model zoo was built specifically to function on the OpenVino toolkit with no conversion needed . By running the application without using the toolkit the average inference time was 139.40 second and while using the toolkit the average infernce time was found to be 90.2 seonds 


## Assess Model Use Cases
Some of the potential use cases of the people counter app are : There are many areas where a person detection/counting model can be used 
1-For retail people  counting model can play a role in protection against theft, understand peak times optimize store layout and organised merchandise in aisles.Hence, this model can assist the retail store in marketing , queue management and staffing. 

2-For safety the people for example during covid-19 the stores can allow certain number of people entrance to the store to avoid crowding within the stores . Also it can be used in high risk areas where only certain number of people is allowed to be inside for example to allow easy evacuation such as confined spaces to determine and check the number of staff who got inside the confined space. 

3-For infrastructure planning the model will allow us to understand how crowded are public places at a given time or how many people are using a particular street crossing everyday.  

Each of these use cases would be useful because using the counting model we are able to get results about number of people count and duration that people spent in certain places, also we can define a specific time that the model count for example in bus doors the doors can be shut automatically after the specified time is over and by using a threshold for a specific number of people for example in case of elevator that the elevator give an alarm once the total number of people has been exceeded. 
   


## Assess Effects on End User Needs
 Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. The potential effects of each of these are as follows...

Image size:There is a proportional relationship between image size and image resolution. The output result for a model with higher resolution will be much better. In contrast a model with less resolution will give less accurate results but will consume less memory size. Hence, depending on the specifications of the machine the end user is operating the results will differ so the end user can account for some delay with more accurate results for an image with higher resolution and bigger image size. 

Lighting : Good predictions require a place with good lighting provided and to enhance our results dark areas will result in less accurate results. 

Model Accuracy : less accurate models will result in more invalid predictions and counting as the end user deals with an application that is deployed for real time results we will require higher model accuracy for much accurate outcomes. 

Camera focal length: depending of the size of the place monitored by the camera  we can decide whether we look for a camera with high focal length or low focal length. This is because a high focal length will result in narrow angle image and focus on specific object. On the other hand a camera with low focal length will result in a wider angle . So a wider place will require high focal camera length but this will give less extracted information about objects in camera.

## Model Research.......
In order to get the application running I used two different models . One that is available from open-vino pre-trained models and the other one is MobileNetSSD. For the purpose of the write up for this project for the openvnino model I used the toolkit to deploy it while for the MobileNetSSD I used my local machine to inference with opencv2. Hence , we will compare elapsed time and approximate fps for MobileNetSSD model while for openvino pre-trained model a study will be conducted on .....

In investigating potential people counter models, I tried each of the following two models:

- Model 1: [MobileNetSSD]
  - [Model Source]:https://drive.google.com/file/d/0B3gersZ2cHIxRm5PMWRoTkdHdHc/view
  I did not convert this model into intermediate representartion instead I was trying to get results by doing inference only on opencv2 and python environment on my loacal machine. 
  
  The results for this model were elapsed time of 32.63 and approximate 42.72 FPS . 
  To get the output video I run the following command: 
  
  python people_counter.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt \
	--model mobilenet_ssd/MobileNetSSD_deploy.caffemodel \
	--input videos/Pedestrian_Detect_2_1_1.mp4 --output output/output_01.avi
 
 
 The result for the output video can be found here :  https://www.dropbox.com/s/bsi46q683l8e9ub/output_02.avi?dl=0
 
  
- Model 2: The model is converted using the openvnio toolkit and the inference is done through openvino 
In order to feed the model the inference engine we have to converte it to the intermediate representation (IR) . Here we are using SSD MobileNet V2 COCO from Tensorflow. Firstly we download the model in the workspace by using the following command: 

wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
 
 Next tp the download of the model to the workspace , it has to be extracted using the follwoing command: 
 
 tar -xvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz 
 
Following extacting the files we generate our xml file and bin file using the following command: 

python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json

Once we success converting our model succeeded a message will be shown stating there are two files generated which are xml file and bin file also the time it took around 72.00 seconds to achieve the conversion process.  

- Model 3: person-detection-retail-0013

  - This model was obtained from Model zoo pre-trained models 
  - There was no need to convert the model as it was downloaded from the intel website. 
  - The model was good enough to count total people in frame , find average duration and working well on edge as well as cloud. 
  - It could be possible to improve the model accuracy and performance by running it on GPU or higher generation hardware. 
  The video output when running on my local machine gave an output of 0.17 seconds avg time and 6 totla of people count please check vido on dropbox for running on UI https://www.dropbox.com/s/jh88fxzakfzjnlh/VID_20200618_113815.mp4?dl=0

