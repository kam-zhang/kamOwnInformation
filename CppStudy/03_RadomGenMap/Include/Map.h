#ifndef __MAP_DEF_20141118_H__
#define __MAP_DEF_20141118_H__

#include <iostream>
#include <string>
#include "Log.h"
#include <string.h>
#include <stdio.h>
#include <cstdlib>
#include "PublicDef.h"

#define W 60
#define H 30
#define MIN_ROOM_NUM 4
//#define MAX_ROOM_AREA ((W*H)/MIN_ROOM_NUM)
#define MAX_ROOM_AREA 60
#define MIN_ROOM_AREA 20
#define MAX_ROOM_NUM ((W*H)/MIN_ROOM_AREA)

#define INVALID_POINT (' ')
#define ENTRANCE_POINT ('*')
#define INI_RAND(in) srand(in);

class Point
{
    private:
        int x;
        int y;
        int DistanceToEntrance;
    public:
        Point(int xin=0, int yin=0);
        int Getx();
        int Gety();
        void Setx(int in);
        void Sety(int in);
        int CalcDistanceToEntrance(int x,int y);
        int GetDistanceToEntrance();
};
class Room : public Point
{
    private:
        int Width;
        int High;
        int Number;
    public:
        Room();
        VOID PrintInfo();
        int GetLeftValue();
        int GetRightValue();
        int GetUpValue();
        int GetDownValue();
        VOID SetNumber(int in);
        int GetNumber();
};
class List
{
    private:
        struct node
        {
            struct node *prev;
            struct node *next;
            Point*element;
        }*head;
        WORD32 NodeNum;
        VOID ChangeNodeElem(struct node*p1,struct node*p2);
    public:
        List();
        VOID AppendElem2List(Point*);
        WORD32 GetNodeNum();
        VOID SortList();
        Point* GetAElem();
};
class Map
{
    private:
        UCHAR *MapDat;
        List RoomList;
        Point Entrance;
        VOID SetEntrancePoint();
        VOID GenRoom2List();
        WORD32 PutRoom2Map(Room*pRoom);
        bool CheckRoomOcpMapFree(Room*pRoom);
        WORD32 GetRandRoomNum(VOID);
        UCHAR GetMapValue(int x,int y);
        VOID SetMapValue(int x,int y,UCHAR v);
        UCHAR Dec2HexChar(int in);
        VOID PrintAllRoom(List*pList);
        VOID AddRoad();
        void CreatRoad(Point*pPoint);
    public:
        Map(WORD32 RandSeed);
        ~Map();
        void PrintMap();
        
};
#endif
