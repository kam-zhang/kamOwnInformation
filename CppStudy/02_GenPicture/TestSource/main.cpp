#include "gtest/gtest.h"
#include <iostream>
#include <cmath>
#include <cstdlib>
#include "base/BaseTypes.h"
using namespace std;
#define GTEST_MODE  SWITCH_OFF

#define DIM 1024
#define DMl (DIM - 1)
#define _sq(x) ((x)*(x))
#define _cb(x) ((x)*(x)*(x))
#define _cr(x) (unsigned char)(pow((x),1.0 / 3.0))
unsigned char GR(int,int);
unsigned char BL(int,int);
unsigned char RD(int i,int j)
{
    return (_sq(0.1*(j-512))+256*sin(0.01*(i-512)));
}
unsigned char GR(int i,int j)
{
    return 0;//+_cr(2000*(j));
}
unsigned char BL(int i,int j)
{
    return RD(j,i);//_sq(0.2*(i-512))+_sq(0.2*(j-512));
}
void pixel_write(int,int);
FILE*fp;


int main(int argc, char **argv)
{
#if (SWITCH_ON == GTEST_MODE)
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();	
#else
    WORD16 wTemp;
    WORD32 dTemp;
    fp = fopen("MathPic.bmp","wb");
    fprintf(fp,"BM");
    
    dTemp = 54+3*DIM*DIM;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = 0;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = 54;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = 0x28;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = DIM;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = DIM;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);

    wTemp = 1;
    fwrite(&wTemp, 1, sizeof(wTemp), fp);
    wTemp = 24;
    fwrite(&wTemp, 1, sizeof(wTemp), fp);
    dTemp = 0;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = 3*DIM*DIM;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = 0;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = 0;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = 0;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);
    dTemp = 0;
    fwrite(&dTemp, 1, sizeof(dTemp), fp);

    
    
    for(int j=0; j < DIM; j++)
        for(int i=0; i < DIM; i++)
            pixel_write(i,j);
    fclose(fp);
    return 0;
#endif
}

void pixel_write(int i,int j)
{
    static unsigned char color[3];
    color[0] = BL(i,j) & 0xff;
    color[1] = GR(i,j) & 0xff;
    color[2] = RD(i,j) & 0xff;
    fwrite(color, 1, 3, fp);
}



