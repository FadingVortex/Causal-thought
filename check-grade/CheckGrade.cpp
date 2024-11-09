#include <bits/stdc++.h>
using namespace std;

void checkGrade(void) 
{
    pair<double, double> par[100];
    double x = 0;
    int i = 1;
    int j = 1;
    bool flag = true;

    while(cin>>x){
        if(flag) {
            if(x >= 10) {
                flag = false;
                goto ELSE; 
            } else {
                par[i++].first = x;
            }
        } else {
ELSE:
            par[j++].second = x;
            if(j == i) break;
        }
    }
    double sum = 0;
    double cnt = 0;
    for(int m = 1; m<i; m++) {
        printf("%.1f\t", par[m].first);
    }
    cout<<endl;
    for(int m = 1; m<i; m++) {
        printf("%.1f\t", par[m].second);
    }
    cout<<endl;
    for(int m = 1; m<i; m++){
        sum += par[m].first*par[m].second;
        cnt += par[m].first;
    }
    double res = sum/cnt;
    cout<<res<<endl;
    return;
}

int main()
{
    // #ifndef ONLINE_JUDGE
    //     freopen("1.txt","r",stdin);
    // #endif
    while(1){
        checkGrade();   
    }
}