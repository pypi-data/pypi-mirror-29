/*
 * Lame.c
 *
 *  Created on: 1 Dec 2017
 *      Author: julianporter
 */


//#include "lib/WAVFile.hpp"
//#include "lib/MP3Encoder.hpp"
//#include "lib/Iterator32.hpp"
//#include "lib/transcoder.hpp"
#include <sstream>
#include <regex>
#include <iostream>
#include <fstream>
#include <stdexcept>

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <pcm2mp3.hpp>

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

static PyObject *mp3Error;
static char *keywordsFile[]={"","","bitrate","quality"};
static char *keywordsStream[]={"","bitrate","quality"};



bool checkName(const char *name,const char *suffix) {
	std::stringstream s;
	s << ".*\\." << suffix << "$";
	return std::regex_match(name,std::regex(s.str()));
}

static PyObject *mp3transcode_file(PyObject *self,PyObject *args,PyObject *keywds) {
	unsigned bitRate = 64;
	unsigned quality = 5;

	const char *inFile;
	const char *outFile;


	try {

		if(!PyArg_ParseTupleAndKeywords(args,keywds,"ss|$II",keywordsFile,&inFile,&outFile,&bitRate,&quality)) {
			throw PException(PyExc_TypeError,"API is transcode(infile,outfile,bitrate=64,quality=5)");
		}
		try {
			std::ifstream wavFile(inFile,std::ifstream::binary);
			pylame::Parameters p(bitRate,quality);
			pylame::Transcode transcode(p,wavFile);
			std::ofstream out(outFile,std::ofstream::binary);
			out << transcode;
			out.close();
			return PyLong_FromUnsignedLong((unsigned long)transcode.size());
		}
		catch(std::exception &e) {
			throw PException(mp3Error,e.what());
		}
	}
	catch(PException &p) {
		return p();
	}
}

static PyObject *mp3transcode_stream(PyObject *self,PyObject *args,PyObject *keywds) {
	unsigned bitRate = 64;
	unsigned quality = 5;

	try {
		Py_buffer buffer;
		if(!PyArg_ParseTupleAndKeywords(args,keywds,"y*|$II",keywordsStream,&buffer,&bitRate,&quality)) {
			throw PException(PyExc_TypeError,"API is transcode(stream,bitrate=64,quality=5)");
		}
		try {
			char *orig=(char *)buffer.buf;
			pylame::pcm_t data(orig,orig+buffer.len);
			pylame::Parameters p(bitRate,quality);
			pylame::Transcode transcode(p,data);
			auto out = Py_BuildValue("y#",transcode.ptr(),transcode.size());
			PyBuffer_Release(&buffer);
			return out;
		}
		catch(std::exception &e) {
			throw PException(mp3Error,e.what());
		}
	}
	catch(PException &p) {
		return p();
	}
}





static struct PyMethodDef methods[] = {
		{"transcodeFile",(PyCFunction) mp3transcode_file, METH_VARARGS | METH_KEYWORDS, "Transcodes data in file"},
		{"transcodeStream",(PyCFunction) mp3transcode_stream, METH_VARARGS | METH_KEYWORDS, "Transcodes data in stream"},
		{NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION==3
static struct PyModuleDef module = {
		PyModuleDef_HEAD_INIT,
		"pcm2mp3",
		"",			/// Documentation string
		-1,			/// Size of state (-1 if in globals)
		methods
};
#endif






PyMODINIT_FUNC
PyInit_pcm2mp3(void) {
#if PY_MAJOR_VERSION==3
	PyObject *m = PyModule_Create(&module);
	if(m==NULL) return NULL;
#else
	PyObject *m = Py_InitModule3("pcm2mp3",methods,"");
	if(m==NULL) return;
#endif



	try {
		std::stringstream s;

		mp3Error=PyErr_NewException("pcm2mp3.MP3Error",NULL,NULL);
		if(mp3Error==NULL) throw std::runtime_error("Cannot allocate MP3Error");
		Py_INCREF(mp3Error);
		auto result=PyModule_AddObject(m,"MP3Error",mp3Error);
		if(result<0) throw std::runtime_error("Cannot attach MP3Error to module");
#if PY_MAJOR_VERSION==3
		return m;
#endif
	}
	catch(std::exception &e) {
		PyErr_SetString(PyExc_ImportError,e.what());
#if PY_MAJOR_VERSION==3
		return NULL;
#endif
	}
}



