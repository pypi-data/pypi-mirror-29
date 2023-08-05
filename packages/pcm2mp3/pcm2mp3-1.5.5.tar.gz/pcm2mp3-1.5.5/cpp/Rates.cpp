/*
 * Rates.cpp
 *
 *  Created on: 2 Dec 2017
 *      Author: julianporter
 */

#include "PyHeader.hpp"
#include "Member.hpp"


const char* ModuleName="pcm2mp3.rates";
 

using _ = Member;
static std::vector<Member> members {_("Best",128),_("Good",64),_("Moderate",48),_("Low",8)};

static struct PyModuleDef module = {
		PyModuleDef_HEAD_INIT,
		ModuleName,
		"",			/// Documentation string
		-1,			/// Size of state (-1 if in globals)
		NULL,
		NULL,		/// Slots
		NULL,		/// traverse
		NULL,		/// clear
		NULL		/// free
}; 


PyMODINIT_FUNC PyInit_rates(void) {
	PyObject *m = PyModule_Create(&module);
	if(m==NULL) return NULL;
	std::for_each(members.begin(),members.end(),[m](Member &member) { member.add(m); });
	return m;
}
