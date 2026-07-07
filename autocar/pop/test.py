from pop import AI 
ann = AI.ANN(input_size=3, output_size=3)
import numpy as np

result = ann.run
pred_index = np.argmax(result, axis=1)
true_index = np.argmax(ann.Y_data, axis=1)
classes = ["유아", "어린이", "성인"]


for i in range(len(pred_index)):
    print(f"{i}번 데이터: :"," 입력 = ", ann.X_data[i], "/예측=", classes[int(pred_index[i])])
    print("/정답=", classes[int(pred_index[i])])

num_classes = len(classes)
confusion = np.zeros(num_classes, num_classes), dtype=np.int32


for name in classes:
    print(f"{name:>6}", end="")
print()

for i in enumerate(classes):
    print(f"{name:>6}", end="")
    for j in range(num_classes):
        print(f"{confusion[i,j]:>6}", end="")
    print()
    