#ifndef INCL_GENERAL_FUNCTION_H_
#define INCL_GENERAL_FUNCTION_H_

extern VOID PrintHex(const CHAR* pName, const VOID*p, WORD32 n);
#define MemoryPrint(a) PrintHex("Expression:"#a,(VOID*)&(a),sizeof(a))

#endif


