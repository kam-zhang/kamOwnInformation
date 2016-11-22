#include<stdio.h>

#define SetValue(Index, Value) (test##Index) = (Value)
#define GetValue(Index) (test##Index)
int test,test0,test1,testDlqos,testCurrentBlockStatus;
int main()
{
    SetValue(,1);
    SetValue(0,2);
    SetValue(1,3);
    SetValue(Dlqos,4);
    SetValue(CurrentBlockStatus,9);
    
    printf("%d%d%d%d%d\n",test,test0,test1,testDlqos,testCurrentBlockStatus);

    return 0;
}

