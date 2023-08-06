/**
 * Copyright (c) 2017 Bitprim developers (see AUTHORS)
 *
 * This file is part of Bitprim.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef BITPRIM_PY_BITPRIMMODULE_H_
#define BITPRIM_PY_BITPRIMMODULE_H_

#include <Python.h>

#ifdef __cplusplus
extern "C" {  
#endif  

PyObject* bitprim_native_executor_construct(PyObject* self, PyObject* args);
PyObject* bitprim_native_executor_destruct(PyObject* self, PyObject* args);
PyObject* bitprim_native_executor_initchain(PyObject* self, PyObject* args);
PyObject* bitprim_native_executor_run(PyObject* self, PyObject* args);
PyObject* bitprim_native_executor_run_wait(PyObject* self, PyObject* args);
PyObject* bitprim_native_executor_stopped(PyObject* self, PyObject* args);
PyObject* bitprim_native_executor_stop(PyObject* self, PyObject* args);
PyObject* bitprim_native_executor_get_chain(PyObject* self, PyObject* args);
PyObject* bitprim_native_wallet_mnemonics_to_seed(PyObject* self, PyObject* args);

#ifdef __cplusplus
} // extern "C"
#endif  

#endif // BITPRIM_PY_BITPRIMMODULE_H_
