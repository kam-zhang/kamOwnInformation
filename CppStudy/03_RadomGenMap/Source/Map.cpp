#include <iostream>
#include <string>
#include "Log.h"
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <cstdlib>
#include "PublicDef.h"
#include "Map.h"
using namespace std; 

int GET_RAND(int max,int min) 
{
    WORD16 randnum = (WORD16)rand();
    //LogPrintf("randnum:%d,max:%d,min:%d\n",randnum,max,min);
    return (((randnum)%(max-min))+min);
}
Point::Point(int xin, int yin){x=xin;y=yin;}
int Point::Getx(){return x;}
int Point::Gety(){return y;}
void Point::Setx(int in){x=in;}
void Point::Sety(int in){y=in;}
int Point::CalcDistanceToEntrance(int x,int y)
{
    DistanceToEntrance = (int)(0.5 + sqrt((double)((x-this->Getx())*(x-this->Getx())
                             +(y-this->Gety())*(y-this->Gety()))));
    return DistanceToEntrance;
}
int Point::GetDistanceToEntrance(){return DistanceToEntrance;}

Room::Room():Point()
{
    int area=GET_RAND(MAX_ROOM_AREA,MIN_ROOM_AREA);
    Width = GET_RAND(W/MIN_ROOM_NUM,3);
    High = MAX(3, MIN(area/Width,H-1));
    Width |= 0x01; // 确保宽度是计数
    High |= 0x01;  // 确保高度是计数
    Setx(GET_RAND(W-Width/2,Width/2+1));
    Sety(GET_RAND(H-High/2,High/2+1));
    Number = InvalidValue;
}
VOID Room::PrintInfo()
{
    LogPrintf("\n");
    LogPrintf("RoomInfo--No:%X,Pointer:0x%08x,Center-x:%d,y:%d\n",Number,this,Getx(),Gety());
    LogPrintf("RoomInfo---Width:%d,High:%d,DistanceToEntrance:%d\n",Width,High,GetDistanceToEntrance());
}
int Room::GetLeftValue(){return Getx()-Width/2;}
int Room::GetRightValue(){return Getx()+Width/2;}
int Room::GetUpValue(){return Gety()-High/2;}
int Room::GetDownValue(){return Gety()+High/2;}
VOID Room::SetNumber(int in){Number=in;}
int Room::GetNumber(){return Number;}


List::List(){head=NULL;NodeNum=0;}
VOID List::AppendElem2List(Point*Elem)
{
    struct node *NewNode=new struct node;
    NewNode->element = Elem;
    if(NULL==head)
    {
        head=NewNode;
        head->prev=head;
        head->next=head;
    }
    else
    {
        NewNode->prev=head->prev;
        NewNode->next=head;
        head->prev->next=NewNode;
        head->prev=NewNode;
    }
    NodeNum++;
}
WORD32 List::GetNodeNum(VOID)
{
    return NodeNum;
}
VOID List::ChangeNodeElem(struct node*p1,struct node*p2)
{
    Point *p=p1->element;
    p1->element = p2->element;
    p2->element = p;
}
VOID List::SortList()
{   
    struct node*pElem1 = head;
    struct node*pElem2 = NULL;
    while(pElem1->next != head)
    {
        pElem2 = pElem1->next;
        while(pElem2 != head)
        {
            if(pElem1->element->GetDistanceToEntrance() > pElem2->element->GetDistanceToEntrance())
                ChangeNodeElem(pElem1, pElem2);
            pElem2 = pElem2->next;
        }
        pElem1 = pElem1->next;
    }
}
Point* List::GetAElem()
{
    static struct node*pElem1 = head;
    static int count = 0;
    if(count >= NodeNum)
    {
        count = 0;
        pElem1 = head;
        return NULL;
    }
    pElem1 = pElem1->next;
    count++;
    return pElem1->prev->element;
}
VOID Map::SetEntrancePoint() 
{
    Entrance.Setx(GET_RAND(W,0));
    Entrance.Sety(GET_RAND(H,0));
    SetMapValue(Entrance.Getx(),Entrance.Gety(),ENTRANCE_POINT);
    LogPrintf("Entrance:x=%d,y=%d\n",Entrance.Getx(),Entrance.Gety());
}
void Map::CreatRoad(Point*pPoint)
{
    
}
VOID Map::AddRoad()
{
    Room*pRoom = NULL;
    List ArrivedRoomList;
    ArrivedRoomList.AppendElem2List(&Entrance);
    while(NULL != (pRoom = (Room*)RoomList.GetAElem()))
    {
        CreatRoad(pRoom);
    }
}
Map::Map(WORD32 RandSeed)
{
    MapDat = new UCHAR[W*H];
    printf("MapDat is 0x%08x\n",MapDat);
    memset(MapDat,INVALID_POINT,W*H);
    srand(RandSeed);
    SetEntrancePoint();
    GenRoom2List();
    RoomList.SortList();
    AddRoad();
    PrintAllRoom(&RoomList);
}

