#include <iostream>
#include "base/BaseTypes.h"
#include "Expr.h"

using namespace std;

class ExprNode
{
public:
    ExprNode():u(1){}
    virtual void print(ostream & out) = 0;
    virtual int eval() = 0;
    virtual int CalcPriority() = 0;
    virtual ~ExprNode(){}
    friend ostream & operator<<(ostream &out,ExprNode &e);
    int u;
};
int CalcPow(int op1, int op2)
{
    int result = 1;
    for(int i=0; i < op2; i++)result *= op1;
    return result;
}
int AddCalc(int op1, int op2){return op1 + op2;}
int SubCalc(int op1, int op2){return op1 - op2;}
int MulCalc(int op1, int op2){return op1 * op2;}
int DivCalc(int op1, int op2){if(0 == op2)return 0x7FFFFFFF;return op1 / op2;}
int ModCalc(int op1, int op2){return op1 % op2;}
int PowCalc(int op1, int op2){return CalcPow(op1, op2);}
PRIVATE struct PriorityTabType{
        CHAR op;
        int Priority;
        int (*pFCalc)(int,int);
        }OperatorTab[] ={{'+', 1, AddCalc},
                         {'-', 1, SubCalc},
                         {'*', 2, MulCalc},
                         {'/', 2, DivCalc},
                         {'%', 2, ModCalc},
                         {'@', 3, PowCalc}};
PRIVATE WORD32 DoCalcPriority(CHAR op)
{    
    for(int i=0;i<(sizeof(OperatorTab)/sizeof(struct PriorityTabType));i++)
        if(op == OperatorTab[i].op)
            return OperatorTab[i].Priority;
    return 1;
}
PRIVATE int DoCalcTwoExpr(CHAR op, int op1,int op2)
{
    for(int i=0;i<(sizeof(OperatorTab)/sizeof(struct PriorityTabType));i++)
        if(op == OperatorTab[i].op)
            return OperatorTab[i].pFCalc(op1,op2);
    return 0x7FFFFFFF;
}
class IntNode:public ExprNode
{
public:
    IntNode(int i):num(i),ExprNode(){}
    void print(ostream & out){out<<num;}
    int eval(){return num;}
    int CalcPriority(){return 1;}
private:
    int num;
};
class TwoExprNode:public ExprNode
{
public:
    TwoExprNode(CHAR opi, ExprNode *p1,ExprNode*p2):op(opi),Left(p1),Right(p2),ExprNode(){}
    void print(ostream & out){out<<"("<<*Left<<op<<*Right<<")";}
    ~TwoExprNode()
    {
        if(0 == --Left->u)delete Left;
        if(0 == --Right->u)delete Right;
    }
    int eval()
    {
        return DoCalcTwoExpr(op,Left->eval(),Right->eval());
    }
    int CalcPriority(){return DoCalcPriority(op);}
private:
    CHAR op;
    ExprNode*Left;
    ExprNode*Right;
};
class ExprCalc
{
public:
    ExprCalc():p(new IntNode(0)){}
    ExprCalc(int i){p=new IntNode(i);}
    ExprCalc(const ExprCalc&e){p = e.p;++p->u;}
    ExprCalc(CHAR s, ExprCalc e1, ExprCalc e2){p=new TwoExprNode(s,e1.p,e2.p);e1.p->u++;e2.p->u++;}

    int eval(){return p->eval();}
    ExprCalc & operator=(ExprCalc e)
    {
        e.p->u++;
        if(0 == --p->u) delete p;
        p = e.p;
        return *this;
    }
    int CalcPriority(){return p->CalcPriority();}
    friend ostream & operator<<(ostream &out,ExprCalc &e);
    ~ExprCalc(){if(0 == --p->u){delete p;}}
private:
    ExprNode *p;
};
ostream & operator<<(ostream &out,ExprNode &e)
{
    e.print(out);
    return out;
}
ostream & operator<<(ostream &out,ExprCalc &e)
{
    out<<*(e.p);
    return out;
}
PRIVATE int CalcAfterOpPriority(CHAR *pIn)
{
	if(0 == *(pIn+2))return 0;
	return DoCalcPriority(*(pIn+2));
}
PRIVATE ExprCalc ExprDo(const CHAR *pInStr, int PreviousPriority, int *pInOffset)
{
    CHAR op = '+';
    ExprCalc op1;
    ExprCalc op2;
    CHAR *pIn = (CHAR *)pInStr;
    int Offset = 0;

    op1 = ExprCalc((int)(*pIn - '0'));pIn++;
    do
    {
        while((0 != *pIn)
			  && (DoCalcPriority(*pIn) >= op1.CalcPriority())
			  && (DoCalcPriority(*pIn) >= PreviousPriority)
			  && (DoCalcPriority(*pIn) >= CalcAfterOpPriority(pIn)))
        {
            op = *pIn;pIn++;
            op1 = ExprCalc(op, op1, (int)(*pIn - '0'));pIn++;
        }
        if((0 == *pIn)
           || ((0 != *pIn)
		       && (0 != PreviousPriority)
			   && (DoCalcPriority(*pIn) <= op1.CalcPriority()))
			   && ((DoCalcPriority(*pIn) <= PreviousPriority)))

        {
            *pInOffset = pIn - (CHAR *)pInStr;
            return op1;
        }
        op = *pIn;pIn++;
        Offset = 0;
        op2 = ExprDo(pIn, DoCalcPriority(op), &Offset);
		pIn += Offset;
        op1 = ExprCalc(op, op1, op2);
    }while('0' != *pIn);
    *pInOffset = pIn - (CHAR *)pInStr;
    return op1;
}
int Expr(const CHAR *const expression)
{
    const CHAR *pIn = expression;
	int InOffset = 0;
    ExprCalc result = ExprDo((const CHAR *)pIn, 0, &InOffset);
    //cout<<result<<" = "<<result.eval()<<endl;
    return result.eval();
}


