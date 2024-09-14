#include <stdio.h>

void checkGrade(void) 
{
    // 使用两个数组来代替 pair
    double first[100];
    double second[100];
    double x = 0;
    int i = 1;
    int j = 1;
    int flag = 1;

    // 使用 scanf 代替 cin
    while(scanf("%lf", &x) == 1){
        if(flag) {
            if(x >= 10) {
                flag = 0;
                goto ELSE; 
            } else {
                first[i++] = x;
            }
        } else {
ELSE:
            second[j++] = x;
            if(j == i) break;
        }
    }

    double sum = 0;
    double cnt = 0;
    
    // 打印 first 数组
    for(int m = 1; m < i; m++) {
        printf("%.1f\t", first[m]);
    }
    printf("\n");
    
    // 打印 second 数组
    for(int m = 1; m < i; m++) {
        printf("%.1f\t", second[m]);
    }
    printf("\n");

    // 计算加权平均值
    for(int m = 1; m < i; m++){
        sum += first[m] * second[m];
        cnt += first[m];
    }
    
    double res = sum / cnt;
    printf("%.4f\n", res);

    return;
}

int main()
{
    while(1){
        checkGrade();   
    }
}
