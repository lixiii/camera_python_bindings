
make:
	g++ -shared -o _camera.so main.cpp -Iinclude -Llib/arm -fPIC `python3 -m pybind11 --includes` -lMVSDK

