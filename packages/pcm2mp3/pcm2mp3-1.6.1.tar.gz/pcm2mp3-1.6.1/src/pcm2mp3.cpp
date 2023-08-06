/*
 * main.cpp
 *
 *  Created on: 30 Nov 2017
 *      Author: julianporter
 */
 
#include "lamer.hpp"
#include <cli.hpp>
#include <regex>
#include <sstream>

#define MODE WAV

int main(int argc,char *argv[]) {
	try {
		CLI::App app{"PCM2MP3 audio format converter test wrapper"};


		std::string infile="file.wav";
		unsigned rate=8;
		unsigned quality=5;
		bool compress=false;
		bool boost=true;

		app.add_option("-i,--infile",infile,"The PCM file to convert");
		app.add_option("-r,--bitrate",rate,"MP3 output bitrate (kbps)");
		app.add_option("-q,--quality",quality,"Conversion quality");
		app.add_flag("-b,--boost",boost,"Boost signal to maximise volume");
		app.add_flag("-c,--compress",compress,"Apply compression effect (creates distortion)");

		try {
		    app.parse(argc, argv);
		} catch (const CLI::ParseError &e) {
		    return app.exit(e);
		}

		std::regex r("^([^.]+)\\.(.+)$");
		std::smatch matcher;
		std::regex_match(infile,matcher,r);
		auto prefix=matcher[1];
		auto suffix=matcher[2];
		std::stringstream s;
		s << prefix << ".mp3";
		auto outfile=s.str();

		pylame::Parameters p(rate,quality,boost,compress);
		std::cout << p;

		std::cout << "Loading " << infile << std::endl;
 		std::ifstream wav(infile,std::ifstream::binary);
		std::cout << "Transcoding with output bit-rate " << rate << "kbps, quality " << quality << std::endl;
		pylame::Transcode transcoder(p,wav);
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




