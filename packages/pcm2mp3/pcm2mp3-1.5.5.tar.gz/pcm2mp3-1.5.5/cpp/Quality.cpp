/*
 * Quality.cpp
 *
 *  Created on: 2 Dec 2017
 *      Author: julianporter
 */

#include "PyHeader.hpp"
#include "Member.hpp"


const char* ModuleName="pcm2mp3.quality";
 

using _ = Member;
static std::vector<Member> members {_("Best_Slowest",1),_("NearBest_Slow",2),_("Good_Fast",5),_("OK_VeryFast",7)};

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

PyMODINIT_FUNC PyInit_quality(void) {
	PyObject *m = PyModule_Create(&module);
	if(m==NULL) return NULL;
	std::for_each(members.begin(),members.end(),[m](Member &member) { member.add(m); });
	return m;
}


