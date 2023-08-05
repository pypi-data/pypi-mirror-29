/*
 * main.cpp
 *
 *  Created on: 30 Nov 2017
 *      Author: julianporter
 */
 
#include "lamer.hpp"
#include <regex>
#include <sstream>

#define MODE WAV

int main(int argc,char *argv[]) {
	try {
		std::string infile(argv[1]);
		std::regex r("^([^.]+)\\.(.+)$");
		std::smatch matcher;
		std::regex_match(infile,matcher,r);
		auto prefix=matcher[1];
		auto suffix=matcher[2];
		std::stringstream s;
		s << prefix << ".mp3";
		auto outfile=s.str();

		unsigned rate=8;
		if(argc>2) {
			std::string r(argv[2]);
			rate=std::stoul(r);
		}
		unsigned quality=5;
		if(argc>3) {
			std::string q(argv[3]);
			quality=std::stoul(q);
		}

		std::cout << "Loading " << infile << std::endl;
 		std::ifstream wav(infile,std::ifstream::binary);
		std::cout << "Transcoding with output bit-rate " << rate << "kbps, quality " << quality << std::endl;
		pylame::Transcode transcoder(wav,quality,rate);
		std::cout << "Writing to " << outfile << std::endl;
		std::ofstream out(outfile,std::ofstream::binary);
		out << transcoder;
		out.close();
		std::cout << "Completed" << std::endl;
//#endif
	}
	catch(std::exception &e) {
		std::cerr << e.what() << std::endl;
	}
	return 0;
 }