Map::~Map()
{
    delete MapDat;
}
WORD32 Map::GetRandRoomNum()
{
    static UCHAR FirstRunFlag = 0;
    static WORD32 RoomNum = 0;
    if(0 == FirstRunFlag)
    {
        FirstRunFlag = 1;
        RoomNum=GET_RAND(MAX_ROOM_NUM,MIN_ROOM_NUM);
    }
    //LogPrintf("RoomNum is %d\n",RoomNum);
    return RoomNum;
}
void Map::PrintMap()
{
	printf("Room Num is %d\n\n",RoomList.GetNodeNum());
    printf(" 012345678901234567890123456789012345678901234567890123456789\n");
    for(int y=0;y<H;y++)
        for(int x=0;x<W;x++)
            if(0==x)
                printf("%d%c%s",y%10,GetMapValue(x,y),((W-1)==x)?"|\n":"");
            else
                printf("%c%s",GetMapValue(x,y),((W-1)==x)?"|\n":"");
    printf(" 012345678901234567890123456789012345678901234567890123456789\n");
}
UCHAR Map::GetMapValue(int x,int y){return MapDat[x*H+y];}
VOID Map::SetMapValue(int x,int y,UCHAR v) {MapDat[x*H+y] = v;}

VOID Map::GenRoom2List()
{
    Room*pRoom=NULL;
    for(int i=0;i<GetRandRoomNum();i++)
    {
        pRoom=new Room();
        if(CheckRoomOcpMapFree(pRoom))
        {
            RoomList.AppendElem2List(pRoom);
            pRoom->SetNumber(RoomList.GetNodeNum()-1);
            pRoom->CalcDistanceToEntrance(Entrance.Getx(),Entrance.Gety());
            PutRoom2Map(pRoom);
            //pRoom->PrintInfo();
        }
        else
            delete (pRoom);
    }
    LogPrintf("List Node Num is %d\n",RoomList.GetNodeNum());
}
UCHAR Map::Dec2HexChar(int in)
{
	UCHAR tab[] = {'0','1','2','3','4','5','6','7','8','9',
		           'A','B','C','D','E','F','G','H','I','J',
		           'K','L','M','N','O','P','Q','R','S','T',
		           'U','V','W','X','Y','Z'};
    return tab[MIN(in,sizeof(tab))];
}
VOID Map::PrintAllRoom(List*pList)
{
    Room*pRoom = NULL;
    while(NULL != (pRoom = (Room*)pList->GetAElem()))
        pRoom->PrintInfo();
}
WORD32 Map::PutRoom2Map(Room*pRoom)
{
    for(int x=pRoom->GetLeftValue();x<=pRoom->GetRightValue();x++)
        for(int y=pRoom->GetUpValue();y<=pRoom->GetDownValue();y++)
            if((x==pRoom->Getx())&&(y==pRoom->Gety()))
                SetMapValue(x, y,Dec2HexChar(pRoom->GetNumber()));
            else if((y == pRoom->GetUpValue())||(y==pRoom->GetDownValue()))
                SetMapValue(x, y,'-');
            else if((x == pRoom->GetLeftValue())||(x==pRoom->GetRightValue()))
                SetMapValue(x, y,'|');
            //else
                //SetMapValue(x, y,'#');
    return SUCCESS;
}
bool Map::CheckRoomOcpMapFree(Room*pRoom)
{
    for(int x=pRoom->GetLeftValue();x<=pRoom->GetRightValue();x++)
        for(int y=pRoom->GetUpValue();y<=pRoom->GetDownValue();y++)
            if(INVALID_POINT!=GetMapValue(x, y))
            {
                //LogPrintf("Room is not In Map\n");
                return false;
            }
    //LogPrintf("Room is  In Map\n");
    return true;
}


