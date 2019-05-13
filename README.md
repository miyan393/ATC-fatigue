# Eye Blink Detector (疲劳眨眼检测)

此项目基于CAFUC的空管人员人因工程疲劳检测项目，主要采用卷积神经网络对眼睛睁闭状态进行判断，用于疲劳检测

- 检测眼睛睁开或者闭合

- 可以在视频中实时检测

- mtcnn_eye_dtection.py 用于采集眼部和嘴部等部位的图像，可用于数据集的建立和实时检测阶段的部位提取

  blink-detection.ipynb ,blink-detection1.ipynb 是针对不同输入大小的模型训练文件

  picture_test.ipynb 用于单张图片检测

  video_test 用于视频检测

## Dependencies(需要的库)
- Python 3+
- Keras
- numpy
- matplotlib (for visualization)
- OpenCV (for visualization)
- mtcnn 

在测试中，需要安装dlib的人脸识别库文件，点此链接下载 [here](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2)



# demo()

运行 blink-detection或blink-detection1 或来构建模型,运行video_test 来进行实时检测

run:

 `blink-detection1.ipynb`

run:
 `video_test.py`



