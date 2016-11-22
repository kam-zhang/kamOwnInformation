/************************************************************
文件名:PublicDef.h
功能描述:公用的定义
作者:zhangkaimin10117906
修改记录:
2013-11-8    张凯敏          新建文件
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
