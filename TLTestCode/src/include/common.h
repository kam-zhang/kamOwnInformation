#ifndef _COMMON_H_
#define _COMMON_H_
#include <stdio.h>
typedef signed int SWORD32;
typedef unsigned int WORD32;

#define PRIVATE static

#define CHECK(logicValue, statement) { \
                                        if(!(logicValue)) \
                                        { \
                                            printf("%s:%s\(\):Line%d--%s is error\n",__FILE__,__FUNCTION__,__LINE__,#logicValue); \
                                            statement; \
                                        }\
                                     }


#endif


