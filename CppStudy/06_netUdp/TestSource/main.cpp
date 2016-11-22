#include <iostream>
#include "base/BaseTypes.h"
#include "GeneralFunction.h"
#include <unistd.h>
#include <stdlib.h>
#include <sys/socket.h>

using namespace std;


VOID StartServer(VOID)
{

}

VOID StartClient(VOID)
{

}

int main(int argc, char **argv)
{
    pid_t ret;

    ret=fork();
    if(ret < 0)
    {
    	cout<<"fork error"<<endl;
    	return 1;
    }
    else if(0==ret)
    {
    	cout<<"I am SON and Server, pid is "<<getpid()<<endl;
    	StartServer();
    }
    else
    {
    	cout<<"I am FATHER and Client, pid is "<<getpid()<<endl;
    	StartClient();
    }
    return 0;
}



