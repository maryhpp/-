# -
引擎计划
face_detect_final 
1）注释test..py的第200行

2）修改mtcnn/detect_face.py的第85行
将代码"data_dict = np.load(data_path, encoding='latin1').item()"
改为
"data_dict = np.load(data_path, encoding='latin1',allow_pickle=True).item()"
