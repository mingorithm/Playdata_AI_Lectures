# EfficientNet 분석

# 1. EfficientNet이란?

ConvNet은 일반적으로 지정된 예산 내에서 개발되어 왔기 때문에 그 안에서 정확도를 높이기 위한 연구가 활발히 진행되었다. 2020년 개발된 EfficientNet은 모델의 depth, width, 입력 이미지의 resolution을 조정하여 모델의 성능을 최적화한다.

width의 경우 증가할수록 Feature map에서는 더 많은 채널정보를 포함하게 돼서 더 많은 종류의 정보를 담을 수 있기에 성능이 좋아집니다.

depth의 경우 Layer의 개수를 의미하며 depth가 깊다는 의미는 해당 네트워크가 많은 수의 Layer를 갖고 있음을 뜻합니다.

resolution은 input image, feature map의 해상도를 의미합니다. 이때 해상도는 width * height의 크기를 뜻합니다.

이러한 점에서 EfficientNet은 이 세 가지 변수를 모두 고려한 모델이라는 점입니다.

![Untitled](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/358c0932-b6ad-4080-9f67-ff5a9e6a3309)

width,height, resolution을 무조건 확장시키기만 한다면 어느 정도 accuracy가 향상되지만 더 큰 모델에서는 accuracy 상승률이 감소한다. 그래서 더 나은 정확도와 효율성을 위해서 세 가지 변수의 balance를 맞추는 것(Compound Scaling)이 매우 중요합니다.

EfficientNet에서는 baseline model을 만들기 위해 Neural Architecture Search(NAS) 방법을 사용합니다. 즉 딥러닝을 사용하여 딥러닝 모델을 찾는 방법입니다.

![Untitled (1)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/6783fd65-bbe8-4515-a1da-9fd3f62ee6a6)

위 테이블은 EfficientNet-B0의 구성을 나타낸 표입니다. 앞쪽 Operator에 해당하는 부분은 NAS로 찾은 부분이고 뒤쪽의 resolution, channels, layers는 grid search로 찾은 부분입니다. 여기서 더 큰 EfficientNet을 만들기 위해선 scale만 키워주면 됩니다.

![Untitled (2)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/3fb13688-b2d2-4786-ace0-76d799d4a2c0)

같은 FLOPS( FLoating point Operations Per Second)를 보여줌에도 정확도가 크게 차이가 나는 것을 확인할 수 있습니다.

# 2. EfficientNet 코드 구현

![Untitled (3)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/a0ce2d6d-9661-4116-9198-f6d1c8cc8ee4)

EfficientNet을 구성하는 핵심 모듈은 MBConv Block이며 이는 MobileNetV2에서 제안된 블록입니다. 

![Untitled (4)](https://github.com/mingorithm/Playdata_AI_Lectures/assets/84362444/80c1b225-f510-4642-9011-6e9c6562c421)

위 코드는 MBConvBlock을 이어 붙여 EfficientNet을 정의하는 코드입니다.

# 3. 마치며

다른 모델들과는 다르게 더 적은 파라미터와 연산량으로 SOTA를 달성했다는 점, Compund Scaling을 통하여 모델을 제안했다는 점이 굉장히 흥미로웠습니다. 무엇보다도 다양한 환경과 app에서도 사용이 가능하며 특히 자원이 제한된 환경에서 매우 유용하다는 점이 인상 깊었습니다.  이 밖에도 Stohastic Depth, AutoAugmentation 등 여러 기법을 사용했다는 점도 배울 것이 많았습니다.
