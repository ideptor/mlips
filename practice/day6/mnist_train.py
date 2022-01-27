import matplotlib.pyplot as plt
import random
import numpy as np
import torch

# mnist data를 받아서 그림으로 그려주는 함수
def plot_train_data(image, title):
    pixels = image.reshape((28, 28))
    plt.imshow(pixels, cmap='gray')
    plt.title(f"{title}")
    plt.show()
    

# 입력 데이터를 5*5로 그려줌
def plot_multiple_train_data(train_data, rows=5, cols=5):
    figure = plt.figure(figsize=(10, 8))
    for i in range(1, cols * rows + 1):
        sample_idx = np.random.randint(len(train_data), size=(1,)).item()
        img, label = train_data[sample_idx]
        figure.add_subplot(rows, cols, i)
        plt.title(label)
        #plt.axis("off")
        plt.imshow(img.squeeze(), cmap="gray")

    plt.tight_layout()
    plt.show()

    
def __show_sample_predict(model, device, image, gt):

    image = image.to(device)
    model = model.to(device)
    
    out = model(image)                # 모델에 이미지 넣은 결과값 -> out.shape = (10, )
    conf, pred = torch.max(out, 1)    # 가장 큰 1개 값의 confidence와 pred(class) 가져오기    
    
    print("> gt:", gt)
    print("> image shape:", image.shape)
    print("< out:", out.cpu().detach().numpy())
    print("< predicted:", pred.item())
    print("< confidence:", conf.item())
    
    plot_train_data(image.cpu(), f"Pred:{pred.item()}, GT:{gt}")
    

def show_sample_predict_nn(model, device, test_data):

    idx = random.randrange(0, len(test_data)-1)
    image, gt = test_data[idx]
    image = image.view(1,-1)
    
    __show_sample_predict(model, device, image, gt)
    

def show_sample_predict_cnn(model, device, test_data):

    idx = random.randrange(0, len(test_data)-1)    # 임의의 정수 1개 
    image, gt = test_data[idx]                     # image하고 gt 가져오기
    image = image.view(1,1,28,28)
    
    __show_sample_predict(model, device, image, gt)
    
    
def draw_loss(train_losses, test_losses):

    epochs = [i for i in range(1, len(train_losses)+1)]
    plt.plot(epochs, train_losses, c="blue", label="train loss")
    plt.plot(epochs, test_losses, c="red", label="test loss")
    plt.legend()
    plt.show()