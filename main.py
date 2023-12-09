# main.py
from __future__ import absolute_import, division, print_function, unicode_literals
from __init__ import pipe, pipe2, pipe3, pipe4


import torch
from PIL import Image
from flask import jsonify, Flask, render_template, request, redirect, url_for, send_file, request
import os, io
import time, random, string



app = Flask(__name__)

# 사용자의 닉네임과 후기를 저장할 딕셔너리
user_reviews = {}

# user-log 디렉토리 경로
log_directory = "./user-log"

# user-log 디렉토리에서 파일 목록을 가져옴
file_list = os.listdir(log_directory)

# 사용되는 model  
model_list = [pipe, pipe2, pipe3, pipe4]
used_model = []

# 각 파일에 대해 사용자 닉네임과 후기를 딕셔너리에 저장
for file_name in file_list:
    # 파일이 .txt로 끝나는지 확인
    if file_name.endswith("_log.txt"):
        # 사용자 닉네임 추출
        user_name = os.path.splitext(file_name)[0]

        # 파일의 내용(후기) 읽어오기
        file_path = os.path.join(log_directory, file_name)
        with open(file_path, "r") as log_file:
            reviews = log_file.readlines()

        # 딕셔너리에 사용자와 후기 저장
        user_reviews[user_name] = {"log_path": file_path, "reviews": reviews}

def generate_random_nickname():
    # 8자리의 무작위 닉네임 생성
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 클라이언트로부터 받은 닉네임
        nickname = request.form["nickname"]

        # 닉네임이 이미 딕셔너리에 있는지 확인
        while nickname in user_reviews:
            # 중복된 닉네임이면 새로운 닉네임 생성
            nickname = generate_random_nickname()

        # 클라이언트 닉네임에 대한 로그 파일 생성 또는 로드
        user_log_path = f"./user-log/{nickname}_log.txt"
        if not os.path.exists(user_log_path):
            with open(user_log_path, "w"):
                pass  # 빈 파일 생성

        # 닉네임 저장 (user_reviews 딕셔너리에는 _log가 포함되지 않도록 수정)
        user_reviews[nickname] = {"log_path": user_log_path, "reviews": []}

        # /service 페이지로 리다이렉트
        return redirect(url_for("service", nickname=nickname))

    return render_template("index.html")



@app.route("/service/<nickname>", methods=["GET", "POST"])
def service(nickname):
    if request.method == "POST":
        # 클라이언트의 후기 읽어오기
        review = request.form["review"]

        # 후기가 있으면 로그 파일에 저장
        if review:
            with open(user_reviews[nickname]["log_path"], "a") as log_file:
                log_file.write(f"{review}\n")

    # 모든 사용자의 후기를 읽어오기
    all_reviews = {}
    for user, data in user_reviews.items():
        with open(data["log_path"], "r") as log_file:
            reviews = log_file.readlines()
            all_reviews[user] = reviews

    return render_template("service.html", nickname=nickname, all_reviews=all_reviews)

@app.route("/submit_review/<nickname>", methods=["POST"])
def submit_review(nickname):
    if request.method == "POST":
        # 클라이언트로부터 받은 후기
        review_data = request.json
        review_text = review_data.get("review")

        # 후기가 있으면 로그 파일에 저장
        if review_text:
            with open(user_reviews[nickname]["log_path"], "a") as log_file:
                log_file.write(f"{review_text}\n")

            # 성공적으로 후기를 받아서 처리했음을 클라이언트에 응답
            return "Review submitted successfully", 200

    # 오류 응답
    return "Failed to submit review", 400


@app.route("/fetch_reviews", methods=["GET"])
def fetch_reviews():
    # Read reviews from the user_reviews dictionary in real-time
    all_reviews = {}
    for user, data in user_reviews.items():
        with open(data["log_path"], "r") as log_file:
            reviews = log_file.readlines()
            all_reviews[user] = reviews

    # 후기를 JSON 형태로 응답
    return jsonify(all_reviews)


@app.route("/generate_image/<nickname>", methods=["POST"])
def generate_image(nickname):
    if request.method == "POST":
        # 클라이언트로부터 받은 text
        text_data = request.json
        user_text = text_data.get("text")

        # 여기서 모델로 이미지를 생성하고 이미지 데이터를 반환
        prompt = user_text  # Use the user's text as the prompt

        generator = torch.manual_seed(42)
        
        model = None
        
        for candidate_model in model_list:
            if str(candidate_model) not in used_model:
                model = candidate_model
                break
        
        if model != None:
            used_model.append(str(model))
            
            image = model(
                prompt=prompt,
                num_inference_steps=5,
                generator=generator,
                guidance_scale=1.0,
            ).images[0]

            # Save the image to a file with a unique filename
            sub_pth = "./static"
            image_path = f"/generated_images/{nickname}/generated_image_{int(time.time())}.png"
            total_pth = sub_pth + image_path
            os.makedirs(os.path.dirname(total_pth), exist_ok=True)
            image.save(total_pth, format="PNG") 

            used_model.remove(str(model))
            # Return the path to the saved image as JSON
            return jsonify({"image_path": image_path}), 200
        return jsonify({"image_path": '/initial.png'}), 200
    # 오류 응답
    return "Failed to generate image", 400

if __name__ == '__main__':
    app.run(debug=True, port = 4999)
    
