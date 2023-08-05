/*
 * Member.cpp
 *
 *  Created on: 2 Dec 2017
 *      Author: julianporter
 */

#include "Member.hpp"

Member::~Member() {
	Py_CLEAR(obj);
	obj=nullptr;
}

PyObject * Member::add(PyObject *module) {
	try {
		obj=PyLong_FromUnsignedLong(value);
		if(obj==NULL) throw std::runtime_error("Allocation of integer property failed");
		Py_INCREF(obj);
		auto result=PyModule_AddObject(module,name.c_str(),obj);
		if(result<0) throw std::runtime_error("Cannot add integer property to module");
		return obj;
	}
	catch(const std::exception &e) {
		PyErr_SetString(PyExc_ImportError,e.what());
		return NULL;
	}
}

