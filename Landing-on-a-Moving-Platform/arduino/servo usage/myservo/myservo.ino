#include<Servo.h>//引入舵机控制库文件

Servo myservo;//实例化一个舵机对象来控制舵机

void setup(){

myservo.attach(9);//声明舵机控制接口为引脚9

Serial.begin(9600);//连接到串行端口，波特率为9600

Serial.println("seral_simple ready" ) ;//串口输出提示内容

}

void loop()//将0到9的数转化为0到180角度，并让LED闪烁相应数的次数

{

int val=Serial.read();//读取串行端口的值

if(val>='0'&&val<='18')

{

val=val-'0';//将特征量转化为数值变量

val=val*10;//角度设置为10的倍数

Serial.print("moving servo to ");//舵机旋转角度输入0-18任意一个数

Serial.print(val,DEC);//以十进制形式输出舵机旋转角度

Serial.println();//实现换行功能

myservo.write(val);//控制舵机旋转输入的角度

}

}
