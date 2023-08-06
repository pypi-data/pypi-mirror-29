#ifndef BITPRIM_PY_CHAIN_OUTPUT_H_
#define BITPRIM_PY_CHAIN_OUTPUT_H_

#include <Python.h>
#include <bitprim/nodecint.h>
#include "../utils.h"

#ifdef __cplusplus
extern "C" {  
#endif  


PyObject* bitprim_native_chain_output_is_valid(PyObject* self, PyObject* args);
PyObject* bitprim_native_chain_output_serialized_size(PyObject* self, PyObject* args);
PyObject* bitprim_native_chain_output_value(PyObject* self, PyObject* args);
PyObject* bitprim_native_chain_output_signature_operations(PyObject* self, PyObject* args);
PyObject* bitprim_native_chain_output_destruct(PyObject* self, PyObject* args);
PyObject* bitprim_native_chain_output_script(PyObject* self, PyObject* args);

//PyObject* bitprim_native_chain_output_get_hash(PyObject* self, PyObject* args);
//PyObject* bitprim_native_chain_output_get_index(PyObject* self, PyObject* args);


#ifdef __cplusplus
} //extern "C"
#endif  


#endif
