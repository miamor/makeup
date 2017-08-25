# makeup

## Prerequisites
dlib   
openface   
flask (optional, for running server)   

## To train:
1. Delete ./data/generated-embeddings and ./data/aligned-images
2. Run these commands from terminal:
`./util/align-dlib.py ./data/training-images/ align outerEyesAndNose ./data/aligned-images/ --size 96`
`./batch-represent/main.lua -outDir ./data/generated-embeddings/ -data ./data/aligned-images/`
`./demos/classifier.py train ./data/generated-embeddings/`   

## Test with your data
`./demos/classifier.py infer ./data/generated-embeddings/classifier.pkl ./data/shane.jpg`  

### Run test from server
To run test from server, you must have flask installed, and run from virtualenv.
Activate server:
`python server.py`
Your server will run at http://127.0.0.0:5000   
Go to http://127.0.0.1:5000/detect_face_shape/shane/ to test or http://127.0.0.1:5000/detect_face_shape/<image_name>/   
whereas ./data/<image_name> is your test image to classify
