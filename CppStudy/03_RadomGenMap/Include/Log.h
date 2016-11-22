/************************************************************
文件名:Log.h
功能描述:完成Log记录功能，可以通过宏或
                       开关控制是否打印Log
作者:zhangkaimin10117906
修改记录:
2013-10-26    张凯敏          新建文件
*************************************************************/

#ifndef _INCL_LOG_H_
#define _INCL_LOG_H_
#include "./base/stdc.h"
#include "./base/BaseTypes.h"

EXTERN_STDC_BEGIN

/* 请勿调用下接口，LogOut()，而是调用LogPrintf()接口，便于控制 */
PUBLIC const WORD32 LogOut(const CHAR*pucFileName,const CHAR* pucFunctionName,WORD32 udLine,const CHAR*pucFormat,...);

PUBLIC UCHAR gucLogPrintSwitch;
#define ENABLE_LOG
#ifdef ENABLE_LOG
#define LogPrintf(...) ((SWITCH_ON == gucLogPrintSwitch)?LogOut(__FILE__, __FUNCTION__, __LINE__,  __VA_ARGS__):(FAILURE))
#else
#define LogPrintf(...) SUCCESS
#endif

PUBLIC WORD32 PrintCompilerTime(VOID);

EXTERN_STDC_END

#endif




