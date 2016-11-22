/************************************************************
文件名:Log.c
功能描述:完成Log记录功能
作者:zhangkaimin10117906
修改记录:
2013-10-26    张凯敏          新建文件
*************************************************************/
#include "base/BaseTypes.h"
#include "PublicDef.h"
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

#define MAX_BUFFER_LEN 2048
UCHAR gucLogPrintSwitch = SWITCH_ON;
#ifdef CHECK_NULL_POINTER
#undef CHECK_NULL_POINTER
#endif
#define CHECK_NULL_POINTER(p)     if(NULL == (p))\
    {\
        printf("Pointer (%s) is NULL,exit \n",#p);\
        return FAILURE;\
    }
#ifdef CHECK_FUNCTION_RET
#undef CHECK_FUNCTION_RET
#endif
#define CHECK_FUNCTION_RET(ret)  if(FAILURE == (ret))\
    {\
        printf("Function return (%s) failure\n",#ret);\
        return FAILURE;\
    }
PRIVATE CHAR gaucLogBuffer[MAX_BUFFER_LEN] = {0};
PUBLIC const WORD32 LogOut(const CHAR*pucFileName, const CHAR* pucFunctionName, WORD32 udLine, const CHAR*pucFormat, ...)
{
    va_list ap;
    SWORD32 sdOutCharNum;

    CHECK_NULL_POINTER(pucFileName);
    CHECK_NULL_POINTER(pucFunctionName);
    CHECK_NULL_POINTER(pucFormat);
    va_start(ap, pucFormat);
    CHECK_FUNCTION_RET(sdOutCharNum = snprintf(gaucLogBuffer, MAX_BUFFER_LEN, "#%s-%s() L%d--", pucFileName, pucFunctionName, udLine));
    CHECK_FUNCTION_RET(vsnprintf(&gaucLogBuffer[sdOutCharNum], MAX_BUFFER_LEN - sdOutCharNum + 1, pucFormat, ap));
    printf(gaucLogBuffer);
    return SUCCESS;
}

PUBLIC WORD32 PrintCompilerTime(VOID)
{
    printf("Compiler Date And Time:%s %s\n", __DATE__, __TIME__);
    return SUCCESS;
}



