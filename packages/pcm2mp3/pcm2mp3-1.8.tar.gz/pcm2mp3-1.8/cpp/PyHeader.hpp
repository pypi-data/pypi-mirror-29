/*
 * PyHeader.hpp
 *
 *  Created on: 2 Dec 2017
 *      Author: julianporter
 */

#ifndef MODULE_CPP_PYHEADER_HPP_
#define MODULE_CPP_PYHEADER_HPP_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>

class PException : public std::exception {
private:
	PyObject *ex;
	std::string message;
public:
	PException(PyObject *type,const std::string &message_) : std::exception(), ex(type), message(message_) {};
	virtual ~PException() = default;

	virtual const char *what() const noexcept { return message.c_str(); };
	PyObject *operator()() {
		PyErr_SetString(ex,what());
		return nullptr;
	}
};


#endif /* MODULE_CPP_PYHEADER_HPP_ */
