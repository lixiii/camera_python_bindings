
make:
	g++ -shared -o camera_capture.so main.cpp -Iinclude -Llib/arm -fPIC `python3 -m pybind11 --includes` -lMVSDK

