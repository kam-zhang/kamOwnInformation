#include "Python.h"
#include <stdio.h>

int calcAdd(int a, int b)
{
    return a + b;
}

int main(int argc, char*argv[])
{
    int c = calcAdd(2,3);
    printf("c=%d\n",c);
    return 0;
}

static PyObject*mytest_calcAdd(PyObject*self,PyObject*args)
{
    int a,b;
    if(!PyArg_ParseTuple(args, "ii",&a,&b))
        return NULL;
    return (PyObject*)Py_BuildValue("i",calcAdd(a,b));
}

static PyMethodDef testMethods[]={
    {"calcAdd",mytest_calcAdd,METH_VARARGS},
    {NULL,NULL}
};

void initmytest() {
    Py_InitModule("mytest", testMethods);
}


