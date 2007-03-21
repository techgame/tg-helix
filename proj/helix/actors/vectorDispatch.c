
/* Vectorized Calling module */

/*
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
*/

#include <Python.h>

/* ******************************************** */

static PyObject *
vectorDispatch(PyObject *self, PyObject *args)
{
    PyObject *callables;
    PyObject *vecArgs;

    if (!PyArg_UnpackTuple(args, "vectorDispatch", 2, 2, &callables, &vecArgs)) 
        return NULL;

    /* seqCallables is a NewReference */
    const char* seqFastErrMsg = "";
    PyObject *seqCallables;
    printf("PySequence_Fast\n");
    seqCallables = PySequence_Fast(callables, seqFastErrMsg);
    if (!PySequence_Check(seqCallables)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of callables");
        return NULL;
    }

    /*
    printf("PyTuple_GetSlice...\n");
    PyObject *vecArgs;
    vecArgs = PyTuple_GetSlice(args, 1, PyTuple_Size(args));
    */

    printf("PySequence_Fast_ITEMS...\n");
    int count = PySequence_Fast_GET_SIZE(seqCallables);
    PyObject** vecCallabls;
    PySequence_Fast_ITEMS(seqCallables);

    int idx;
    for (idx=0; idx<count; idx++) {
        printf("PyObject_Call\n");
        if (!PyObject_Call(vecCallabls[idx], vecArgs, NULL)) {
            Py_DECREF(seqCallables);
            //Py_DECREF(vecArgs);
            return NULL;
        }
    }

    Py_DECREF(seqCallables);
    //Py_DECREF(vecArgs);

    Py_INCREF(Py_None);
    return Py_None;
}
PyDoc_STRVAR(vectorDispatch_doc,
"vectorDispatch(vecCallables, *args):\n\
    for vcall in vecCallables:\n\
        vcall(*args)\n\
    return None;\n\
");

/* ******************************************** */

static PyMethodDef CallVectorDispatchMethods[] = {
    {"vectorDispatch",  vectorDispatch, METH_VARARGS, vectorDispatch_doc},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

/* Initialize this module. */

PyDoc_STRVAR(module_doc,
"Vectorized Calling");


PyMODINIT_FUNC
initvectorDispatch(void)
{
	PyObject *module;
	module = Py_InitModule3("vectorDispatch", CallVectorDispatchMethods, module_doc);
	if (module == NULL)
	    return;
}

