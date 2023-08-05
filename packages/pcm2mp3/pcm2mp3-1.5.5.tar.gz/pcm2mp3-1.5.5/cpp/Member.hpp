/*
 * Member.hpp
 *
 *  Created on: 2 Dec 2017
 *      Author: julianporter
 */

#ifndef MODULE_CPP_MEMBER_HPP_
#define MODULE_CPP_MEMBER_HPP_

#include <Python.h>
#include <string>
#include <stdexcept>

struct Member {
	std::string name;
	std::string description;
	unsigned value;
	PyObject *obj; 
	
	Member(const std::string &n,const unsigned v,const std::string &d) : name(n), description(d),value(v), obj(nullptr) {};
	Member(const std::string &n,const unsigned v) : Member(n,v,n) {};
	virtual ~Member();
	
	const char * cName() { return name.c_str(); };
	const char * cDescription() { return description.c_str(); };
	
	PyObject * add(PyObject *module);
};

#endif /* MODULE_CPP_MEMBER_HPP_ */
