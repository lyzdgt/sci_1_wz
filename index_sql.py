import matplotlib.pyplot as plt
import math
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
_type='蔬菜'
city='衢州'
n_c=5
#导入数据
import pymysql
# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
db = pymysql.connect(host="39.107.25.235",user="root", password="zqc1982", db="wzz")
cursor = db.cursor()
sql = 'select * from Shiyan'
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
        password=row[2]
except:
    print("Error: unable to fecth data")
db.close()
test=pd.DataFrame(results)
test['date']=test[0]
test=test[[1,2,3,6,'date']]
c=[]
for i in test.groupby([1,3,2]):
    c.append(i)
list_s=['type','avg','median','80per','90per','95per','max','place','EDI50','EDI95','P_c','MOE','city']
df_c= pd.DataFrame(np.zeros((len(c),len(list_s))),columns=list_s)
province=['黑龙江','吉林','辽宁','北京','河北','河南','宁夏','陕西','内蒙古','青海','福建','浙江','江苏','上海','江西','湖北','四川','湖南','广西','广东']
array=[[673.70,1201.02,1131.27,825.20,935.58,1517.90,1002.35,783.86,1038.39,1681.60 ,920.55 ,1126.50 ,620.64 ,566.96 ,641.55 ,916.16 ,806.08 ,905.68 ,765.55 ,431.90],
       [76.49 ,153.02 ,262.77 ,173.63 ,61.95,36.66 ,109.07 ,89.21 ,72.02 ,6.10 ,74.87 ,82.04 ,139.29 ,81.58 ,34.83 ,82.57 ,105.28 ,39.27 ,42.99,27.39 ] ,
       [122.06 ,187.44, 85.42 ,55.88, 51.22, 75.34, 141.51, 103.41, 253.63, 117.85, 90.20 ,28.56 ,53.99 ,19.13 ,30.23, 46.38 ,100.65 ,29.60, 15.37, 19.96], 
       [48.75, 100.50, 105.92 ,116.30, 39.16, 34.55 ,84.33, 52.41 ,136.71, 77.55 ,170.83, 75.40, 128.81, 107.81, 75.41, 65.18, 132.67, 123.30, 135.66, 104.11 ],
       [42.13, 46.87, 45.88 ,61.13, 29.97, 31.95, 17.63, 28.75 ,52.74, 11.57 ,27.37 ,34.65, 32.44, 35.09, 23.97, 29.10 ,16.25, 24.46 ,19.78, 16.51 ],
       [9.75, 17.54, 52.67, 77.93, 26.36 ,2.88 ,19.70 ,48.56, 108.16 ,62.09 ,48.48 ,70.83 ,72.63 ,100.30, 48.56, 3.28, 11.61 ,9.62 ,4.31 ,36.46 ],
       [21.54, 25.41, 13.14, 19.48, 13.67, 5.88 ,19.00 ,5.81, 4.24 ,3.57 ,158.65 ,99.73 ,79.13 ,73.29 ,19.11 ,42.26 ,16.47 ,43.88 ,31.42, 55.65 ],
       [359.62, 458.48, 283.39, 584.27, 347.67 ,345.22 ,353.04 ,346.14 ,231.38 ,409.95 ,397.80 ,409.79 ,404.33, 495.25, 263.75 ,483.62 ,492.99 ,633.87, 566.25 ,253.66 ],
       [74.03 ,58.84 ,125.85, 192.48, 231.73 ,46.45, 137.41 ,16.76 ,67.79, 41.50 ,114.88 ,150.72 ,134.42, 108.29 ,7.91 ,23.30 ,76.44, 2.20 ,2.87 ,28.69 ],
       [219.89 ,1301.49, 493.43, 1107.71, 775.30, 1192.45 ,517.10 ,345.39 ,2575.06 ,618.33 ,865.37 ,786.33 ,1009.08 ,903.59,320.26,284.99,313.97,1062.00,1302.19,1192.68]]
