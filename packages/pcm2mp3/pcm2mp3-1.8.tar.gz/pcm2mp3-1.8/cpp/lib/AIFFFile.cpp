/*
 * AIFFFile.cpp
 *
 *  Created on: 5 Dec 2017
 *      Author: julianporter
 */

#include "AIFFFile.hpp"
#include "Conversions.hpp"
#include "PCMData.hpp"
#include <cstdlib>
#include <locale>

namespace pylame { namespace pcm {

DataFormat AIFFFile::convertFormat(const std::string &f) {
	    auto fmt=toLower(f);
	    if(fmt=="none" || fmt=="sowt") return DataFormat::PCM;
	    else if(fmt=="fl32" || fmt=="fl64") return DataFormat::IEEEFloat;
	    else if(fmt=="ulaw") return DataFormat::ULaw;
	    else if(fmt=="alaw") return DataFormat::ALaw;
	    else throw MP3Error("Unknown AIFC data format");
}

std::string AIFFFile::FormHeader() const { return "FORM"; };

FormMetaData::TypeMap AIFFFile::FormTypes() const {
		return {
			{"AIFF",FileType::AIFF},
			{"AIFC",FileType::AIFC}
		};
};



AIFFFile::AIFFFile(const data_t &file_) : PCMFile(file_) {
	Iterator32 it(file,Endianness::BigEndian);
	parse(it,"COMM","SSND");
}



AIFFFile::AIFFFile(std::istream &stream) : PCMFile(stream) {
	Iterator32 it(file,Endianness::BigEndian);
    parse(it,"COMM","SSND");
}


void AIFFFile::infoChunk(const std::shared_ptr<DataChunk> &comm) {
	
    auto itc=comm->iterator();
    
    auto p1=itc.next<pair_t>();
    auto p2=itc.next<pair_t>();
    nChannels=(unsigned)p1.first;
    nSamples=swap(p1.second,p2.first);
    bitsPerSample=(unsigned)p2.second;
    sampleRate=(unsigned)itc.next<long double>();
    if(!isAIFC()) format=DataFormat::PCM;
    else format=AIFFFile::convertFormat(itc.next<std::string>());
}

void AIFFFile::soundChunk(const std::shared_ptr<DataChunk> &ssnd) {
	 	dataSize=ssnd->size()-8;
	 	auto it=ssnd->iterator();
	 	offset=it.next<uint32_t>();
	 	blocksize=it.next<uint32_t>();
	 	if(it.size()!=dataSize) throw MP3Error("Data size error");
}

PCMData AIFFFile::bytes() {
	if(format!=DataFormat::PCM and format!=DataFormat::IEEEFloat) throw MP3Error("Can only enumerate Int16, Int32 or Float32 files");
	if(offset!=0 || blocksize!=0) throw MP3Error("Cannot enumerate blocked data sets");
	auto qr=std::div(bitsPerSample,8);
	if(qr.rem!=0) throw MP3Error("Cannot enumerate non-integral byte samples");
	bytesPerSample=qr.quot;

	std::shared_ptr<DataChunk> ssnd=form["SSND"];
	auto it=ssnd->iterator();
	it.skip(2);
	return PCMData(sampleFormat(),nChannels,nSamples,it);
}


bool AIFFFile::isInstance(const data_t &d) {
			try {
				AIFFFile w(d);
				return true;
			}
			catch(...) {
				return false;
			}
		};
bool AIFFFile::isInstance(std::istream &stream) {
			try {
				AIFFFile w(stream);
				return true;
			}
			catch(...) {
				return false;
			}
		};

}}

