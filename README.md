# Real Time Text-to-Image Synthesis with ChatGPT & LCM-LoRA

### main.py
- Flask 로 구현
- User 는 먼저 nickname 을 입력하고 들어온다.
- 그 후, AI service(text-to-image) 를 체험할 수 있다.
- Text 를 입력하는 동시에 image 는 생성이 되고(정확히는 user 의 입력이 0.5 초 이상 멈추면 생성) 이때, 코드 상으로 구현된 AI model 은 GPU 4 개를 이용해 구현됐기 때문에 최대 4명의 client request 를 처리할 수 있다. 
- Service 이용을 다했으면, review 를 남길 수 있다. 
- 이 review 는 server 가 다운되도 .txt 형태로 남아있기 때문에 다시 server 를 가동시키면 불러올 수 있다.

### __init__.py
- User 가 들어올 때마다 매번 model 을 불러오는 것은 cost 가 굉장히 크기 때문에 server 를 가동시키는 즉시. 4개의 pipe(AI model) 을 불러온다. 
- 가용한 GPU 가 4개이기 때문에 4개만 사용한다. 
- 사용한 AI model 은 SDXL(더 큰 model) + LCM-LoRA(sampling 횟수 25->4~8회로 감소)이다. 

### static
- generated_images: user 가 생성한 이미지들을 user 별로 저장
- initial.png: 아무런 text 가 입력되지 않았을 때/모든 GPU 가 사용중일 때 보여지는 이미지(짱구)


### templates
- index.html: user nickname 을 받는 화면
- service.html: text-to-image generation service 제공/review
    - review 는 user-log/{nickname}_log.txt 에 남겨진다. 

### user-log
- {nickname}_log.txt: user 별 후기

### videos

Demo 영상

<!-- [![Watch the video](./videos/test1.webm)] -->

![demo1](![demo1](https://github.com/qkrwnstj306/Text-to-Image-Toy-Project/assets/120474819/40613aef-0f45-47d3-ac73-ebd1f02862f1))

<img src="![demo1](https://github.com/qkrwnstj306/Text-to-Image-Toy-Project/assets/120474819/40613aef-0f45-47d3-ac73-ebd1f02862f1)" width="500" height="300">

<!-- [![Watch the video](./videos/test2.webm)]  -->


### Server

Ngrok 을 사용해서 공용 서버로 올린다. 


### 개선점

Image 를 저장하지 않고 바로 response 하면 더 빠른 이미지 제공이 가능할 것 이다. (본 프로젝트에선, 이미지를 확인하기 위해 진행하지 않음)
