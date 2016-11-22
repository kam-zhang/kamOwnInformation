#include "gtest/gtest.h"
#include <iostream>
#include <cmath>
#include <cstdlib>
#include "base/BaseTypes.h"
#include "GeneralFunction.h"
#include <pthread.h>
#include <unistd.h>
using namespace std;
#define GTEST_MODE  SWITCH_OFF
#ifndef NULL
#define NULL ((void*)0)
#endif
UCHAR b[256] = {0x01,0x23,0x45,0x56};
void *thread1(void* pin)
{
    int i;
    for(i=0;i<5;i++)
    {
    	cout<<"PID["<<getpid()<<"] thread11111   "<<i<<endl;
    	sleep(2);
    }
    return NULL;
}
void *thread2(void* pin)
{
    int i;
    for(i=0;i<7;i++)
    {
    	cout<<"PID["<<getpid()<<"] thread22222   "<<i<<endl;
    	sleep(2);
    }
    return NULL;
}
int main(int argc, char **argv)
{
#if (SWITCH_ON == GTEST_MODE)
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();	
#else
    pthread_t pid1;
    pthread_t pid2;
    pthread_attr_t *p1_attr=NULL;
    pthread_attr_t *p2_attr=NULL;
    pid_t ret;

    ret=fork();
    if(ret < 0) printf("fork error\n");
    else if(0==ret)printf("I am SON, pid is %d\n",getpid());
    else printf("I am FATHER, pid is %d\n",getpid());
    if(0!=pthread_create(&pid1, p1_attr, thread1, (void*)NULL))
    {
        printf("creat thread1 failed\n");
        return 1;
    }
    else
    	printf("creat thread1 success\n");

    if(0!=pthread_create(&pid2, p2_attr, thread2, (void*)NULL))
    {
    	printf("creat thread2 failed\n");
        return 1;
    }
    else
    	printf("creat thread2 success\n");

    pthread_join(pid1,NULL);
    pthread_join(pid2,NULL);

    return 0;

#endif
}



