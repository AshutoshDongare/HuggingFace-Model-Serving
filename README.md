# HuggingFace-Model-Serving
Quick and easy tutorial to serve HuggingFace sentiment analysis model using torchserve

Full explanation of all possible configurations to serve any type of model can be found at [Torchserve Github](https://github.com/pytorch/serve)  

However, This tutorial can help you to get started quickly on serving your models to production.
we will be using a pretrained huggingface model ``` distilbert-base-uncased-finetuned-sst-2-english ``` for serving.

This model is finetuned for Text Classification (sentiment analysis) task. It is available on [HuggingFace](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)

## Dependencies Installation 

We will require following components available for serving. It is a good idea to create and activate a python virtual environment with name of your choice before installing python dependencies. We may want to call it "torchserve" as an environment.

- [JDK 11](https://www.oracle.com/in/java/technologies/javase/jdk11-archive-downloads.html) 
  You may need to sign up to oracle to download archived version of JDK to be able to download and install
  Torchserve uses JDK for HTTP server support.

- [pytorch](https://github.com/pytorch/serve/blob/master/README.md#serve-a-model)
  Install torchserve and related components using below command 

```
pip install torchserve torch-model-archiver torch-workflow-archiver
```

-[Transformers](https://huggingface.co/docs/transformers/index)
As we will be serving Transformer model, we will require to install Transformers using following command
```
pip install transformers
```

## Setup

We will first download the transformer model locally, then archive it to model archive file (.mar) and serve it using Torch Serve

- Step 1 - Lets create and change directory to a local folder named "sentiment_deployment".   
 
-Step 2  - Clone or download and extract serve repo to your machine from [Torch Serve repo](https://github.com/pytorch/serve). we  will require a couple of files from this repo. this will give you "serve-master" directory with all the artifacts. 

<span style="color:red">If you do not want to download all the files/repo from torch serve, you can download my repo that has only required files. In that case you can skip the steps 3,4 & 5 and directly continue with step 6</span> 

- Step 3 - copy following files from serve-master folder of serve repo to sentiment_deployment folder.
``` 
/serve-master/examples/Huggingface_Transformers/setup_config.json
/serve-master/examples/Huggingface_Transformers/Download_Transformer_models.py
/serve-master/examples/Huggingface_Transformers/Transformer_handler_generalized.py
/serve-master/examples/Huggingface_Transformers/Seq_classification_artifacts/index_to_name.json

```


- Step 4 - Edit ```setup_config.json``` to have following content. 
```
{
 "model_name":"distilbert-base-uncased-finetuned-sst-2-english",
 "mode":"sequence_classification",
 "do_lower_case":true,
 "num_labels":"2",
 "save_mode":"pretrained",
 "max_length":"128",
 "captum_explanation":false,
 "embedding_name": "distilbert",
 "FasterTransformer":false,
 "model_parallel":false
}

```
- Step 5 - Edit ```index_to_name.json``` to have following content. 
```
{
 "0":"Negative",
 "1":"Positive"
}

```

- Step 6 - Let's now download Transformer model using following command
```
python Download_Transformer_models.py
```
This will create a new folder ```Transformer_model``` under current directory & download transformer model mentioned in setup_config.json and  and all required artifacts

- Step 6 - Let's create Model Archieve (.mar) using following command. Please ensure that you have all the files at correct places. If you have followed the steps correctly then these files should be in correct places. 
```
torch-model-archiver --model-name distilBERTSeqClassification --version 1.0 --serialized-file Transformer_model/pytorch_model.bin --handler ./Transformer_handler_generalized.py --extra-files "Transformer_model/config.json,./setup_config.json,./index_to_name.json"
```

- Step 7 - Create a directory named ```model_store``` under current directory and move your new archived model file to this folder
```
mkdir model_store
mv distilBERTSeqClassification.mar model_store/ 

```
- Step 8 - This is the final step in serving the model. We will run torchserve as below
```
torchserve --start --model-store model_store --models sentiments=distilBERTSeqClassification.mar --ncs
``` 
If everything goes well, you should see a message like below in the terminal log
<span style="color:blue">Transformer model from path <your path> loaded successfully</span>

This confirms that you are now serving pretrained Huggingface sentiment analysis model as a REST API


# Running inference  

You can test the model inference that we just hosted as REST API

Quick way to do this is run below Curl command. Before you run below command you need to create a simple text file named ```sentiment.txt``` with one sentence that will be given for inference.
```
curl -X POST http://127.0.0.1:8080/predictions/sentiments -T sentiment.txt
```
You may as well write a simple python REST client to check model inference. I have added a simple REST API client code in this repo. In a new terminal with "torchserve" virtual environment activated,  Please run following client code to get model inference  

 ```
python /client/Sentiment_analysis_client.py
 
``` 

This should return the sentiment inference as Positive or Negative. 

Since this server is running locally and we are only running one sentence not the batch inference, the response time is extremely fast.

 
## Citations
 
This tutorial is curated list of steps from Torch Serve Github documentation. 
 
