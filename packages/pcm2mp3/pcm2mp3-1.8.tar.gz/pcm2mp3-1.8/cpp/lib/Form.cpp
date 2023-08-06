/*
 * Form.cpp
 *
 *  Created on: 21 Dec 2017
 *      Author: julianporter
 */

#include "Form.hpp"
#include <cstdlib>
#include <locale>

namespace pylame {
namespace pcm {

bool FormMetaData::verify(const std::string &head,const TypeMap &formats) {
	try {
		if(header!=head) throw MP3Error("Form header mismatch with expected header");
		auto it=formats.find(format);
		if(it==formats.end()) throw MP3Error("Form type does not match any of those available");
		type=it->second;
		return true;
	}
	catch(std::exception &e) {
		//std::cerr << e.what() << std::endl;
		type=FileType::Other;
		return false;
	}
};

bool Form::nextChunk() {
	try {
		auto idx=toUpper(it.next<std::string>());
		auto n=it.next<uint32_t>();
		auto c=std::make_shared<DataChunk>(idx,std::move(it.getN(n)),endian);
		//chunks[idx]=c;
		chunks.insert(std::make_pair(idx,c));
		return true;
	}
	catch(...) {
		return false;
	}
}

FormMetaData Form::typeCheck() {
	try {
		auto h=it.next<std::string>();
		len=it.next<uint32_t>() ;
		auto t=it.next<std::string>();
		return FormMetaData(h,t,len);
	}
	catch(std::exception &e) {
		//std::cerr << "Exception is" << e.what() << std::endl;
		throw e;
	}
}

void Form::walk() {
	while(nextChunk()) {};
	//std::for_each(chunks.begin(),chunks.end(),[](auto c) { std::cout << c.first << std::endl; });
}

std::shared_ptr<DataChunk> Form::operator[](const std::string &ID) {
	try {
		auto ptr = chunks.find(ID);
		if(ptr==chunks.end()) throw MP3Error("No such chunk");
		return ptr->second;
	}
	catch(...) {
		throw MP3Error("No such chunk");
	}
}



} /* namespace pcm */
} /* namespace pylame */

std::ostream & operator<<(std::ostream &o,const pylame::pcm::FormMetaData &m) {
	o << "Form header = '" << m.header << "'" << std::endl;
	o << "Format      = '" << m.format << "'" << std::endl;
	o << "Length = " <<  std::hex << m.length << std::dec << std::endl;
	return o;
}

