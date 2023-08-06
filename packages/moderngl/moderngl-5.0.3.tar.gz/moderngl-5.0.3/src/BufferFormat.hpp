#pragma once

struct FormatNode {
	int size;
	int count;
	int type;
	bool normalize;
};

struct FormatInfo {
	int size;
	int nodes;
	int divisor;
	bool valid;
};

struct FormatIterator {
	const char * ptr;
	FormatNode node;

	FormatIterator(const char * str);

	FormatInfo info();
	FormatNode * next();
};

extern FormatNode * InvalidFormat;
