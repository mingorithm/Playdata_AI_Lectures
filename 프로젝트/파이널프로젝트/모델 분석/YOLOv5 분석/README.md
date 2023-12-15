# 1. YOLOv5란?

YOLOv5는 YOLO(You Only Look Once) 객체 탐지 시스템의 2020년에 나온 버젼으로 이미지 내의 객체를 탐지하는데 사용되는 실시간 딥러닝 알고리즘입니다. 

![Untitled](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/0d831052-bab9-473f-83f9-32b67b979dbc)


YOLO는  Bounding Box Regression 과 Classification을 나눠서 진행하는 Two Stage 방법과는 다르게 두개를 합쳐 동시에 진행함으로써 속도를 높였다. 

그리고 이미지를 S x S 개의 그리드로 나누고 이미지가 있을 법한 곳에 Bounding Box를 여러 개 예측하고 각 Bounding Box에 대한 confidence를 추출한다. 이 confidence score는 box안에 예측할 클래스가 존재하는지에 대한 파라미터를 뜻한다.

![Untitled (1)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/df4e6dda-8615-403a-bfc5-1a36c722282c)



YOLOv5의 경우 YOLOv5s, YOLOv5m, YOLOv5l, YOLOv5x 모델로 나눠지며 위 표와 같이 s가 가장 가벼운 모델로 다른 모델보다 성능이 낮지만 프레임수가 가장 높으며 x가 제일 무거운 모델로 성능이 좋으나 프레임 수가 가장 낮습니다. 즉 위 표를 보면 정확도와 속도 사이의 trade-off 를 보여주는 좋은 예시입니다.

![Untitled (2)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/35e682a4-8d5d-4e56-9f93-d23cdbf3f453)


YOLOv5의 구조는 위와 같습니다. Feature를 추출하는 Backbone, 추출된 Feature를 융합하여 성능을 높이는 Neck, Feature를 바운딩 박스 파라미터로 변환하는 Head와 같이 3종류의 부분으로 이루어져 있습니다.

Backbone은 여러층의 Convolution Layer와 Pooling Layer를 통해 입력 이미지로부터 다양한 크기의 Feature map을 추출하는 부분입니다. Backbone은 크게 3가지 블록으로 나뉘어져 있는데

CBL(Convolution with Batch normalization and Leaky Relu)은 Convolution Layer와 배치정규화, Leaky-Relu의 활성 함수로 이루어진 블록으로 피쳐를 추출하는데 기본적으로 사용되는 블록입니다.

CSP(Cross Stage Partial)로 피처맵의 일부에만 연산을 수행하고, 나머지 부분과 통합시키는 방법입니다. 일부의 피처맵만 통과시키기 때문에 연산량을 줄일 수 있고, 역전파 과정에서 Gradient의 흐름을 효율적으로 수행하게 되어 성능이 개선될 수 있습니다.

SSP(Spatial Pyraimd Pooling)으로 피처맵을 다양한 크기의 필터로 풀링한 후 다시 합쳐줌으로써 성능 향상을 가져옵니다.

**Neck** 부분에서는 다양한 크기의 피처맵을 융합하는데 PAN(Path Aggregation Network)을 사용하여 낮은 레벨의 피쳐와 높은 레벨의 피쳐를 섞어서 성능을 향상시킵니다.

Head는 컨볼루션 레이어를 이용해 Neck으로부터 출력된 피쳐를 네트워크의 최종 출력으로 변환해주는 부분으로 바운딩박스  파라미터, 물체가 존재할 확률, 클래스가 존재할 확률로 변환해줍니다.

# 2. YOLOv5 예제 구현

예제 구현을 위해 Google Colab 환경을 사용했으며 Dataset 은 Roboflow의 Aquarium_dataset을 사용했습니다.

본격적인 코드 구현에 들어가기 전 , Dataset을 다운받아 구글 코랩에 업로드하였으며, Dataset 구조는 아래와 같다.

![Untitled (3)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/4d295a88-ec73-45bc-8e0f-4a3f1531f894)


폴더의 구조를 보여주는 이유는 모델마다 설계와 구현 방식, 데이터셋에 따라서 형식이 달라지는데 YOLOv5는 위와 같으며 images 폴더에는 이미지가 들어가 있으며 label 폴더에는 txt 파일이 들어가 있다.

![Untitled (4)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/53de4098-ba6e-4cd8-9a9a-0634c3d5082e)


txt 파일의 경우 제목은 images에 들어있는 이미지들과 1:1 매칭이 돼야 하며 다를 시에는 학습시 오류가 난다. 위의 사진과 같이 내용이 적혀있는데 아래에서 다룰 Yaml파일에 n 번째 클래스와 X,Y,W,H값 좌표가 나와 있는 것을 확인할 수 있다.

![Untitled (5)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/8b197105-0de5-4a66-bb26-5c7a7a5a0eb7)


다음은 Yaml파일의 구조로 train,val 의 경우 학습할 이미지들의 경로를 적어주고 nc는 클래스의 개수를 적어주고 names에는 객체 검출을 위한 이름을 적어주면 된다.

![Untitled (6)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/05692fe4-a0ad-46b5-ab37-d863f9ac6e88)


YOLOv5 모델을 사용하기 위해 Github에 올려진 repository에서 코드들을 다운로드 및 임포트 했다.

![Untitled (7)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/9d11eb4d-3817-4688-878b-02356405d33f)

yaml파일의 경로를 설정해주고 바로 학습에 들어갔는데 image_size는 416, batch_size는 17, epochs는 100번을 주고 yaml파일 경로 설정 후 [yolo5s.pt](http://yolo5s.pt) 파일로 저장을 했다. 위 코드를 실행하면 YOLOv5 모델의 구조가 나오는데

![Untitled (8)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/d41bbda9-5531-4007-a638-57371ebf6ec3)


from 열은 이전 레이어를 나타내며 [-1,6]의 경우 -1은 직전 레이어 6은 6번째 레이어를 입력으로 사용한다는 것을 의미한다.

n 열은 해당 레이어를 몇 번 반복하는지 나타내고

module 의경우 Conv는 Convolution Layer, C3은 3way Cross Stage Partial Connections를, SPPF는 Spatial Pyramid Pooling Field를 의미한다

![Untitled (9)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/2942696c-d2c4-447b-95ca-4cbc0f9229f2)

위와 같이 결과를 간략하게 확인하는 것을 볼 수 있다.

![Untitled (10)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/c677dc56-45d0-46ee-9391-a0bb704956bd)

이렇게 학습이 제일 잘된 best.pt파일로 테스트를 해보면

![Untitled (11)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/e07ad4c3-2816-45f5-9334-41c61e94baff)

![Untitled (12)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/8e54aeb1-e90c-4ffb-a152-de284134f41c)

아래와 같이 객체 검출이 잘 되는 것을 확인할 수 있다.

또 YOLOv5의 경우 [best.pt](http://best.pt) 와 [yolov5s.pt](http://yolov5s.pt) 파일은 물론 다양한 curve 결과와 상관관계 loss, label등을 확인할 수 있는 파일들도 제공한다. 아래 그림은 F1-Confidence Curve 그래프이다.

![Untitled (13)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/f33a284d-3e56-468f-86b7-b77685106f17)

