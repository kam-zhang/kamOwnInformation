/************************************************************
�ļ���:PublicDef.h
��������:���õĶ���
����:zhangkaimin10117906
�޸ļ�¼:
2013-11-8    �ſ���          �½��ļ�
*************************************************************/

#ifndef INCL_PUBLIC_MACRO_H_
#define INCL_PUBLIC_MACRO_H_

#define CHECK_NULL_POINTER(p)     if(NULL == (p))\
    {\
        LogPrintf("FILE:%s-L%d:Pointer (%s) is NULL,exit \n",__FILE__,__LINE__,#p);\
        return InvalidValue;\
    }
#define CHECK_FUNCTION_RET(ret)  if(InvalidValue == (ret))\
    {\
        LogPrintf("FILE:%s-L%d:Function return (%s) failure\n",__FILE__,__LINE__,#ret);\
        return InvalidValue;\
    }
#define CHECK(LogicValue)   if(!(LogicValue))\
    {\
        LogPrintf("FILE:%s-L%d:LogicValue(%s) is %d\n",__FILE__,__LINE__,#LogicValue,LogicValue);\
        return InvalidValue;\
    }
#endif
