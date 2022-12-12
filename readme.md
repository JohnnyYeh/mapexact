# 使用方法
1、运行main.py  
2、无需任何输入, 默认开始获取连接点的坐标的模式, 只需点击**左键**, 代码会自动记录坐标点  
3、在**地图窗口**输入**t**, 即开始记录**停靠点坐标**, 然后输入与这个停靠点连接的连接点的数量, 这个数量一定是小于**4**的,  
   然后输入与这个停靠点连接的**连接点ID**, 最重要的是一定不要输错和点错, 因为代码目前没有实现删除上一步操作的功能  
4、在**地图窗口**输入**c**, 即开始记录**目标点坐标**  
5、如果有前面操作有**漏**的点没有记录, 则可以输入**a**或者**b**, **a**是增加连接点, **b**是增加连接点与停靠点的边  
6、在**地图窗口**输入**c**，即可保存所有结果, 并输出为 data.csv, RoadVertexPosData.csv,  StoppingPointPosData.csv, CustomerPosData.csv四个文件  
    data.cs 为连接点与停靠点之间的连接关系 0表示没有连接 1表示有连接  
    RoadVertexPosData.csv 为连接点的坐标和ID  
    StoppingPointPosData.csv 为停靠点的坐标和ID  
    CustomerPosData.csv 为客户点的坐标和ID  
7、在**地图窗口**按ESC键即可退出程序  

# 依赖性
## 安装Numpy  
`pip install numpy` 
## 安装OpenCV
`pip install opencv-python`
## 安装Pandas
`pip install pandas`
