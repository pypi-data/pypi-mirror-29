/*
 * transcoder.cpp
 *
 *  Created on: 4 Dec 2017
 *      Author: julianporter
 */

#include "transcoder.hpp"
#include <base.hpp>
#include <mp3/MP3Encoder.hpp>
#include <pcm/WAVFile.hpp>
#include <pcm/AIFFFile.hpp>
#include <pcm/PCMFile.hpp>
#include <Parameters.hpp>

namespace pylame {

data_t load(std::istream &stream) {
	stream.seekg (0, stream.end);
	auto length = stream.tellg();
	stream.seekg (0, stream.beg);

	data_t file(length,0);
	auto c=file.data();
	int pos=0;
	while(pos<length) {
		stream.read(c+pos,1024);
		pos+=stream.gcount();
	}
	return std::move(file);
}

template <typename T>
std::shared_ptr<pcm::PCMFile> make(const data_t &in) {
	auto p = std::make_shared<T>(in);
	return std::static_pointer_cast<pcm::PCMFile>(p);
}

Transcode::Transcode(const Parameters &parameters,const data_t &in) : out()  {
	std::shared_ptr<pcm::PCMFile> infile;
	if(pcm::WAVFile::isInstance(in)) {
		infile=make<pcm::WAVFile>(in);
	}
	else if(pcm::AIFFFile::isInstance(in)) {
		infile=make<pcm::AIFFFile>(in);
	}
	else throw MP3Error("Unrecognised file format");

	mp3::MP3Encoder trans(parameters,infile);
	trans.transcode();
	out.assign(trans.cbegin(),trans.cend());

}

const char* Transcode::ptr() const {
	const unsigned char *u=out.data();
	const char *d=reinterpret_cast<const char *>(u);
	return d;
}

std::ostream & Transcode::output(std::ostream &o) const {
		o.write(ptr(),size());
		return o;
	};


}

std::ostream & operator<<(std::ostream &o,const pylame::Transcode &t) {
	return t.output(o);
}
std::istream & operator>>(std::istream &i,pylame::Transcode &t) {
	t=pylame::Transcode(pylame::Parameters(),i);
	return i;
}


