/************************************************************
�ļ���:Log.h
��������:���Log��¼���ܣ�����ͨ�����
                       ���ؿ����Ƿ��ӡLog
����:zhangkaimin10117906
�޸ļ�¼:
2013-10-26    �ſ���          �½��ļ�
*************************************************************/

#ifndef _INCL_LOG_H_
#define _INCL_LOG_H_
#include "./base/stdc.h"
#include "./base/BaseTypes.h"

EXTERN_STDC_BEGIN

/* ��������½ӿڣ�LogOut()�����ǵ���LogPrintf()�ӿڣ����ڿ��� */
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




