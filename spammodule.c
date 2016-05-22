#include "python.h"
//#include "methodobject.h"

//#define METH_VARARGS  0x0001

static PyObject *
spam_strlen(PyObject *self, PyObject *args)
{

        char* str;
        int   len;

        if(!PyArg_ParseTuple(args, "s", &str))
                return NULL;

        len = strlen(str);
        return Py_BuildValue("i", len);
}

static PyMethodDef 
SpamMethods[] = {
    {"strlen", spam_strlen, METH_VARAGRS },
    {NULL, NULL },
};

static struct PyModuleDef 
spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",
    "It is test module",
    -1,
    SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void){
    return PyModule_Create(&spammodule);
}