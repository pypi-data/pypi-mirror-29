/*
 * enums.cpp
 *
 *  Created on: 30 Nov 2017
 *      Author: julianporter
 */


#include "base.hpp"

using namespace pylame;

#include <cstdlib>
#include <locale>

std::ostream & operator<<(std::ostream &o,const MP3Error &ex) {
	o << "MP3Error : " << ex.what();
	return o;
}

std::locale l;
char up(const char c) { return std::toupper(c,l); };
char down(const char c) { return std::tolower(c,l); };

std::string pylame::toUpper(const std::string &s) {
	std::vector<char> bytes(s.size(),0);
	std::transform(s.begin(),s.end(),bytes.begin(), up);
	return std::move(std::string(bytes.begin(),bytes.end()));
}
std::string pylame::toLower(const std::string &s) {
	std::vector<char> bytes(s.size(),0);
	std::transform(s.begin(),s.end(),bytes.begin(), down);
	return std::move(std::string(bytes.begin(),bytes.end()));
}
