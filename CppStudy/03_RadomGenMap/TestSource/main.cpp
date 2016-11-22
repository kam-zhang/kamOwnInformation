#include "Map.h"
#include "base/BaseTypes.h"
#include "GeneralFunction.h"
using namespace std; 
class Arg
{
    private:

    public:
        WORD32 Deal(int argc, char* argv[])
        {
            #define DEFAULT_SRAND 9876
            WORD32 temp = 0;
            //printf("argc:%d\n",argc);
            if(2>=argc)return DEFAULT_SRAND;
            CHAR*pIn=argv[1];
            if(0!=strcmp(pIn,"-s"))return DEFAULT_SRAND;
            pIn=argv[2];
            //printf("%s\n",pIn);
            while('\0'!=*pIn)
                if((*pIn<'0')||(*pIn>'9'))
                    return DEFAULT_SRAND;
                else
                    temp=temp*10+((*pIn++)-'0');
            return temp;
        }
};
int main(int argc, char* argv[])
{
    Arg arg;
    WORD32 RandSeed=arg.Deal(argc,argv);
    printf("RandSeed is %d\n",RandSeed);
    Map map(RandSeed);
    map.PrintMap();
    MemoryPrint(map);
    MemoryPrint(arg);
    return 0;
}


