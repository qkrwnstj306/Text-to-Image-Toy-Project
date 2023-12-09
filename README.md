# Real Time Text-to-Image Synthesis with ChatGPT & LCM-LoRA

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

[![Watch the video](./videos/test1.webm)]

<img src="![ezgif com-crop](https://github.com/qkrwnstj306/Text-to-Image-Toy-Project/assets/120474819/1efae5d3-34cd-4f02-9fc5-a78e4a1a4a47)">


[![Watch the video](./videos/test2.webm)]


### Server
Ngrok 을 사용해서 공용 서버로 올린다. 