array=np.array(array)
ltype=['粮食加工品','豆制品','薯类和膨化食品','肉制品','蛋制品','乳制品','水产制品','蔬菜','水果制品','饮料']
df_i= pd.DataFrame(array,columns=province,index=ltype)
for i in range(len(c)):
    df_c.loc[i,'type']=c[i][0][2]
    df_c.loc[i,'place']=c[i][0][0]
    df_c.loc[i,'city']=c[i][0][1]
    df_c.loc[i,'80per']=np.percentile(c[i][1][6].astype('float32').values,80)
    df_c.loc[i,'90per']=np.percentile(c[i][1][6].astype('float32').values,90)
    df_c.loc[i,'95per']=np.percentile(c[i][1][6].astype('float32').values,95)
    df_c.loc[i,'max']=c[i][1][6].astype('float32').values.max()
    df_c.loc[i,'avg']=c[i][1][6].astype('float32').values.mean()
    df_c.loc[i,'median']=np.percentile(c[i][1][6].astype('float32').values,50)
    df_c.loc[i,'EDI50']=((df_i.loc[c[i][0][2],c[i][0][0]]/1000)*df_c.loc[i,'median'])/60
    df_c.loc[i,'EDI95']=((df_i.loc[c[i][0][2],c[i][0][0]]/1000)*df_c.loc[i,'95per'])/60
    c_max=c[i][1][6].astype('float32').values.max()
    c_avg=c[i][1][6].astype('float32').values.mean()
    df_c.loc[i,'P_c']=math.sqrt((c_max*c_max+c_avg*c_avg)/2)
    df_c.loc[i,'MOE']=df_c.loc[i,'EDI50']/0.0006
    df_c.loc[i,'THQ']=df_c.loc[i,'EDI95']/0.0035
m=df_c.shape[0]
julei=df_c[['P_c','MOE','THQ']]
kmeans = KMeans(n_clusters=n_c, random_state=0).fit(julei) 
label=list(kmeans.labels_)
center=pd.DataFrame(kmeans.cluster_centers_,columns=['P_c','MOE','THQ']) 
for i in range(len(c)):
    df_c.loc[i,'level']=label[i]
for i in range(n_c):
    center.loc[i,'point']=np.sqrt(center.loc[i,'P_c']*center.loc[i,'P_c'])+np.sqrt(center.loc[i,'MOE']*center.loc[i,'MOE'])+np.sqrt(center.loc[i,'THQ']*center.loc[i,'THQ'])
for i in range(n_c):
    center.loc[i,'point']=np.sqrt(center.loc[i,'P_c']*center.loc[i,'P_c'])+np.sqrt(center.loc[i,'MOE']*center.loc[i,'MOE'])+np.sqrt(center.loc[i,'THQ']*center.loc[i,'THQ'])
    center.loc[i,'biao']=center.index[i]
    if center.loc[i,'point']==np.percentile(center['point'],0):
        center.loc[i,'level']=1
    if center.loc[i,'point']==np.percentile(center['point'],25):
        center.loc[i,'level']=2
    if center.loc[i,'point']==np.percentile(center['point'],50):
        center.loc[i,'level']=3
    if center.loc[i,'point']==np.percentile(center['point'],75):
        center.loc[i,'level']=4
    if center.loc[i,'point']==np.percentile(center['point'],100):
        center.loc[i,'level']=5 
for i in range(len(c)):
    df_c.loc[i,'new_level']=center.loc[center[center['biao']==df_c.loc[i,'level']].index,'level'].values
for i in range(m):
    if (df_c.loc[i,'type']==_type and df_c.loc[i,'city']==city):
        re_TCR=df_c.loc[i,'MOE']
        re_P_c=df_c.loc[i,'P_c']
        re_THQ=df_c.loc[i,'THQ']
        re_level=df_c.loc[i,'new_level']
print(re_level)
print(center[['P_c','MOE','THQ','level']])
df_c.to_excel('C:/Users/29468/Desktop/222.xlsx')