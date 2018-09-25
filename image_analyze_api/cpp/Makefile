CXX ?= g++

CXXFLAGS += -std=c++11 -c -Wall $(shell pkg-config --static --cflags opencv curlpp)
LDFLAGS += $(shell pkg-config --libs opencv curlpp)

all: http_file_jpg http_camera_raw

http_file_jpg: http_file_jpg.o; $(CXX) $< -o $@ $(LDFLAGS)

http_camera_raw: http_camera_raw.o; $(CXX) $< -o $@ $(LDFLAGS)

%.o: %.cpp; $(CXX) $< -o $@ $(CXXFLAGS)

clean: ; rm -f http_file_jpg.o http_camera_raw.o http_file_jpg http_camera_raw
