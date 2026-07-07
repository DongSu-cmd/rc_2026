from pop import AI 
ann = AI.ANN(input_size=3, output_size=3)
import numpy as np

a1 = [173, 171, 162, 187, 157, 169, 177, 159, 182]
a2 = [270, 275, 245, 280, 230, 265, 270, 250, 275]
a3 = [17, 51, 62, 12, 47, 30, 5, 32, 0]
a4 = [[1,0,0], [1,0,0,],[1,0,0],[0,1,0],[0,1,0],[0,1,0],[0,0,1],[0,0,1],[0,0,1]]

ann.X_data = np.array([a1, a2, a3], dtype=np.float32).T
ann.Y_data = np.array(a4, dtype=np.float32).reshape(-1,1)

